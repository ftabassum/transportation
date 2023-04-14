
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

#%% This is a generalized code that can be applied to any bus line. Comments are made where specific inputs are required
# This code masks a dataframe, meaning it reduces the size of the dataframe to contain only the defined value(s) in the defined column(s)

df_ts_bl = df_ts[["route_id", "trip_id", "shape_id","trip_headsign", "arrival_time", "stop_id", "stop_sequence", "direction_id"]].loc[df_ts["route_id"]=="M15"] #choose a specific bus line for the route_id


#%%                 
# This code chooses arbitrary trip_ids to isolate a route running in both directions, defined by a 0 for northbound or eastbound and 1 for southbound or westbound routes. 
df_ts_bl_01 = df_ts_bl.loc[(df_ts_bl["trip_id"]=="INSERT TRIP ID FOR DIRECTION_ID = 0") | (df_ts_bl["trip_id"] =="INSERT TRIP ID FOR DIRECTION_ID = 1")]
df_ts_bl_0 = df_ts_bl_01.loc[df_ts_bl_01["direction_id"] == 0]
df_ts_bl_1 = df_ts_bl_01.loc[df_ts_bl_01["direction_id"] == 1]

#%%% Add time difference column to northbound/eastbound and southbound/westbound direction dataframes

df_ts_bl_0["timetravelledinhours"] = pd.to_timedelta(df_ts_bl_0["arrival_time"]).dt.total_seconds()/3600 # converting arrival time into seconds and then hours
df_ts_bl_0["timedifference"] = df_ts_bl_0["timetravelledinhours"].diff().abs() # takes the difference between index i and i-1, and places it in index i
df_ts_bl_0 = df_ts_bl_0.drop(["timetravelledinhours"], axis = 1)
df_ts_bl_1["timetravelledinhours"] = pd.to_timedelta(df_ts_bl_1["arrival_time"]).dt.total_seconds()/3600
df_ts_bl_1["timedifference"] = df_ts_bl_1["timetravelledinhours"].diff().abs()
df_ts_bl_1 = df_ts_bl_1.drop(["timetravelledinhours"], axis = 1)

#%%% Save each dataframe as a csv file, according to the particular bus line name

df_ts_bl_0.to_csv("INSERTBUSLINENAME_DIRECTION.csv", index=False) 
df_ts_bl_1.to_csv("INSERTBUSLINENAME_DIRECTION.csv", index=False)