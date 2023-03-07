
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 13:34:22 2023

@author: minah
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, asin, sqrt, radians

#%% This code calculates distances between bus stops for the M101 bus line. These are the shortest distances between coordinates that do not take into account road geometry.
# load GTFS MTA Bus Stop file which has stop coordinates (but not according to bus lines) 
MTA_Bus_Stops = pd.read_csv('stops.txt')
MTA_Bus_Stops = MTA_Bus_Stops.drop(["stop_desc", "zone_id", "stop_url", "location_type", "parent_station"], axis=1)

# load previously calculated M101 northbound and southbound csv files with time difference
df_ts_M101_n = pd.read_csv("M101_northbound.csv")
df_ts_M101_s = pd.read_csv("M101_southbound.csv")

# merge time and location dataframes to correspond the time difference to a stop location (coordinates)
df_ts_M101_n = df_ts_M101_n.merge(MTA_Bus_Stops, on = 'stop_id')
df_ts_M101_n["distanceinmiles"] = 3960*2 * np.arcsin(np.sqrt(np.sin((np.radians(df_ts_M101_n['stop_lat']) - np.radians(df_ts_M101_n.stop_lat.shift(1)))/2)**2 + np.cos(np.radians(df_ts_M101_n.stop_lon.shift(1))) * np.cos(np.radians(df_ts_M101_n['stop_lon'])) * np.sin((np.radians(df_ts_M101_n['stop_lon']) - np.radians(df_ts_M101_n.stop_lon.shift(1)))/2)**2))
df_ts_M101_s = df_ts_M101_s.merge(MTA_Bus_Stops, on = 'stop_id')
df_ts_M101_s["distanceinmiles"] = 3960*2 * np.arcsin(np.sqrt(np.sin((np.radians(df_ts_M101_s['stop_lat']) - np.radians(df_ts_M101_s.stop_lat.shift(1)))/2)**2 + np.cos(np.radians(df_ts_M101_s.stop_lon.shift(1))) * np.cos(np.radians(df_ts_M101_s['stop_lon'])) * np.sin((np.radians(df_ts_M101_s['stop_lon']) - np.radians(df_ts_M101_s.stop_lon.shift(1)))/2)**2))

#%% Save each dataframe as a csv file

df_ts_M101_n.to_csv("M101_northbound_dist.csv", index=False)
df_ts_M101_s.to_csv("M101_southbound_dist.csv", index=False)

#%% This code calculates bus speeds for the M101 for the northbound and southbound routes. 
# load calculated distance and time difference files
df_ts_M101_n = pd.read_csv("M101_northbound_dist.csv")
df_ts_M101_s = pd.read_csv("M101_southbound_dist.csv")

# calculate speeds for each df
df_ts_M101_n["speed"] = df_ts_M101_n["distanceinmiles"]/df_ts_M101_n["timedifference"]
df_ts_M101_s["speed"] = df_ts_M101_s["distanceinmiles"]/df_ts_M101_s["timedifference"]

# compare distances calculated to actual distances from NYCT
# changing NYCT data syntax to match ours
df_ts_M101_n["dist_from_start"]=df_ts_M101_n["distanceinmiles"].cumsum(axis=0)
NYCT_data = pd.read_excel("M101_Stop_Distance.xlsx")
NYCT_M101_ns = NYCT_data.drop(["ROUTE_ID", "SPS_REL_STOP", "STOP_ID"], axis=1)
NYCT_M101_n = NYCT_M101_ns.loc[(NYCT_M101_ns["SPA_DIR"]=="NB")] #masking dataframe- takes columns associated with "NB" in the SPA_DIR column and makes new dataframe
NYCT_M101_n = NYCT_M101_n.rename(columns={'STO_BOX_ID':'stop_id'})

M101_dist_compare_n = df_ts_M101_n.merge(NYCT_M101_n, on="stop_id") #merges NYCT data with ours
M101_dist_compare_n = M101_dist_compare_n[["stop_name", "stop_id", "dist_from_start", "SRS_DIST_FROM_START"]]
M101_dist_compare_n["%_diff"]=((M101_dist_compare_n["SRS_DIST_FROM_START"]-M101_dist_compare_n["dist_from_start"])/M101_dist_compare_n["dist_from_start"])*100 #percent difference between the two datas
avg_percent_error = M101_dist_compare_n["%_diff"].mean()