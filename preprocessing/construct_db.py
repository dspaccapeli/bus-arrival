#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Description:
  Create a new table in the database.
  This is  achieved using a view and
  checking various constraints.

@author: dspaccapeli
"""

#imports to manage the sql db and the unix epoch conversion
import sqlite3 as lite
import datetime as dt

#connect to the database
db_connection = lite.connect('DATABASE_PATH')

#let the fetch be of type row (keys() and access by name)
#otherwise it's a simple tuple with values
db_connection.row_factory = lite.Row

#open the cursor to start querying the database - read ops
read_curs = db_connection.cursor()
#open the cursor to start querying the database - write ops
write_curs = db_connection.cursor()

#read all the db one-by-one, this just 'sets' the query
read_curs.execute("QUERY")

#status counter to check progression of the program
status = 0

#        new schema:
#            route_id
#            stop_id
#            stop_order
#	     direction
#            start_time
#            sch_time
#            arr_time
#            dep_time
#            hour
#            day
#            month
#            year
#            weekday
#            delay
#            pause

while True:
    #fetch the next 100.000 results - batches
    results = read_curs.fetchmany(120000)

    #at the end the method will return an empty list, so break
    if not results:
        break

    for row in results:
          #counter update and print
          status += 1
          print 'row: ' + str(status)

          delay = int(row['dep_time']) - int(row['sch_time'])
          pause = int(row['dep_time']) - int(row['arr_time'])

          #reject every delay bigger than an hour // probably outlier
          #anyway not the normal behavior we're trying to predict
          #it counts as 'almost' a new run
          if(abs(delay) > 60*30):
              continue

          #reject every entry that has departed before arrival
          #or that buses that stops for more than 10 minutes // errors
          #sometimes buses too early try to catch up
          if(pause < 0 or pause > 60*10):
              continue

          #reject every entry in which the schedule time is before
          #the beginning runtime for the route
          if(int(row['sch_time']) < int(row['run_sch_starttime'])):
              continue

          #datetime func automatically adjust for timezones (!)
          #NULL on the autoincrement field to _autoincrement_
          write_curs.execute("INSERT INTO hsl VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",        \
                             (str(row['route_id']),                                               \
                              str(row['stop_id']),                                                \
                              int(row['stop_order']),                                             \
                              int(row['direction']),                                              \
                              int(row['run_sch_starttime']),                                      \
                              int(row['sch_time']),                                               \
                              int(row['arr_time']),                                               \
                              int(row['dep_time']),                                               \
                              int(dt.datetime.fromtimestamp(row['arr_time']).strftime('%H')),     \
                              int(dt.datetime.fromtimestamp(row['arr_time']).strftime('%d')),     \
                              int(dt.datetime.fromtimestamp(row['arr_time']).strftime('%m')),     \
                              int(dt.datetime.fromtimestamp(row['arr_time']).strftime('%Y')),     \
                              int(dt.datetime.fromtimestamp(row['arr_time']).isoweekday()),       \
                              delay,                                                              \
                              pause                                                               \
                                                   )                                              \
                            )
    #commit the insertions ca. 100k at a time
    db_connection.commit()

#close the cursor instance
read_curs.close()
#close the connection to the database
db_connection.close()
