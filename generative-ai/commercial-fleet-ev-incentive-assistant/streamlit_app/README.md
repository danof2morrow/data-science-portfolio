# Commercial Fleet EV Incentive Assistant

Dan Morrow · Bellevue University · DSC670 final project

This Streamlit prototype reviews a fictional fleet charging project against supplied
program evidence. It uses the full Qwen model fine-tuned in Milestone 3 to explain
the next step and prepare calculation inputs. Python independently checks those
inputs and applies the program formula. The application does not discover current
incentives, establish eligibility, or guarantee an award.

## Run locally

Use Python 3.11 or 3.12 in a separate environment. From this app folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The app opens at `http://localhost:8501`. It can display the project form without
the model, but reviews remain disabled until the saved fine-tuned model loads.
The original base model is never downloaded as a substitute.

## Connect the trained model

Milestone 3 saved this file in Google Drive:

`DSC670_Milestone3_Full_Fine_Tuning/4ec6c67be487/DSC670_Milestone3_Complete_4ec6c67be487.zip`

Download and extract that existing ZIP. Keep its folders together:

- `full_model/`: the saved model weights, tokenizer, and configuration
- `reports/recipe.json`: the original model and training instructions
- `model_manifest.json`: recorded sizes and hashes for the saved model files
- `training_complete.json`: the training-completion record

In the app sidebar, enter the path to the extracted `full_model` folder and choose
**Load saved model**. Alternatively, set the `DSC670_MODEL_DIR` environment
variable to that folder before starting the app. Keep the rest of the extracted
run beside it. Merely renaming a base-model folder will not pass verification.

The source package does not include the roughly 2 GB of trained weights. The
notebook contains their saving code and evaluation results, rather than embedding
the weights themselves. No additional training is needed when that ZIP is intact.

Automatic device selection uses CUDA, Apple MPS, or CPU in that order. Inference
can run on a computer without the T4 used for training, provided there is enough
memory. CPU generation can take longer. Select CPU explicitly if MPS is
unavailable or unsupported. The app retains the notebook's float32 model loading,
greedy decoding, and 384-token output limit.

## Demonstration workflow

Choose an example, review its project facts and evidence, and submit it to the
loaded model. Useful examples include a complete utility project, a missing port
count, unconfirmed eligible costs, and conflicting program sources. Example
projects come from the submitted notebook's fictional test scenarios. The model
receives only their inputs, never their authored target answers.

The result separates the model's proposed decision from Python's acceptance or
rejection of a calculation. An accepted estimate is the minimum of the per-port
allowance, eligible-cost percentage, and program cap. Raw JSON, source IDs,
request timing, and the submitted facts are available for inspection. Results
refer to the last submitted request, rather than unsent form changes.

No customer information is sent to a hosted model API. Requests remain in the
current Streamlit session unless the user downloads a review. This is a course
prototype using fictional data, not a deployed service with authentication or
production privacy controls. Run it locally and do not expose the port publicly.

## Recorded model evaluation

The submitted Milestone 3 notebook reported 25/28 strict checks, 26/28 correct
decisions, and usable inputs for all 8 complete calculation cases after training.
There was still one incorrect ready decision, and manual review found explanation
errors that structured checks did not catch. These are historical notebook
results, not a new accuracy claim for arbitrary app inputs.

## Code checks

```bash
python -m unittest -v test_incentive_logic.py
```

These tests check program limits and failure handling using authored examples.
They do not evaluate the fine-tuned model. Live inference and screenshots require
the actual saved artifact.

## Files

- `app.py`: Streamlit form, results, source evidence, and evaluation display
- `model_runtime.py`: saved-model verification, local loading, and generation
- `incentive_logic.py`: response validation and independent calculator
- `training_contract.py`: the exact system prompt and expected training identity
- `example_cases.py`: the notebook's fictional scenario generator
- `test_incentive_logic.py`: calculator and response-validation checks

## Live application results

The accompanying screenshots and downloaded JSON reviews show the saved model
running on Apple MPS. The complete project produced a conditional $10,800
estimate. In the unconfirmed-cost case, the model incorrectly proposed a
calculation, and Python blocked it. The conflicting-source case returned no
calculation inputs and asked which program version was authoritative.

These three examples demonstrate the application workflow using fictional
scenarios from the notebook. They are not an independent accuracy evaluation.

## Technical references

- [Streamlit caching](https://docs.streamlit.io/develop/concepts/architecture/caching)
- [Hugging Face model loading](https://huggingface.co/docs/transformers/v4.57.1/main_classes/model)

The model results and example data come from the submitted Milestone 3 notebook.
