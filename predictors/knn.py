#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Description:
  Train a knn model on the data and test
  it printing the results on the console.
  MAY TAKE A WHILE FOR BIG DATASETS.

@author: dspaccapeli
"""

#imports to manage the sql db
import sqlite3 as lite
import pandas as pd
import datetime as dt
from sklearn.neighbors import KNeighborsRegressor
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
month=2

#select all infos for stop equals _n_
#month
#df = pd.read_sql_query("SELECT arr_time, stop_order, stop_id, direction, start_time, sch_time, day, weekday, delay from hsl where route_id=%s and month=%s order by start_time" % (route_id, month), db_connection)

#general
#df = pd.read_sql_query("SELECT arr_time, stop_order, stop_id, direction, start_time, sch_time, day, weekday, delay from hsl where route_id=%s and month=%s order by start_time" % (route_id, month), db_connection)

df = pd.read_sql_query("SELECT arr_time, stop_order, stop_id, direction, start_time, sch_time, day, weekday, delay from hsl where route_id=%s and month=%s order by start_time" % (route_id, month), db_connection)

stop_ids = df['stop_id'].unique()

df = df[df['stop_id']==stop_ids[0]]


for index, row in df.iterrows():
   row['start_time'] = int(dt.datetime.fromtimestamp(row['start_time']).strftime('%H'))
   row['sch_time'] = int(dt.datetime.fromtimestamp(row['sch_time']).strftime('%H'))
   if(row['day']<14):
       if(row['day']<7):
           row['day'] = 1
       else:
           row['day'] = 2
   elif(row['day']<21):
       row['day'] = 3
   else:
       row['day'] = 4

train, test = train_test_split(df, test_size = 0.1)

neigh = KNeighborsRegressor(n_neighbors=8, metric='braycurtis', n_jobs=-1)

temp = train.drop(['delay'], axis=1)

temp = temp.drop(['stop_id'], axis=1)

neigh.fit(temp.drop(['arr_time'], axis=1).values, train['delay'].values)

knn_err = 0
naive = 0

for index, row in test.iterrows():
  print index
  temp = row.drop(['delay'])
  temp = temp.drop(['stop_id'])
  knn_err+=abs(row['arr_time']-row['sch_time']-neigh.predict(temp.drop(['arr_time']))[0])
  naive+=abs(row['delay'])

print('avg error for knn: >> %s <<' % (knn_err/len(test)))
print('--------------------------------')
print('avg error for naive: >> %s <<' % (naive/len(test)))
