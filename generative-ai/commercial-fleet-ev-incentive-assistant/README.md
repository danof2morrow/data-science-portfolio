# Commercial Fleet EV Incentive Assistant

## Business Problem

Fleet charging incentive information is scattered, eligibility depends on customer and project details, and a plausible estimate can be misleading when required information is missing. This prototype explores an assistant that asks for clarification, follows supplied program rules, and passes confirmed inputs to Python for calculations.

## Project Development

The [prompt-engineering notebook](commercial_fleet_ev_incentive_assistant.ipynb) and [initial report](commercial_fleet_ev_incentive_assistant_report.pdf) retain the original Gemini-based experiments. The [full fine-tuning notebook](commercial_fleet_ev_incentive_assistant_fine_tuning.ipynb) extends the same project with Qwen2.5-0.5B-Instruct training and before-and-after response evaluation. These stages belong to one portfolio project.

The fine-tuning stage uses fictional customer cases and supplied fictional program evidence. It separates 168 training, 28 validation, and 28 test examples, checks split separation, and makes all 494,032,768 parameters available for updates. The response schema includes the next decision, missing information, questions, calculation inputs, caveats, and source IDs. Python separately checks whether proposed calculation inputs are supported before calculating an estimate.

## Saved Evaluation Results

| Measure | Original model | Fine-tuned model |
|---|---:|---:|
| Strict response checks passed | 0/28 | 25/28 (89.3%) |
| Correct decision | 6/28 | 26/28 (92.9%) |
| Complete calculation cases with usable inputs | 0/8 | 8/8 |
| Incorrect ready-for-calculation decisions | 12 | 1 |

All 28 fine-tuned responses followed the required JSON structure. The remaining incorrect calculation-ready response used an unconfirmed eligible cost; the independent calculator rejected it. Manual review also found an inaccurate explanation that passed the strict checks. The phrase-based wording check flagged no responses and missed that error.

These are the retained results in the latest revised notebook, not a new training run. Training completed three epochs and 63 optimizer steps. A non-finite metric was logged during training; the selected weights passed finite-value checks. The training record preserves that issue rather than claiming an entirely clean run.

## Reproduce

For the prompt-engineering notebook, use a Jupyter environment with `google-genai` and IPython. Supply your own Gemini API key interactively; model access, quota, and internet access are required.

For full fine-tuning, open the newer notebook in Google Colab with a Tesla T4 or compatible CUDA GPU. Run its package setup and connect your own Google Drive when prompted. The notebook checks persistent storage, trains or reuses a matching run, and saves model weights and evaluation files to Drive. Its original internal folder names remain unchanged. The model weights and saved ZIP are not included in this repository.

## Status and Limitations

**Evaluated prototype; further development remains.** The model is tested on a small synthetic dataset with repeated patterns. Token accuracy is not complete-answer accuracy, strict checks do not validate every explanation, and fictional program evidence does not establish real incentive availability or eligibility. This version does not search current program websites. A finished assistant needs current official sources, broader customer testing, and manual verification of its interpretations.

Both notebooks and the report are preserved without content changes. See the [validation record](../../docs/validation.md) for fresh-run limits.

[Portfolio](../../index.html) · [Repository](../../README.md)
