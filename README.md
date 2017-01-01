# Bus arrival time prediction based on historical GPS data.
Research project files at Aalto University (2016) regarding the prediction of bus arrival time given historical data.
##Intro
This project consists in finding a way to predict the arrival time of buses in the Helsinki area given historical GPS data.
This is approached using a database containing the data from the first six months of 2016. 
The objective is to beat the timetable estimate by at least one minute on average (minute given the resolution).
##Preprocessing
This folder contains the python scripts (besides the query used) employed to filter and _normalize_ the data or checking for inconsistencies.
##Visualization
Here several variety of scripts for plots are presented; from simil-heatmaps to histograms.
##Predictors
All the methods tried are in this folder, with the best performing one being the Random Forest that manage to give the hoped results. Here a table with the related results (to be taken relative to their naive result counterpart):
| Number of Estimators | No. 4 | No. 6 | No. 8 | No. 10 | No. 12 |
|----------------------|-------|-------|-------|--------|--------|
| Predictor            | 53.8  | 52.4  | 52.4  | 51.1   | 50.9   |
| Naive                | 116   | 116   | 115   | 116    | 116    |
