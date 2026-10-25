# Dodgers Attendance and Promotion Strategy

## Overview

This project analyzes Los Angeles Dodgers game attendance to understand which factors are associated with higher turnout and how promotional events may influence attendance.

The goal is to turn those patterns into a practical recommendation for future promotional planning.

## Analysis

The project examines factors such as:

- Day of the week
- Opponent
- Weather and temperature
- Promotional events
- Attendance patterns across games
- The effect of bobblehead promotions

## Key Finding

Bobblehead promotions showed the strongest relationship with higher attendance in the analysis.

The project recommends using bobblehead promotions strategically when the goal is to increase game attendance.

## Tools

- Python
- Pandas
- Matplotlib
- Jupyter Notebook
- Exploratory data analysis

## Project Files

- Jupyter notebook — complete attendance analysis and recommendation

## Open the Artifacts

- [dodgers_attendance_promotion_strategy.ipynb](dodgers_attendance_promotion_strategy.ipynb)

## Reproduce the Analysis

The original [81-game dataset](dodgers-2022.csv) is included beside the notebook, so no API key or external data download is needed. Use Python 3.11 or newer. From this project folder:

```bash
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open `dodgers_attendance_promotion_strategy.ipynb`, restart the kernel, and run all cells in order. The requirements include a Matplotlib version supporting the notebook’s `boxplot(tick_labels=...)` argument.

The input filename remains `dodgers-2022.csv` because that is the exact name used by the original code. The CSV has no year column; the notebook constructs dates using 2012 and joins a supplemental 2012 giveaway schedule. This behavior is documented rather than changing the filename or code.

## Execution Check

On October 25, 2026, all **12 nonempty code cells** completed sequentially in a fresh IPython process using the included **81-game dataset**. All **11 bobblehead games** matched a supplemental giveaway name. The notebook code, markdown, saved outputs, and file bytes are unchanged.

The fresh run reproduced these rounded attendance averages:

| Game group | Average attendance |
|---|---:|
| With bobblehead promotion | 53,145 |
| Without bobblehead promotion | 39,138 |

These are observed associations, not evidence that the promotion alone caused the attendance difference. Opponent, scheduling, and other factors can also matter.

The [execution record](execution_summary.json) contains package versions, input hashes, and promotion comparisons. The test used fresh IPython execution rather than a connected Jupyter kernel, which is restricted in this environment. The original reference notebook was also located, but no replacement or restoration was necessary for this project.


[Portfolio](../../index.html) · [Repository guide](../../README.md)
