# Level 2 Charging Infrastructure Planning

## Overview

This project evaluates whether commercial fleet vehicles identified as stronger candidates for electrification can be supported using Level 2 charging at private fleet depots.

The analysis moves beyond vehicle suitability and focuses on the infrastructure side of fleet electrification: daily energy demand, charging power, available charging time, required charger ports, and estimated installation costs.

## Business Problem

Selecting vehicles for electrification is only part of the decision. A fleet also needs to understand whether its charging infrastructure can support those vehicles without overbuilding the site or creating operational problems.

This project provides an early planning framework for estimating Level 2 charging requirements before a fleet moves into detailed site engineering.

## Data

The analysis uses commercial fleet operating data from the National Renewable Energy Laboratory's Fleet DNA dataset.

The primary analysis includes:

- 4,705 vehicle-day records
- 486 vehicles
- 57 fleet deployments
- A primary cohort of 373 operationally suited vehicles
- 53 deployments represented in the primary cohort

Additional assumptions and reference values are informed by AFLEET and Alternative Fuels Data Center resources.

## Methods

The project includes:

- Fleet operating data cleaning and validation
- Operational suitability screening
- Vehicle-level and deployment-level aggregation
- 90th percentile daily mileage for planning demand
- Estimated EV energy consumption by vehicle class
- Charging-efficiency adjustments
- Level 2 charging scenarios at 7.2, 11.5, and 19.2 kW
- Charging windows of 8, 10, and 12 hours
- Charger-port requirement calculations
- Infrastructure feasibility screening
- Low, typical, and high installation cost scenarios
- Sensitivity analysis for changes in energy demand

This is a deterministic scenario model rather than a predictive machine learning model. The goal is to compare planning assumptions consistently rather than predict a single future outcome.

## Key Findings

At the 10-hour baseline charging window, 34 of the 53 primary deployments were feasible using the tested Level 2 configurations.

Among the feasible deployments:

- 26 required 19.2 kW charging
- 5 were feasible at 11.5 kW
- 3 were feasible at 7.2 kW
- The median requirement was 2 charger ports
- The median typical estimated upfront infrastructure cost was approximately $15,000

Charging power had a larger effect on feasibility than extending the charging window within the tested 8-to-12-hour range.

The results also showed that some deployments remain difficult to support with Level 2 charging alone, particularly when daily energy demand is high.

## Tools

- Python
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook

## Limitations

This analysis is intended for early-stage planning and is not a substitute for site engineering.

Important site-specific information such as electrical service capacity, parking layout, trenching requirements, construction conditions, utility upgrades, and actual vehicle arrival and departure times were not available.

Installation costs are therefore presented as planning ranges rather than project quotes.

DC fast charging is outside the scope of this analysis.

## Repository Files

- `level2_charging_infrastructure_planning.ipynb` — complete analysis, scenario modeling, sensitivity testing, and results
- `level2_charging_infrastructure_planning_report.pdf` — final project report and detailed findings

## Practical Use

The framework can help a fleet identify which depots appear supportable with Level 2 charging and which locations need additional investigation.

Deployments that pass the screening can move into more detailed site assessment, while constrained sites may require changes such as longer charging windows, managed charging, staggered schedules, or additional electrical planning.
