#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Description:
  Plot the delay evolution during a run
  for multiple ones having the run_time
  (in seconds) on the X axis.

@author: dspaccapeli
"""

#imports to manage the sql db
import sqlite3 as lite
import pandas as pd
#to make the plot show-up from command line
import matplotlib.pyplot as plt
#to get multiple evolution of delay
from random import shuffle

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

#select all infos for stop equals _n_sqlite
df = pd.read_sql_query("SELECT delay, sch_time-start_time as time, start_time as begin from hsl where route_id=%s and direction=%s or hour>=%s and hour<=%s order by time" % \
                       (route_id, direction, hh_start, hh_end), db_connection)

#select a list of all the different start_time -> they identify daily departures for a bus (~run_code)
unq_dep = df.begin.unique()

#init 9 plots

for count in [1, 2, 3, 4, 5, 6, 7, 8, 9]:

    #take a random run_code
    shuffle(unq_dep)

    i=0
    for x in unq_dep:
        i+=1
        #for each run_code
        temp = df[df['begin'] == x]
        #plot evolution of the delay
        plt.plot(temp['time'], temp['delay'], alpha=0.6)
	#plt.scatter(temp['time'], temp['delay'], alpha=0.7)
	#up to a max of 5 lines
        if i==10:
            break

    plt.suptitle('Delay progression between %s and %s during the week' % (hh_start, hh_end))
    plt.xlabel('run time')
    plt.ylabel('delay')
    plt.savefig(str(count), ext="png")
    plt.clf()

'''
plt.suptitle('Delay progression between %s and %s during the week' % (hh_start, hh_end))
plt.xlabel('run time')
plt.ylabel('delay')
plt.savefig(str(count), ext="png")
plt.clf()
'''
