
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 20:51:38 2023

@author: minah
"""

# this code runs all necessary packages 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, asin, sqrt, radians
from datetime import timedelta


#%% this code loads the GTFS MTA Manhattan trips and trips files. Merging them preserve the sequence of trips
df_trips = pd.read_csv('trips.txt')
df_time = pd.read_csv('stop_times.txt')
# merging the two files, the first df takes precedence
df_ts = df_trips.merge(df_time, on = "trip_id")

#%% Case Study = M101 bus line
# This code masks a dataframe, meaning it reduces the size of the dataframe to contain only the defined value(s) in the defined column(s)

df_ts_M101 = df_ts[["route_id", "trip_id", "shape_id","trip_headsign", "arrival_time", "stop_id", "stop_sequence", "direction_id"]].loc[df_ts["route_id"]=="M101"]
df_ts_M101.to_csv("M101_stops.csv", index=False)
                 
# This code chooses arbitrary trip_ids to isolate a route running in both directions, defined by a 0 for northbound and 1 for southbound routes. Each direction is 78 stops. 
df_ts_M101_ns = df_ts_M101.loc[(df_ts_M101["trip_id"]=="OH_H3-Weekday-015200_M101_2") | (df_ts_M101["trip_id"] =="OH_H3-Weekday-025000_M101_2")]
df_ts_M101_n = df_ts_M101_ns.loc[df_ts_M101_ns["direction_id"] == 0]
df_ts_M101_s = df_ts_M101_ns.loc[df_ts_M101_ns["direction_id"] == 1]

#%%% Add time difference column to northbound and southbound direction dataframes

df_ts_M101_n["timetravelledinhours"] = pd.to_timedelta(df_ts_M101_n["arrival_time"]).dt.total_seconds()/3600 # converting arrival time into seconds and then hours
df_ts_M101_n["timedifference"] = df_ts_M101_n["timetravelledinhours"].diff().abs() # takes the difference between index i and i-1, and places it in index i
df_ts_M101_n = df_ts_M101_n.drop(["timetravelledinhours"], axis = 1)
df_ts_M101_s["timetravelledinhours"] = pd.to_timedelta(df_ts_M101_s["arrival_time"]).dt.total_seconds()/3600
df_ts_M101_s["timedifference"] = df_ts_M101_s["timetravelledinhours"].diff().abs()
df_ts_M101_s = df_ts_M101_s.drop(["timetravelledinhours"], axis = 1)

#%%% Save each dataframe as a csv file

df_ts_M101_n.to_csv("M101_northbound.csv", index=False)
df_ts_M101_s.to_csv("M101_southbound.csv", index=False)