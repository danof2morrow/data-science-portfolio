# Childcare Affordability and Workforce Impact

## Overview

This project explores childcare affordability across the United States and how childcare costs compare with household income.

The analysis focuses on infant and preschool care costs at the county level and uses data visualization to show how affordability varies by location and how those costs can affect working families.

## Analysis

The project includes:

- Data cleaning and preparation
- County- and state-level comparisons
- Household income analysis
- Infant and preschool childcare cost comparisons
- Affordability measures
- Visual storytelling designed for a nontechnical audience

## Tools

- Python
- Pandas
- Matplotlib
- Seaborn
- Jupyter Notebook

## Project Files

- Analysis code — data preparation and visualization
- Final report PDF — completed visual story and findings

## Open the Artifacts

- [childcare_affordability_workforce_impact.ipynb](childcare_affordability_workforce_impact.ipynb)
- [childcare_affordability_workforce_impact_report.pdf](childcare_affordability_workforce_impact_report.pdf)

## Reproduce the Analysis

Use Python 3.11 or newer. From this project folder:

```bash
python -m pip install -r requirements.txt
python download_data.py
python -m jupyterlab
```

Open `childcare_affordability_workforce_impact.ipynb`, restart the kernel, and run all cells in order. No API key is needed. The requirements include openpyxl, which pandas uses to read the Excel workbook.

The data helper retrieves the original **2008-2018** workbook from the [U.S. Department of Labor archive](https://www.dol.gov/agencies/wb/topics/featured-childcare) and checks its SHA-256 digest against the input used in the execution test. It does not substitute the newer 2008-2022 dataset. If an existing or downloaded workbook differs, the helper stops without overwriting the existing input or saving a changed download. If the download is blocked, obtain the archived workbook manually, name it `nationaldatabaseofchildcareprices.xlsx`, place it beside the notebook, and run the helper to verify it.

## Execution Check

On October 25, 2026, all **20 nonempty code cells** completed sequentially in a fresh IPython process using the original workbook. No notebook code, markdown, saved output, or file bytes were changed.

| Measure | Fresh execution result |
|---|---:|
| Original workbook | 34,567 rows; 227 columns |
| Rows after the notebook’s childcare-price missing-value filter | 23,593 |
| Usable counties in the 2018 analysis | 2,360 |
| Median annual two-child cost in 2018 | $14,850.16 |
| Median county-level two-child burden in 2018 | 29.66% of county median household income |
| Change in median two-child cost, 2008-2018 | 25.55% |

The two-child scenario combines one infant and one preschool-aged child in center-based care. The cost and burden statistics are medians across the usable county records, not estimates of an individual family’s spending. Results describe the historical dataset, not current childcare prices.

The [execution record](execution_summary.json) lists tested package versions and input hashes. The test used fresh IPython execution rather than a connected Jupyter kernel, which is restricted in this environment. The workbook is downloaded separately rather than bundled with the repository.


[Portfolio](../../index.html) · [Repository guide](../../README.md)
