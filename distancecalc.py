
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 13:34:22 2023

@author: minah
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, asin, sqrt, radians
from timedifference import time

#%% This code calculates distances between bus stops for a selected bus line. These are the shortest distances between coordinates that do not take into account road geometry.
# load GTFS MTA Bus Stop file which has stop coordinates (but not according to bus lines) 

def speed(line, trip_id_0, trip_id_1, trips, stop_times, stops):
    # load previously calculated bus line csv files with time difference in both directions
    #df_ts_bl_0 = pd.read_csv('insert path for bus line 0 direction')
    #df_ts_bl_1 = pd.read_csv('insert path for bus line 1 direction')
    
    MTA_Bus_Stops = pd.read_csv(stops)
    MTA_Bus_Stops = MTA_Bus_Stops.drop(["stop_desc", "zone_id", "stop_url", "location_type", "parent_station"], axis=1) #these columns are not required in the code
    
    df_ts_bl_0, df_ts_bl_1= time(line, trip_id_0, trip_id_1, trips, stop_times)
    
    #(run this code as is)
    # merge time and location dataframes to correspond the time difference to a stop location (coordinates)
    df_ts_bl_0 = df_ts_bl_0.merge(MTA_Bus_Stops, on = 'stop_id')
    df_ts_bl_0["distanceinmiles"] = 3960*2 * np.arcsin(np.sqrt(np.sin((np.radians(df_ts_bl_0['stop_lat']) - np.radians(df_ts_bl_0.stop_lat.shift(1)))/2)**2 + np.cos(np.radians(df_ts_bl_0.stop_lon.shift(1))) * np.cos(np.radians(df_ts_bl_0['stop_lon'])) * np.sin((np.radians(df_ts_bl_0['stop_lon']) - np.radians(df_ts_bl_0.stop_lon.shift(1)))/2)**2))
    df_ts_bl_1 = df_ts_bl_1.merge(MTA_Bus_Stops, on = 'stop_id')
    df_ts_bl_1["distanceinmiles"] = 3960*2 * np.arcsin(np.sqrt(np.sin((np.radians(df_ts_bl_1['stop_lat']) - np.radians(df_ts_bl_1.stop_lat.shift(1)))/2)**2 + np.cos(np.radians(df_ts_bl_1.stop_lon.shift(1))) * np.cos(np.radians(df_ts_bl_1['stop_lon'])) * np.sin((np.radians(df_ts_bl_1['stop_lon']) - np.radians(df_ts_bl_1.stop_lon.shift(1)))/2)**2))
    
    # create a column for cumulative distance
    df_ts_bl_0["dist_from_start"]=df_ts_bl_0["distanceinmiles"].cumsum(axis=0)
    df_ts_bl_1["dist_from_start"]=df_ts_bl_1["distanceinmiles"].cumsum(axis=0)
    #%% This code calculates bus speeds for the M101 for the northbound and southbound routes. 
    
    # calculate speeds for each df (run this code as is)
    df_ts_bl_0["speed"] = df_ts_bl_0["distanceinmiles"]/df_ts_bl_0["timedifference"] 
    df_ts_bl_1["speed"] = df_ts_bl_1["distanceinmiles"]/df_ts_bl_1["timedifference"]
    
    #%% Save each dataframe as a csv file, according to particular bus line name
    #(insertions required)
    df_ts_bl_0.to_csv(line+"_northbound_dist.csv", index=False)
    df_ts_bl_1.to_csv(line+"_southbound_dist.csv", index=False)

#speed (line, trip_id_northbound, trip_id_southbound, path_to_trips, path_to_time, path_to_bus_stops)
speed('Q43','QV_B3-Weekday-007000_Q43_551','QV_B3-Weekday-011000_Q43_551', 'trips.txt', 'stop_times.txt', 'stops.txt')

