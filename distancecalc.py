# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 13:34:22 2023

@author: minah
"""

import pandas as pd
import matplotlib.pyplot as pltimport numpy as np
from math import cos, sin, asin, sqrt, radians

#%% This code calculates distances between bus stops for the M101 bus line. These are the shortest distances between coordinates that do not take into account road geometry.
# load GTFS MTA Bus Stop file which has stop coordinates (but not according to bus lines) 
MTA_Bus_Stops = pd.read_csv('stops.txt')
MTA_Bus_Stops = MTA_Bus_Stops.drop(["stop_desc", "zone_id", "stop_url", "location_type", "parent_station"], axis=1)

# load previously calculated M101 northbound and southbound csv files with time difference
df_ts_M101_n = pd.read_csv("M101_northbound.csv")
df_ts_M101_s = pd.read_csv("M101_southbound.csv")
# merge time and location dataframes to correspond the time difference to a stop location
df_ts_M101_n = df_ts_M101_n.merge(MTA_Bus_Stops, on = 'stop_id')
df_ts_M101_n["distanceinmiles"] = 3960*2 * np.arcsin(np.sqrt(np.sin((np.radians(df_ts_M101_n['stop_lat']) - np.radians(df_ts_M101_n.stop_lat.shift(1)))/2)**2 + np.cos(np.radians(df_ts_M101_n.stop_lon.shift(1))) * np.cos(np.radians(df_ts_M101_n['stop_lon'])) * np.sin((np.radians(df_ts_M101_n['stop_lon']) - np.radians(df_ts_M101_n.stop_lon.shift(1)))/2)**2))
df_ts_M101_s = df_ts_M101_s.merge(MTA_Bus_Stops, on = 'stop_id')
df_ts_M101_s["distanceinmiles"] = 3960*2 * np.arcsin(np.sqrt(np.sin((np.radians(df_ts_M101_s['stop_lat']) - np.radians(df_ts_M101_s.stop_lat.shift(1)))/2)**2 + np.cos(np.radians(df_ts_M101_s.stop_lon.shift(1))) * np.cos(np.radians(df_ts_M101_s['stop_lon'])) * np.sin((np.radians(df_ts_M101_s['stop_lon']) - np.radians(df_ts_M101_s.stop_lon.shift(1)))/2)**2))

#%% Save each dataframe as a csv file

df_ts_M101_n.to_csv("M101_northbound_dist.csv", index=False)
df_ts_M101_s.to_csv("M101_southbound_dist.csv", index=False)

