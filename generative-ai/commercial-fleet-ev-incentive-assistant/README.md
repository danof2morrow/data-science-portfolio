# Commercial Fleet EV Incentive Assistant

## Project Status

In progress.

## Overview

This project is exploring how generative AI can support commercial fleet customers who are trying to understand electric vehicle and charging incentive opportunities.

The current work focuses on prompt engineering, model behavior, controlled calculations, and retrieval-supported workflows. The project will continue to evolve as additional testing, validation, and implementation work is completed.

## Current Focus

The project currently includes:

- Prompt engineering experiments
- Testing how the model handles missing information
- Controlled incentive calculations
- Evaluation of model responses and failure cases
- Planning for retrieval-supported access to changing incentive information

## Tools

- Python
- Jupyter Notebook
- Large language models
- Prompt engineering
- Retrieval-supported workflow design

## Next Steps

Future work will focus on improving model behavior, expanding incentive data coverage, strengthening validation, and developing a more complete customer-facing workflow.

## Open the Artifacts

- [commercial_fleet_ev_incentive_assistant.ipynb](commercial_fleet_ev_incentive_assistant.ipynb)
- [commercial_fleet_ev_incentive_assistant_report.pdf](commercial_fleet_ev_incentive_assistant_report.pdf)

## Reproduce the Analysis

Use a Jupyter environment with `google-genai` and IPython. The notebook prompts for a Gemini API key and makes external model calls. Supply your own authorized key interactively; do not commit it. Model access, quota, and network connectivity are required. Saved outputs do not verify current incentive information.

Open Jupyter from this project folder and restart the kernel before running all cells in order. Original source data is not bundled in this repository. See [validation status](../../docs/validation.md) for the current execution limits. Existing code, markdown, and saved outputs in the notebook are preserved.

[Portfolio](../../index.html) · [Repository guide](../../README.md)
