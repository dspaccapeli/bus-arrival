#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Description:
  Plot the correlation between features.

@author: dspaccapeli
"""

#imports to manage the sql db
import sqlite3 as lite
import pandas as pd
from random import shuffle

#connect to the database
db_connection = lite.connect('DATABASE_PATH')

#open the cursor to start querying the database - read ops
read_curs = db_connection.cursor()

#this is line 550
route_id = 2550

#select all infos for stop equals _n_
df = pd.read_sql_query("SELECT stop_order, start_time, sch_time, arr_time, dep_time, delay, pause from hsl where route_id=%s" % \
                       (route_id), db_connection)

unq_dep = df.start_time.unique()
shuffle(unq_dep)
temp = df[df['start_time'] == unq_dep[0]]

import seaborn as sns
corr = df.corr()

sns.heatmap(corr,
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)
sns.plt.savefig('correlation matrix for start_time = %s' % str(unq_dep[0]), ext="png")
