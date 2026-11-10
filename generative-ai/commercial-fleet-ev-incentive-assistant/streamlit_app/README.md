# DTE eFleet Streamlit Application

Dan Morrow, DSC670 final project

## Model and scope

This application uses the full Qwen2.5-0.5B-Instruct model from DTE training run `1bcf2a3b1d8e`. It uses a dated DTE eFleet Level 2 rules snapshot, reviewed November 8, 2026. Customer examples are fictional. The application does not perform live incentive searches or independently confirm customer eligibility or funding.

## Local setup

Keep the completed training bundle together: `app/`, `full_model/`, `reports/recipe.json`, `model_manifest.json`, and `training_complete.json`. The saved bundle is named `DSC670_DTE_Complete_1bcf2a3b1d8e.zip`. Model weights are separate from this source package and from GitHub.

From the extracted completed-model bundle:

```bash
python -m pip install -r app/requirements.txt
python -m streamlit run app/app.py --server.port 8502
```

Open http://localhost:8502 and select **Load saved model**. The app discovers the adjacent `full_model` folder. Verify run `1bcf2a3b1d8e` in the sidebar. The loader checks the recipe and saved file hashes before inference. The training notebook can reproduce a model bundle in Google Colab with a compatible GPU and Google Drive.

When using only this repository's `streamlit_app` directory, run `python -m streamlit run streamlit_app/app.py` from the project directory and select the existing completed bundle's `full_model` path in the sidebar. A source-only checkout cannot perform inference without the saved weights and their sibling metadata.

## Recorded results

The authored 64-case notebook test passed all decision and structured checks. On six live app examples, the same model matched 5/6 decisions and passed 5/6 structured checks. Manual review found appropriate explanations in 4/6 cases. Electric Choice was incorrectly rejected, and the different-utility case used the correct label with an incorrect uptime explanation. CPU reproduced the MPS responses exactly. The independent Python decision check flagged the Electric Choice disagreement, but a matching decision label did not expose the different-utility explanation error.

For the standard complete example, Python calculated a $40,000 published ceiling from 16 ports at $2,500 per port. The Electric Choice reference ceiling is $14,000 at $875 per port, but the live model failed to supply that handoff. DTE caps, documentation, compliance and funding review can reduce or prevent an award. The app does not apply the earlier fictional cost-percentage limit or fixed program cap.

## Files

`app.py` launches Streamlit. `official_ui.py` provides the DTE intake and example checks. `model_runtime.py` verifies and loads the saved model. `training_contract.py` identifies its run and inference instructions. `official_program.py` contains the dated rules and independent checklist. `incentive_logic.py` validates responses and calculation inputs. `official_checks.py` records live inference and checks report provenance. The retained example and test modules also document the earlier fictional workflow.

Run the rule and response-validation tests with `python -m unittest discover -s app -p 'test_*.py'` from the completed bundle. These code tests do not measure model accuracy. Review the raw model explanations alongside the independent planning checklist.
