# Portfolio Validation Record

Reviewed October 25, 2026. All ten featured entries contain artifacts. Original code, saved outputs, reports, and presentations were preserved. The fleet suitability notebook restores four intact original cells; its previous incomplete version is archived. See [artifact provenance](file-renames.md).

| Project | Current result | Details |
|---|---|---|
| Level 2 charging infrastructure | All 14 nonempty cells completed; nine validation checks passed in the initial execution audit. | [Setup and execution record](../applied-data-science/level2-charging-infrastructure-planning/README.md) |
| Fleet EV suitability | All 17 nonempty cells passed after restoring original steps. Both models reached 95.33% accuracy on the defined suitability label. | [Setup and provenance](../predictive-analytics/commercial-fleet-ev-suitability/README.md) |
| Dodgers attendance | All 12 nonempty cells passed on 81 games; all 11 bobblehead games matched their supplemental names. | [Included input and execution record](../business-analytics/dodgers-attendance-promotion-strategy/README.md) |
| Childcare affordability | All 20 nonempty cells passed with the original workbook; 2,360 counties were usable in 2018. | [Verified download and execution record](../data-visualization-storytelling/childcare-affordability-workforce-impact/README.md) |
| Movie success | All 13 nonempty cells passed using recovered CSVs; 4,799 joined rows, 12 website and 44 API matches. | [Included snapshots and coverage limits](../data-wrangling/what-determines-movie-success/README.md) |
| TextBlob/VADER sentiment | All 12 nonempty cells passed on 25,000 reviews. Saved accuracy scores and feature dimensions matched exactly. | [Verified setup and execution record](../natural-language-processing/movie-review-sentiment-analysis/README.md) |
| Lord of the Rings RAG | All 12 runtime cells passed on CPU, including retrieval, generation, and the original interactive loop. Installation completed separately. | [Tested dependencies and execution record](../generative-ai/lord-of-the-rings-rag/README.md) |
| EV incentive assistant | API workflow meets Dan's key/setup criterion: runnable unchanged Python export, launcher, and simulated five-request check. Full fine-tuning syntax and saved run reviewed; original data-generation/scoring cells passed freshly. | [API and Colab instructions](../generative-ai/commercial-fleet-ev-incentive-assistant/README.md) |
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
