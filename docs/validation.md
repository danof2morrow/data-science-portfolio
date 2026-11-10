# Portfolio Validation Record

Initial review October 25, 2026; incentive Streamlit evidence updated November 9, 2026. All ten featured entries contain artifacts. Original code, saved outputs, reports, and presentations were preserved. The fleet suitability notebook restores four intact original cells; its previous incomplete version is archived. See [artifact provenance](file-renames.md).

| Project | Current result | Details |
|---|---|---|
| Level 2 charging infrastructure | All 14 nonempty cells completed; nine validation checks passed in the initial execution audit. | [Setup and execution record](../applied-data-science/level2-charging-infrastructure-planning/README.md) |
| Fleet EV suitability | All 17 nonempty cells passed after restoring original steps. Both models reached 95.33% accuracy on the defined suitability label. | [Setup and provenance](../predictive-analytics/commercial-fleet-ev-suitability/README.md) |
| Dodgers attendance | All 12 nonempty cells passed on 81 games; all 11 bobblehead games matched their supplemental names. | [Included input and execution record](../business-analytics/dodgers-attendance-promotion-strategy/README.md) |
| Childcare affordability | All 20 nonempty cells passed with the original workbook; 2,360 counties were usable in 2018. | [Verified download and execution record](../data-visualization-storytelling/childcare-affordability-workforce-impact/README.md) |
| Movie success | All 13 nonempty cells passed using recovered CSVs; 4,799 joined rows, 12 website and 44 API matches. | [Included snapshots and coverage limits](../data-wrangling/what-determines-movie-success/README.md) |
| TextBlob/VADER sentiment | All 12 nonempty cells passed on 25,000 reviews. Saved accuracy scores and feature dimensions matched exactly. | [Verified setup and execution record](../natural-language-processing/movie-review-sentiment-analysis/README.md) |
| Lord of the Rings RAG | All 12 runtime cells passed on CPU, including retrieval, generation, and the original interactive loop. Installation completed separately. | [Tested dependencies and execution record](../generative-ai/lord-of-the-rings-rag/README.md) |
| EV incentive assistant | DTE full model run 1bcf2a3b1d8e completed in Colab. Notebook outputs record 64/64 authored decision and structured checks. Actual Mac MPS and CPU runs matched 5/6 live decisions, with appropriate explanations in 4/6 cases. Twenty-one rule/response tests passed. | [Source, results and limitations](../generative-ai/commercial-fleet-ev-incentive-assistant/README.md) |
| Fine-tuned DistilBERT | All 11 code cells passed syntax checks. Retained Colab results show 88.4% test accuracy and macro F1 0.8840; no saved exception outputs. | [Colab instructions and review record](../natural-language-processing/fine-tuned-movie-review-sentiment/README.md) |
| Netflix content strategy | 13 slides and 14 embedded images checked; ZIP integrity and all internal relationships passed. Slide text and embedded images inspected. | [Presentation and review record](../data-visualization-storytelling/netflix-top10-content-strategy/README.md) |

## Execution Methods and Limits

Fresh execution used original code cells in order, generally in a new IPython process. The initial charging run used a Python subprocess with the notebook's own display fallback. The RAG package install ran separately, and the unchanged interactive cell received scripted question/exit input. Executed copies did not replace source notebooks.

A connected Jupyter kernel transport was unavailable here. Sequential IPython checks test execution and state dependencies, but do not certify the Jupyter UI. Syntax checks transform notebook magics with IPython before parsing; they are not equivalent to training.

Dan accepts an API-key requirement when a runnable Python file and instructions exist. The Gemini export matches the original notebook code. Its simulated five-request run checked readable output and original rebate arithmetic. A live request was not made; account, model access, and quota are still needed to run it.

Both training notebooks require a CUDA GPU; the incentive notebook also mounts Google Drive. Their retained completed Colab results and source syntax were reviewed. Fresh GPU training was **not repeated** in this CPU environment. The incentive notebook's original data-generation and scoring/calculator cells were executed independently: splits were 168/28/28, altered port counts were rejected, and the $6,000 arithmetic fixture passed. These test the evaluation code, not new model performance.

## Provenance and Interpretation

