#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Description:
  Check if there are any jumps in the stop_id column.
  A jump is found when in two subsequent entries for the
  same run the number differ for more than one.
  e.g. 5 -> 7
  This means that the bus doesn't stop at one or more stations.

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

start_prev = 1
stop_prev = 1
jumps = 0
iteration = 0

while True:
    row = read_curs.fetchone()

    start_now = int(row['start_time'])
    stop_now = int(row['stop_id'])

    jumps_prev = jumps

    if(start_now == start_prev):
        if(stop_now > (stop_prev + 1)):
            jumps += 1

    start_prev = start_now
    stop_prev = stop_now

    iteration += 1
    print('iter <- %s' % iteration)

    if(jumps_prev != jumps):
	print('----|| %s ||----' % jumps)

#close the cursor instance
read_curs.close()
#close the connection to the database
db_connection.close()
