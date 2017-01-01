#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Description:
  Plot the relationship between the delay
  at one stop and the one at 1/3/5
  stops from now.

@author: dspaccapeli
"""

#imports to manage the sql db
import sqlite3 as lite
import pandas as pd
#to make the plot show-up from command line
import matplotlib.pyplot as plt
import numpy as np

#connect to the database
db_connection = lite.connect('DATABASE_PATH')

#open the cursor to start querying the database - read ops
read_curs = db_connection.cursor()

#this is line 550
route_id = 2550
direction=1

#select all infos for stop equals _n_
df = pd.read_sql_query("SELECT delay, delay as delay_prev, start_time as begin from hsl where route_id=%s and direction=%s" % \
                       (route_id, direction), db_connection)

#since start_time is UNIX time it's unique given a route

#select a list of all the different start_time -> they identify daily departures for a bus (~run_code)
unq_dep = df.begin.unique()

at_next = 1
points = 400

#init 9 plots
for count in range(1,2):
    #take a random run_code
    np.random.shuffle(unq_dep)

    i=0
    for x in unq_dep:
        i+=1
        #for each run_code
        temp = df[df['begin'] == x]
        #allign the shifted columns assuming sequential stop_order
        #caveat @ http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
        temp.delay_prev = temp.delay_prev.shift(-at_next)
        temp = temp[:-at_next]
        #plot evolution of the delay
        plt.scatter(temp['delay_prev'], temp['delay'], alpha=0.1)
        #up to a max of 200 lines
        #if i==points:
            #break
    '''
    plt.suptitle('Sequential delay evolution')
    plt.xlabel('delay')
    plt.ylabel('delay at %s stop from now' % at_next)
    plt.savefig(str(count), ext="png")
    plt.clf()
    '''

plt.suptitle('Sequential delay evolution')
plt.xlabel('delay')
plt.ylabel('delay at %s stop from now' % at_next)
plt.savefig('rep_%s' % (at_next), ext="png")
plt.clf()
