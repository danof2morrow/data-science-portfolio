# Validation Record

Checked October 25, 2026. No notebook source, notebook markdown, saved output, report, or presentation was edited. All 14 renamed artifacts retain their original SHA-256 digests; see the [rename record](file-renames.md).

## Execution Method

Noninteractive analyses were checked by executing their saved code cells in order in a fresh Python subprocess from the project directory. A lightweight `display` stand-in was supplied by the external test harness where IPython was unavailable. The charging notebook uses its own display fallback. Matplotlib used a noninteractive backend. This checks sequential Python execution, but is not a full Jupyter UI or notebook-kernel compatibility test. No executed notebook copies replaced the originals.

The environment did not have Jupyter execution packages, IPython, or all project dependencies. Saved output review is separate from a fresh execution result. None of the eight notebooks contains a saved error output; that alone does not establish that a notebook runs from a clean kernel.

| Project | Observed execution result | Required follow-up |
|---|---|---|
| Level 2 charging infrastructure | All 14 nonempty code cells completed successfully using the official composite CSV downloaded by the unmodified code. All nine printed validation checks passed. | Confirm the same run in the intended Jupyter environment. Source data and generated test charts are not added to this commit. |
| Commercial fleet EV suitability | Initial attempt failed because source data was absent. A second attempt with the downloaded Fleet DNA composite file reached `NameError: negative_stop_count is not defined`. | Recover the complete original notebook. Additional state including `model_ready`, model objects, metrics, and plotting imports is referenced without its construction in the saved cells. |
| Dodgers attendance | Stopped at `FileNotFoundError: dodgers-2022.csv`. | Supply the original data and rerun. Use a Matplotlib release supporting `tick_labels`. |
| Childcare affordability | Stopped at `FileNotFoundError: nationaldatabaseofchildcareprices.xlsx`. | Supply the original workbook, install openpyxl if needed, and rerun. |
| Movie success | Stopped at `ModuleNotFoundError: requests`. Three required cleaned CSVs are also absent from the repository. | Install the documented packages, recover the cleaned inputs, and rerun from the documented directory. |
| Movie review sentiment | Stopped at `FileNotFoundError: labeledTrainData.tsv`. | Supply the original labeled reviews and the documented NLP resources, then rerun. |
| EV incentive assistant | Not executed; requires an interactive Gemini API key and external model calls. Saved responses reviewed only. | Run with an authorized account and quota; verify any live incentive claims against their source programs. |
| Lord of the Rings RAG study | Not executed; installs dependencies and retrieves external article/model content. Saved notebook reviewed only. | Run in a compatible connected environment; check retrieval and generated answers. This is a supporting study outside the selected ten entries. |
| Netflix content strategy | Presentation artifact; no notebook in this project. | Review the presentation visually before final submission. |

## What Is and Is Not Confirmed

Artifact integrity, descriptive filenames, repository organization, and local documentation targets were checked. The charging analysis completed a fresh sequential code run. The portfolio does **not** currently satisfy the requirement that every featured notebook has a confirmed successful clean run. Missing original inputs, incomplete saved code, external account requirements, and two planned projects remain explicit completion items.
