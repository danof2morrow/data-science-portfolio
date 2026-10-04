# Commercial Fleet EV Suitability Prediction

## Overview

This project examines commercial fleet operating data to identify vehicles with usage patterns that may be better suited for electrification.

Rather than treating fleet electrification as an all-or-nothing decision, the analysis focuses on prioritization: which vehicles should a fleet evaluate first?

The project uses real-world operating data from the National Renewable Energy Laboratory's Fleet DNA dataset and applies feature engineering and machine learning to classify vehicle operating patterns.

## Business Problem

Commercial fleets often contain vehicles with very different duty cycles. Some operate predictable local routes with manageable daily mileage and regular downtime, while others travel farther or have operating patterns that may make electrification more difficult.

The goal of this project is to provide an initial screening tool that helps fleet managers identify vehicles that deserve a closer look for electric replacement.

## Data

The primary dataset is the National Renewable Energy Laboratory's Fleet DNA dataset.

The analysis includes:

- 4,705 vehicle-day records
- 486 unique vehicles
- 57 fleet deployments
- Vehicle class and vocation information
- Daily mileage
- Driving duration
- Average speed
- Trip and stop activity
- Zero-speed time

## Methods

The project includes:

- Data cleaning and validation
- Exploratory data analysis
- Feature selection and engineering
- Development of an operational EV suitability target
- Decision tree classification
- Random forest classification
- Model comparison and evaluation
- Feature importance analysis
- Business interpretation of model results

The suitability target was created from operational characteristics such as daily mileage, driving time, average speed, stop activity, and route behavior.

## Key Findings

The analysis shows that fleet electrification should be approached as a prioritization problem rather than assuming every vehicle is equally suited for electric replacement.

Average speed, stop activity, and daily distance were among the most important operational characteristics associated with the suitability classification.

The random forest provided the strongest overall predictive performance, while the decision tree provided a more interpretable view of the classification logic.

These results are intended to support an initial screening process rather than serve as a final vehicle-purchase recommendation.

## Tools

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

## Limitations

The model predicts an analyst-defined operational suitability classification rather than actual future EV performance or deployment success.

Important factors such as vehicle purchase cost, charging infrastructure, electrical capacity, incentives, maintenance costs, route reliability, and real-world EV energy consumption are outside the scope of this model.

A fleet should use the results as the first stage of a broader electrification assessment.

## Repository Files

- `commercial_fleet_ev_suitability.ipynb` — complete analysis, modeling, and results
- Final project report PDF — detailed project documentation and findings

## Next Step

Vehicles identified as stronger operational candidates should move into a more detailed assessment that includes charging requirements, infrastructure costs, vehicle-specific energy use, and site conditions.
