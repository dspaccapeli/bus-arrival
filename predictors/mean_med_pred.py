#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Description:
  Test the mean and median predictor and
  print the results on the console.
  
@author: dspaccapeli
"""

#imports to manage the sql db
import sqlite3 as lite
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


#connect to the database
db_connection = lite.connect('DATABASE_PATH')

#open the cursor to start querying the database - read ops
read_curs = db_connection.cursor()

#this is line 550
route_id = 2550
#refine query
hh_start = 15
hh_end = 2
wk_start = 1
wk_end = 5
direction = 1

#select all infos for stop equals _n_
#month
#df = pd.read_sql_query("SELECT arr_time, stop_order, stop_id, direction, start_time, sch_time, day, weekday, delay from hsl where route_id=%s and month=%s order by start_time" % (route_id, month), db_connection)

#general
df = pd.read_sql_query("SELECT stop_order, direction, start_time, sch_time, weekday, delay, pause from hsl where route_id=%s order by start_time" % (route_id), db_connection)

train, test = train_test_split(df, test_size = 0.2)

mean = train['delay'].mean()
median = train['delay'].median()

mean_err = 0
med_err =0
naive = 0

for index, row in test.iterrows():
  mean_err+=abs(row['arr_time']-row['sch_time']-mean)
  med_err+=abs(row['arr_time']-row['sch_time']-median)

for index, row in test.iterrows():
  naive+=abs(row['arr_time']-row['sch_time'])

print('avg error for mean: >> %s <<' % (mean_err/len(test)))
print('avg error for median: >> %s <<' % (med_err/len(test)))
print('--------------------------------')
print('avg error for naive: >> %s <<' % (naive/len(test)))
