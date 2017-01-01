 #!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Description:
  Plot the delay and pause distribution
  eliminating the outliers to visualize
  a _normalized_ plot.

@author: dspaccapeli
"""

#imports to manage the sql db
import sqlite3 as lite
import pandas as pd
#to make the plot show-up from command line
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#connect to the database
db_connection = lite.connect('DATABASE_PATH')

#open the cursor to start querying the database - read ops
read_curs = db_connection.cursor()

route_id = 2550

#select all infos for stop equals _n_
df = pd.read_sql_query("SELECT * FROM hsl WHERE route_id=%s" % (route_id), db_connection)

#select column to plot as series
delay = df['delay']

pause = df['pause']

#declare figure to show
plt.figure(1)

#start delay plot
plt.subplot(211)


#-----------------------------------------------------------------------------#
#                           OUTLIER DETECTION                                 #
#          note that substracting the mean centres the data                   #
#                    OLD AND PROBABLY HAS ERRORS                              #
#-----------------------------------------------------------------------------#
#consider all the points that go further than 3.5 std from the mean as outliers
d_outlier =  delay[~((delay-delay.mean()).abs()>3*delay.std())]
#d_outlier.rename('DELAY FOR ROUTE_ID = %s, NO OUTLIERS' % route_id);

"""
#-----------------------------------------------------------------------------#
#                             TUCKEY'S TEST                                   #
#      https://www.jstor.org/stable/2289073?seq=8#page_scan_tab_contents      #
#      (!)     w/ k=2.28   &   formula~ [q_1 -k(q_3 -q_1), q_3 +k(q_3 -q_1)]  #
#-----------------------------------------------------------------------------#

k = 1.5


#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#---------------------------     DELAY     -----------------------------------#
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

q_1 = delay.quantile(q=0.25)
q_3 = delay.quantile(q=0.75)
mean = delay.mean()

print "delay q_1 is " + str(q_1)
print "delay q_3 is " + str(q_3)
print "delay mean is " + str(mean)


#remove the data that is out of the Tuckey's range
d_outlier = delay[~(delay-mean <= q_1-k*(q_3-q_1))]

print "d_outlier size pre-skim: " + str(d_outlier.size)

d_outlier = d_outlier[~(d_outlier-mean >= q_3+k*(q_3-q_1))]

print "d_outlier size post-skim: " + str(d_outlier.size)
"""

#plot as a distribution
#d_outlier.plot(kind='kde', title="DELAY FOR ROUTE_ID = %s" % route_id)
#sns.distplot(d_outlier, rug=True, hist=False);
plt.hist(d_outlier, bins=30, histtype='step')
plt.title('Delay distribution for route_id = %s' % route_id)
#show the median and mean on the plot
plt.axvline(d_outlier.mean(), color='k', linestyle='solid')
plt.axvline(d_outlier.median(), color='r', linestyle='dashed')

#display the legend for subplot(1)
MN = mpatches.Patch(color='black', label='Mean')
MD = mpatches.Patch(color='red', label='Median')
plt.legend(handles=[MN, MD], loc='upper right')


#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#---------------------------     PAUSE     -----------------------------------#
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

#start pause plot
plt.subplot(212)

#-----------------------------------------------------------------------------#
#                           OUTLIER DETECTION                                 #
#          note that substracting the mean centres the data                   #
#                    OLD AND PROBABLY HAS ERRORS                              #
#-----------------------------------------------------------------------------#
p_outlier = pause[~((pause-pause.mean()).abs()>3*pause.std())]

#pause.plot(kind='kde', title="DELAY FOR STOP_ID = %s" % stop_id)

"""
q_1 = pause.quantile(q=0.25)
q_3 = pause.quantile(q=0.75)
mean = pause.mean()

print "pause q_1 is " + str(q_1)
print "pause q_3 is " + str(q_3)
print "pause mean is " + str(mean)

p_outlier = pause[~(pause-mean <= q_1-k*(q_3-q_1))]

print "p_outlier size pre-skim: " + str(p_outlier.size)


p_outlier = p_outlier[~(p_outlier-mean >= q_3+k*(q_3-q_1))]

print "p_outlier size post-skim: " + str(p_outlier.size)

#plot as a distribution
p_outlier.plot(kind='kde', title="PAUSE FOR STOP_ID = 1204101")

#show the median and mean on the plot
plt.axvline(p_outlier.mean(), color='k', linestyle='solid')
plt.axvline(p_outlier.median(), color='r', linestyle='dashed')


print(p_outlier.max())
print(p_outlier.count())
"""

#display the legend for subplot(2)
#PROBABLY REDUNDANT, you could use the old one
#MN_P = mpatches.Patch(color='black', label='Mean')
#MD_P = mpatches.Patch(color='red', label='Median')

#delay.rename("DELAY FOR ROUTE_ID = %s" % route_id);
#p_outlier.plot(kind='kde', title="PAUSE FOR ROUTE_ID = %s" % route_id)
#sns.distplot(delay, rug=True, hist=False);
plt.hist(p_outlier, bins=30, histtype='step')
plt.title('Pause distribution for route_id = %s' % route_id)
plt.legend(handles=[MN, MD], loc='upper right')
#show the median and mean on the plot
plt.axvline(p_outlier.mean(), color='k', linestyle='solid')
plt.axvline(p_outlier.median(), color='r', linestyle='dashed')

#let it show
plt.show()
