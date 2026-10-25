# Validation Record

Checked October 25, 2026. No notebook source, notebook markdown, saved output, report, or presentation was edited. All 14 renamed artifacts retain their original SHA-256 digests; see the [rename record](file-renames.md).

## Execution Method

Noninteractive analyses were checked by executing their saved code cells in order in a fresh Python subprocess from the project directory. A lightweight `display` stand-in was supplied by the external test harness where IPython was unavailable. The charging notebook uses its own display fallback. Matplotlib used a noninteractive backend. This checks sequential Python execution, but is not a full Jupyter UI or notebook-kernel compatibility test. No executed notebook copies replaced the originals.

The initial audit environment did not have Jupyter execution packages, IPython, or all project dependencies. A separate test environment was later prepared for the fleet suitability review. Saved output review is separate from a fresh execution result. None of the ten notebooks contains a saved error output; that alone does not establish that a notebook runs from a clean kernel.

| Project | Observed execution result | Required follow-up |
|---|---|---|
| Level 2 charging infrastructure | All 14 nonempty code cells completed successfully using the official composite CSV downloaded by the unmodified code. All nine printed validation checks passed. | Confirm the same run in the intended Jupyter environment. Source data and generated test charts are not added to this commit. |
| Commercial fleet EV suitability | Restored four intact original cells; all 17 nonempty cells completed in a fresh IPython process on the original 4,705-row input. Both models achieved 95.33% test accuracy. | Follow the project requirements and verified data-download instructions. A full Jupyter kernel connection could not be tested in this environment; see the project execution record. |
| Dodgers attendance | Stopped at `FileNotFoundError: dodgers-2022.csv`. | Supply the original data and rerun. Use a Matplotlib release supporting `tick_labels`. |
| Childcare affordability | Stopped at `FileNotFoundError: nationaldatabaseofchildcareprices.xlsx`. | Supply the original workbook, install openpyxl if needed, and rerun. |
| Movie success | Stopped at `ModuleNotFoundError: requests`. Three required cleaned CSVs are also absent from the repository. | Install the documented packages, recover the cleaned inputs, and rerun from the documented directory. |
| Movie review sentiment | Stopped at `FileNotFoundError: labeledTrainData.tsv`. | Supply the original labeled reviews and the documented NLP resources, then rerun. |
| EV incentive assistant | Not executed; requires an interactive Gemini API key and external model calls. Saved responses reviewed only. | Run with an authorized account and quota; verify any live incentive claims against their source programs. |
| Lord of the Rings RAG study | Not executed; installs dependencies and retrieves external article/model content. Saved notebook reviewed only. | Run in a compatible connected environment; check retrieval and generated answers. This is now a featured project. Saved examples include successful answers and retrieval/generation failures. |
| Fine-tuned DistilBERT sentiment | Final notebook imported unchanged. Saved outputs show completed T4 training, 88.4% test accuracy, macro F1 0.8840, and custom-review failures. No saved exception output. | A fresh GPU run was not repeated. Reproduce using the notebook’s Colab setup; model weights are not bundled. |
| EV incentive assistant full fine-tuning | Latest revised notebook imported unchanged. Saved outputs record 25/28 strict checks, 26/28 correct decisions, and 8/8 usable complete calculation cases. No saved exception output; installation conflicts and one non-finite training metric remain documented. | A fresh Colab/Drive/GPU run was not repeated. Review broader real-world cases and supply current official program sources. |
| Netflix content strategy | Presentation artifact; no notebook in this project. | Review the presentation visually before final submission. |

## What Is and Is Not Confirmed

Artifact integrity, descriptive filenames, repository organization, and local documentation targets were checked. The charging analysis completed a fresh sequential code run. The portfolio does **not** currently satisfy the requirement that every featured notebook has a confirmed successful clean run. Missing original inputs, external account requirements remain explicit completion items. All ten selected project entries now contain artifacts; none is a planning placeholder.

## Portfolio Expansion

The RAG study is now featured. The final IMDb fine-tuning notebook and latest revised incentive-assistant fine-tuning notebook were copied without changes; source and repository SHA-256 digests match. JSON structure and saved results were reviewed. All previously tracked notebooks, reports, and presentations also retain their pre-update bytes. No GPU training was repeated as part of this update.

## API-Key Completion Criterion

At Dan's direction, an API key requirement does not by itself leave a portfolio project unfinished when its code is available in a runnable Python file. The Gemini incentive experiments now have an unchanged-code `.py` export, a terminal launcher, a dependency list, and setup commands. Source-cell equality, Python syntax, and the five-request flow are checked with a simulated client. Live API access is not verified without a key. This criterion applies to the Gemini experiment workflow; it does not establish a fresh run of its separate GPU fine-tuning workflow or resolve missing data and missing definitions elsewhere.

## Fleet Suitability Review Completed

The active notebook now restores four intact original code cells while preserving all pre-existing cell contents and order. The previous incomplete file remains in the project archive. A fresh IPython execution passed all 17 nonempty code cells using the original public input, which matches the official downloadable CSV byte for byte. The setup helper verifies that file’s SHA-256 digest. See the project README, `execution_summary.json`, and `restoration_record.json` for the current result. This supersedes the initial missing-definitions failure. Full Jupyter transport was unavailable in this environment; no notebook source was changed to work around it.