The movie CSVs were recovered from the original database, with value/missingness and floating-point checks; they are not claimed as byte-identical originals. The sentiment TSV uses a pinned public mirror matching saved IDs, label counts, scores, and dimensions; the original local TSV was unavailable for byte comparison.

RAG and incentive failures remain visible. A successful execution does not guarantee accurate model answers. The incentive prototype uses fictional program evidence, not current eligibility rules.

Netflix slide text and embedded images were reviewed, but full PowerPoint/LibreOffice layout and font rendering were unavailable. The source presentation is unchanged.

There are no remaining known missing-input or missing-definition blockers in the active featured analyses. This record does not claim fresh runs of the two GPU training workflows or live Gemini access.


## Historical Fictional-Program Application Evidence — November 8, 2026

The earlier fictional-program demonstration included its [Streamlit source](../generative-ai/commercial-fleet-ev-incentive-assistant/streamlit_app/), four actual running-application screenshots, a presentation, and three downloaded JSON reviews. The reviews identify model run `4ec6c67be487` and the same manifest fingerprint. Inference ran on Dan's Mac using MPS, not in the CPU review workspace.

The complete project produced a conditional $10,800 estimate. With unconfirmed eligible costs, the model incorrectly proposed a calculation; the independent Python check blocked it. Conflicting program evidence prompted an authoritative-source question and no calculation inputs. These are demonstrations using the existing fictional scenario generator, not an additional independent model accuracy test.

Eight unit tests passed for response validation, program limits, confirmation checks, purchase timing, conflicting evidence, and malformed input. Streamlit startup and missing-model behavior were also checked. Those code checks do not prove the model's explanations are accurate. The original Gemini API workflow remains a separate historical experiment; no new live Gemini call or GPU training is claimed.

The presentation has eight slides with speaker notes. Its package/layout checks passed and the rendered slides were visually reviewed. Native PowerPoint execution was not tested. Saved model weights remain separate; local inference requires the completed Milestone 3 artifact. GitHub Pages is the portfolio, not a hosted model endpoint.


## Final DTE Application Evidence — November 9, 2026

The [executed DTE notebook](../generative-ai/commercial-fleet-ev-incentive-assistant/commercial_fleet_ev_incentive_assistant_dte_full_fine_tuning.ipynb) records a new full fine-tuning run, `1bcf2a3b1d8e`, with 320/64/64 authored training/validation/test cases, four epochs, 160 optimizer steps and 32.3 minutes on a Tesla T4. All 494,032,768 parameters were trainable. Saved-file verification and finite-weight checks passed. The selected checkpoint subsequently generated 64/64 matching decisions and structured checks, including 24/24 ready handoffs. Validation token accuracy is a separate metric. The 64 cases comprise four project groups with 16 related variants each and share authored scenario templates with training.

The actual Mac [MPS](../generative-ai/commercial-fleet-ev-incentive-assistant/evaluation/dte_live_checks_mps.json) and [CPU](../generative-ai/commercial-fleet-ev-incentive-assistant/evaluation/dte_live_checks_cpu.json) reports identify the same new model manifest, prompt and rules snapshot. The matching application verifier reproduced both reports from raw responses. CPU and MPS generated identical answer text across all six cases. Each report matched 5/6 decision labels and 5/6 structured workflows. Manual review of all six explanations found 4/6 appropriate responses. Electric Choice received an incorrect rejection that Python flagged. Different utility received the correct label with the wrong explanation, which the label comparison missed. These six cases are development examples, not a new independent accuracy sample.

Three actual application screenshots match the individual downloaded JSON reviews. The complete standard case produced a $40,000 published ceiling, the missing meter/network case asked for clarification, and Electric Choice exposed an incorrect rejection. These replace the fictional examples in the current eight-slide presentation. Original model outputs remain available. Python checks supplied facts and calculation inputs but does not independently verify customer statements or every explanation.

All 21 retained rule/response tests passed against the final exported source. All 13 executed notebook code cells have recorded execution counts and no saved exception outputs. The current notebook keeps the actual Colab outputs and adds a Markdown assessment of later live results without altering executable code. The DTE source snapshot documents the September 2026 agreement and its November 8 review. Full model weights stay in the separate completed bundle and are not in GitHub. This review did not repeat GPU training or model inference in the CPU workspace. GitHub Pages hosts the portfolio, not the model endpoint.
