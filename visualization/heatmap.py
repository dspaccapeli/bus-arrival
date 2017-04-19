#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Description:
  Plot an heatmap of the relationship
  between the delay at different stops
  in the same run.

  NB There's a problem in the relative size
     of the output image, see the library doc.

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

#select all infos for stop equals _n_
df = pd.read_sql_query("SELECT delay, delay as delay_prev, start_time as begin from hsl where route_id=%s" % \
                       (route_id), db_connection)

#since start_time is UNIX time it's unique given a route
#select a list of all the different start_time -> they identify daily departures for a bus (~run_code)
unq_dep = df.begin.unique()

at_next = 3
runs = 600

np.random.shuffle(unq_dep)
x1 = np.array([])
y = np.array([])
i=0
for x in unq_dep:
    i+=1
    #for each run_code
    temp = df[df['begin'] == x]
    #allign the shifted columns assuming sequential stop_order
    #caveat @ http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
    temp.delay_prev = temp.delay_prev.shift(-at_next)
    temp = temp[:-at_next]
    x1 = np.append(x1, temp['delay_prev'])
    y = np.append(y, temp['delay'])
    #up to a max of 200 lines
    #if i==runs:
        #break
print(np.size(x1))
print(np.size(y))

heatmap, xedges, yedges = np.histogram2d(x1, y, bins=60)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

fig = plt.figure()
fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')

ax = fig.add_subplot(111)
ax.set_title('Heatmap with %s delay and %s runs' % (at_next, runs))

ax.set_xlabel('delay_prev')
ax.set_ylabel('delay')

plt.clf()
plt.imshow(heatmap.T, extent=extent, origin='lower')
plt.show()
