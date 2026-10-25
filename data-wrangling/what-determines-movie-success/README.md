# What Determines Movie Success?

## Overview

This project examines factors associated with movie performance by combining and cleaning data from multiple sources.

The goal is to explore how characteristics such as budget, genre, popularity, audience response, and revenue relate to movie success.

## Analysis

The project includes:

- Combining data from multiple sources
- Cleaning and standardizing fields
- Handling missing and inconsistent values
- Transforming variables for analysis
- Comparing movie budgets and revenue
- Examining genre and popularity patterns
- Exploring audience response and ratings

## Tools

- Python
- Pandas
- Jupyter Notebook
- APIs
- Data cleaning and transformation techniques

## Project Files

- Jupyter notebook — data collection, cleaning, integration, and analysis
- Supporting project documentation

## Open the Artifacts

- [what_determines_movie_success.ipynb](what_determines_movie_success.ipynb)

## Reproduce the Analysis

Use Python 3.11 or newer. All three cleaned CSV inputs are included. From this project folder:

```bash
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open `what_determines_movie_success.ipynb`, restart the kernel, and run all cells in order. Preserve this directory layout because the original code loads the flat-file CSV from its parent folder:

- [cleaned_flat_movies.csv](../cleaned_flat_movies.csv) in `data-wrangling/`.
- [cleaned_website_movies.csv](cleaned_website_movies.csv) beside the notebook.
- [cleaned_api_movies.csv](cleaned_api_movies.csv) beside the notebook.

No API key or live website request is needed for this final integration notebook: it loads already-cleaned source snapshots. The original import of requests remains unchanged and is included in the dependencies. The notebook creates or replaces three tables in a local `movies_project.db` file when run.

## Input Recovery

The standalone CSV files were unavailable, but the original `movies_project.db` contained all three cleaned tables. The included CSVs were exported from those tables without dropping columns or changing the analysis:

| Original table | Recovered rows | Columns |
|---|---:|---:|
| movies_flat | 4,799 | 20 |
| movies_website | 50 | 5 |
| movies_api | 188 | 10 |

Recovered CSV values were checked against the database tables after reading them back, treating database NULL and CSV missing values as equivalent and allowing floating-point tolerance of 1e-14. These are recovered snapshots of the stored table values, not byte-for-byte copies of the unavailable original CSV files. Source database and CSV hashes are recorded in [execution_summary.json](execution_summary.json).

## Execution Check and Coverage

On October 25, 2026, all **13 nonempty code cells** completed sequentially in a fresh IPython process. Notebook code, markdown, saved outputs, and file bytes are unchanged. Five charts were produced by the original code.

The left joins retained **4,799 rows**. Only **12 rows** had a matched website worldwide-gross value, and **44 rows** had a matched API popularity value. The source snapshots have different coverage; the joined website and API fields therefore should not be treated as complete across the movie dataset. Budget and revenue analyses use the flat-file fields. The genre plots retain the original splitting logic.

The [execution record](execution_summary.json) contains the tested package versions, dataset hashes, and join counts. The test used fresh IPython execution rather than a connected Jupyter kernel, which is restricted in this environment. Results are historical observations and do not establish causal effects on movie success.


[Portfolio](../../index.html) · [Repository guide](../../README.md)
