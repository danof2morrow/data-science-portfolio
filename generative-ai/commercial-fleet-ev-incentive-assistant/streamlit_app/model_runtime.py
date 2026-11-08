"""Load only the saved full model from the submitted Milestone 3 run."""

from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import os
import threading
import time

from training_contract import (BASE_MODEL_ID, EXPECTED_MANIFEST_PREFIX,
                               EXPECTED_RUN_ID, MAX_INPUT_TOKENS,
                               MAX_NEW_TOKENS, SYSTEM_PROMPT)


def find_model_folder():
    configured = os.environ.get('DSC670_MODEL_DIR')
    if configured:
        return str(Path(configured).expanduser())
    adjacent = Path(__file__).resolve().parent / 'full_model'
    if adjacent.is_dir():
        return str(adjacent)
    colab = (Path('/content/drive/MyDrive/DSC670_Milestone3_Full_Fine_Tuning')
             / EXPECTED_RUN_ID / 'full_model')
    return str(colab if colab.is_dir() else adjacent)


def _sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def verify_saved_model(folder):
    """Check the saved artifact's identity before loading any weights."""
    folder = Path(folder).expanduser().resolve()
    if not folder.is_dir():
        raise FileNotFoundError('The saved full_model folder is not available.')
    parent = folder.parent
    required = ['model_manifest.json', 'training_complete.json', 'reports/recipe.json']
    for name in required:
        if not (parent / name).is_file():
            raise ValueError(f'The extracted training run is missing {name}.')
    manifest = json.loads((parent / 'model_manifest.json').read_text())
    fingerprint = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
    if not fingerprint.startswith(EXPECTED_MANIFEST_PREFIX):
        raise ValueError('This model manifest does not match the submitted fine-tuned model.')
    recipe = json.loads((parent / 'reports/recipe.json').read_text())
    run_id = hashlib.sha256(json.dumps(recipe, sort_keys=True).encode()).hexdigest()[:12]
    if run_id != EXPECTED_RUN_ID or recipe.get('model') != BASE_MODEL_ID:
        raise ValueError('The training recipe belongs to a different model run.')
    if recipe.get('system_prompt') != SYSTEM_PROMPT:
        raise ValueError('The inference instructions do not match the saved training recipe.')
    if 'config.json' not in manifest or not any(name.endswith('.safetensors') for name in manifest):
        raise ValueError('The export must contain the complete model and tokenizer.')
    for name, details in manifest.items():
        file = (folder / name).resolve()
        if file.parent != folder or not file.is_file():
            raise ValueError(f'A saved model file is missing or has an invalid path: {name}')
        if file.stat().st_size != details['bytes'] or _sha256(file) != details['sha256']:
            raise ValueError(f'A model file changed after training: {name}')
    config = json.loads((folder / 'config.json').read_text())
    if config.get('model_type') != 'qwen2':
        raise ValueError('The saved configuration is not the expected Qwen model.')
    if (folder / 'adapter_config.json').exists():
        raise ValueError('This application requires the full model, not a LoRA adapter.')
    return {'folder': str(folder), 'run_id': run_id, 'manifest_sha256': fingerprint,
            'verified_files': len(manifest), 'base_model': BASE_MODEL_ID}


@dataclass
class LocalModel:
    model: object
    tokenizer: object
    device: str
    provenance: dict
    lock: object

    def generate(self, payload):
        import torch
        from official_program import (PROGRAM_ID, OFFICIAL_SYSTEM_PROMPT,
                                      OFFICIAL_PROMPT_VERSION, SNAPSHOT_SHA256)
        official = any(p.get('source_id') == PROGRAM_ID for p in payload.get('program_evidence', []))
        system_prompt = OFFICIAL_SYSTEM_PROMPT if official else SYSTEM_PROMPT
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': json.dumps(payload, ensure_ascii=False)},
        ]
        with self.lock:
            inputs = self.tokenizer.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True,
                return_tensors='pt', return_dict=True,
            ).to(self.device)
            input_tokens = inputs['input_ids'].shape[1]
            if input_tokens > MAX_INPUT_TOKENS:
                raise ValueError('This request is longer than the prototype supports. Shorten the program evidence.')
            if self.device == 'cuda':
                torch.cuda.synchronize()
            elif self.device == 'mps':
                torch.mps.synchronize()
            started = time.perf_counter()
            with torch.inference_mode():
                generated = self.model.generate(
                    **inputs, do_sample=False, max_new_tokens=MAX_NEW_TOKENS,
                    pad_token_id=self.tokenizer.pad_token_id,
                )[0, input_tokens:]
            if self.device == 'cuda':
                torch.cuda.synchronize()
            elif self.device == 'mps':
                torch.mps.synchronize()
            seconds = time.perf_counter() - started
            eos = self.model.generation_config.eos_token_id
            eos = eos if isinstance(eos, list) else [eos or self.tokenizer.eos_token_id]
            stopped = bool(len(generated) and generated[-1].item() in eos)
            return {
                'raw_response': self.tokenizer.decode(generated, skip_special_tokens=True).strip(),
                'input_tokens': int(input_tokens), 'output_tokens': int(len(generated)),
                'seconds': round(seconds, 3),
                'hit_token_limit': len(generated) >= MAX_NEW_TOKENS and not stopped,
                'device': self.device, 'model_run': self.provenance['run_id'],
                'model_manifest_sha256': self.provenance['manifest_sha256'],
                'inference_prompt_version': OFFICIAL_PROMPT_VERSION if official else 'original-training-prompt',
                'inference_prompt_sha256': hashlib.sha256(system_prompt.encode()).hexdigest(),
                'rules_snapshot_sha256': SNAPSHOT_SHA256 if official else None,
            }


def load_saved_model(folder, device_choice='auto'):
    provenance = verify_saved_model(folder)
    # Import the heavier packages only when the saved model is actually requested.
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    if device_choice == 'auto':
        device = ('cuda' if torch.cuda.is_available() else
                  'mps' if torch.backends.mps.is_available() else 'cpu')
    else:
        device = device_choice
    tokenizer = AutoTokenizer.from_pretrained(
        provenance['folder'], local_files_only=True, trust_remote_code=False,
    )
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        provenance['folder'], local_files_only=True, trust_remote_code=False,
        use_safetensors=True, torch_dtype=torch.float32, attn_implementation='sdpa',
    ).to(device)
    model.eval()
    model.config.use_cache = True
    return LocalModel(model, tokenizer, device, provenance, threading.Lock())
