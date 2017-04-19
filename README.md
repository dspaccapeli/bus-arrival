# Bus arrival time prediction based on historical GPS data.
This repository consists in the code used for a research project for Aalto University regarding the prediction of bus arrival time given historical data.

This project consists in finding a way to predict the arrival time of buses in the Helsinki area given historical GPS data. The collected data is given by the Helsinki Region Transport to try and improve the public service.

This problem is approached using a database containing the data from the first six months of 2016.
The objective is to beat the timetable estimate, on average by _at least one minute_ (we chose to use this time resolution given the timetable reference).

## Preprocessing
This folder contains the Python scripts (the additional SQL queries are omitted) employed to _filter_ and _normalize_ the data and to check for inconsistencies.

_We can see the results of this stage in the following plot:_

<p align="center">
  <img src="/images/dist_plot.png" width="420" height="350">
</p>

## Visualization
Here several variety of scripts for plots are presented. This plots vary from histograms to simil-heatmaps.

_Here some examples:_

<p align="center">
  <img src="/images/vis_delay.png" width="240" height="200">
  <img src="/images/seq_delay_evo.png" width="240" height="200">
</p>

## Predictors
All the methods evaluated for the purpose of the final report are included in this folder. The methods tried include:
- Mean
- Median
- k-Nearest Neighbor
- Multi-layer Perceptron
- Random Forest

## Results

The best performing predictor resulted being the Random Forest. It managed to give the hoped results of improving the result by a whole minute. The result is __meaningful__ considering that the median delay is under two minutes. Here's a table with the related results (the values are to be contextualize relative to their naive result counterpart):


| Number of Estimators | No. 4 | No. 6 | No. 8 | No. 10 | No. 12 |
|----------------------|-------|-------|-------|--------|--------|
| Predictor            | 53.8  | 52.4  | 52.4  | 51.1   | 50.9   |
| Naive                | 116   | 116   | 115   | 116    | 116    |

Given more data, better preprocessing and parameter selection I'm confident the results could be ulteriorly improved.  
