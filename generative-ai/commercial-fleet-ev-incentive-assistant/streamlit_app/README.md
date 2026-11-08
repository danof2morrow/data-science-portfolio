# Commercial Fleet EV Incentive Assistant

Dan Morrow · Bellevue University · DSC670 final project

The application uses the fully fine-tuned Qwen model saved in Milestone 3. Its
default workflow reviews fictional fleet customers against the official DTE
eFleet Level 2 program. The earlier fictional program cases remain available in
the sidebar for comparison.

## Official program scope

The [DTE program page](https://www.dteenergy.com/us/en/business/service-request/pev/efleet-charger-rebate.html)
and its linked [eFleet Charger Rebate Agreement](https://www.dteenergy.com/content/dam/dteenergy/deg/website/business/service-request/pev/efleet-charger-rebate/eFleetChargerRebateAgreement.pdf)
were reviewed November 8, 2026. The agreement is revised September 2026.
`official_program.py` contains the dated, paraphrased rules snapshot. The source
receipt records the reviewed document URLs and hashes; the program websites can
change after this review.

For Level 2, the published maximum is $2,500 per port. Electric Choice customers
receive 35% of that established amount, or $875 per port. DTE sets site and
participant limits at its discretion. This workflow therefore reports a
**published per-port ceiling before DTE caps and review**, rather than an approved
rebate or complete award estimate. It does not invent a cost-percentage limit,
a fixed site cap, or a universal approval-before-purchase condition.

The intake covers the DTE account and service territory, site rights, qualifying
vehicles, equipment, ongoing commitments, the meter/network alternative,
applicable grid requirements, confirmed ports, Electric Choice status, and
review of the full agreement and documentation obligations. These are supplied
planning facts, not independent utility verification. Final documentation,
compliance, funding, caps, and award review remain with DTE.

The model sees the facts and reviewed evidence. Python independently checks the
planning requirements and compares the proposed handoff with those facts before
multiplying ports by the applicable published rate. The original model response
stays visible when it is incorrect. The app does not search for other programs,
verify funding, determine real-world eligibility, or submit applications.

## Run locally

Use the existing `dsc670_app` environment, or a separate Python 3.11 environment.
From this folder:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The interface opens at `http://localhost:8501`. Select the saved `full_model`
folder in the sidebar and load it. Model reviews stay disabled until it loads.
No pretrained-model substitute is downloaded.

## Saved model

Use the completed artifact from run `4ec6c67be487`. Keep these together:

```text
completed_training_run/
    full_model/
    reports/recipe.json
    model_manifest.json
    training_complete.json
```

The source package does not contain the approximately 2 GB model. The application
verifies its file hashes, manifest fingerprint, and training recipe. Existing
weights are reused; no training is performed by the app. Device selection uses
CUDA, Apple MPS, or CPU in that order.

The training prompt and weights are unchanged. Official-program mode uses a
separately versioned inference prompt to apply the real evidence and permit null
values for the three unsupported cost/cap fields. Each live review records the
training run, manifest, inference prompt, and rules-snapshot identities.

## Evaluation

The historical synthetic notebook recorded 25/28 strict checks and 26/28 correct
decisions. These are not DTE-program performance results.

On **Run example checks**, select **Run all six examples** after loading the model.
The app runs complete, incomplete, Electric Choice, and wrong-utility cases and
exports `official_program_live_checks.json`. Authored expected answers are used
only after generation. They are not model inputs. The report preserves model
errors, calculation blocks, timing, tokens, and provenance. Six demonstration
cases do not establish independent real-world accuracy. Explanations need manual
review even when structured checks pass.

The same live checks can be run from the terminal:

```bash
python official_checks.py --model-dir "/path/to/completed_training_run/full_model"
```

Rule and failure-handling tests can be run without the model:

```bash
python -m unittest -v test_incentive_logic.py test_official_program.py
```

These tests use explicit authored fixtures. They do not measure model performance.

## First official-program live run

The first six-case run used the saved model on Mac MPS. All six responses parsed,
but none passed the strict workflow checks and no calculation handoff was
produced. Three decision labels matched; two of those clarifications asked about
cost rather than the actual missing requirement. The port-confirmation question
was relevant but did not match the exact field-name criterion. The model also
missed a confirmed utility mismatch and added unsupported conditions.

The current inference prompt adds four worked examples with different customer
facts. It leaves the weights, rules, and six development cases unchanged. A new
live run is required before claiming an improvement. The original prompt is
retained in `source_review/prompt_v1.txt`; the first report and manual review are
retained in the project repository.

## Files

- `app.py`: Streamlit entry point and shared result display.
- `official_ui.py`: official-program intake, source view, and live test controls.
- `official_program.py`: dated rules, inference prompt, and fictional cases.
- `official_checks.py`: live-model checks and downloadable report.
- `incentive_logic.py`: strict response parsing and independent calculations.
- `model_runtime.py`: saved-artifact verification and local generation.
- `training_contract.py`: unchanged training prompt and run identity.
- `example_cases.py`: retained fictional scenario generator.
- `test_incentive_logic.py`, `test_official_program.py`: code-level checks.

## Data and privacy

Use fictional customer information for the course demonstration. Inference uses
local model files, and customer entries remain in the current Streamlit session
unless a review is downloaded. There is no hosted model API call, authentication,
or production privacy control. The app is intended for local use.
