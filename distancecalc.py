# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 13:34:22 2023

@author: minah
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, asin, sqrt, radians

## load GTFS MTA Bus Stop file which has stop coordinates (but not according to bus lines) 
#MTA_Bus_Stops = pd.read_csv(r'C:\Users\minah\OneDrive\Desktop\Independent Study\stops.txt')
MTA_Bus_Stops = pd.read_csv('stops.txt')
MTA_Bus_Stops = MTA_Bus_Stops.drop(["stop_desc", "zone_id", "stop_url", "location_type", "parent_station"], axis=1)

## load calculated time difference csv file
#df_time_M101 = pd.read_csv(r'C:\Users\minah\OneDrive\Desktop\Independent Study\Time Difference\M101_timedifference.csv')
df_time_M101 = pd.read_csv('M101_timedifference.csv')

# merge time and location dataframes to correspond the time difference to a stop location
M101 = MTA_Bus_Stops.merge(df_time_M101, on = 'stop_id')
M101["distanceinmiles"] = 3960*2 * np.arcsin(np.sqrt(np.sin((np.radians(M101['stop_lat']) - np.radians(M101.stop_lat.shift(1)))/2)**2 + np.cos(np.radians(M101.stop_lon.shift(1))) * np.cos(np.radians(M101['stop_lon'])) * np.sin((np.radians(M101['stop_lon']) - np.radians(M101.stop_lon.shift(1)))/2)**2))

#M101.to_csv(r'C:\Users\minah\OneDrive\Desktop\Independent Study\Distances\M101 distances.csv')
M101.to_csv('distances.csv')