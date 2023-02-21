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


#%% this code loads the GTFS MTA Manhattan trips and shape files. Merging them preserve the sequence of trips
df_trips = pd.read_csv('trips.txt')
df_shapes = pd.read_csv('shapes.txt')
# merging the two files, the first df takes precedence
df_ts = df_trips.merge(df_shapes, on = "shape_id")

#%%this code loads GTFS MTA Manhattan bus stop times and divides them according to the bus line
#df_time = pd.read_csv(r'C:\Users\minah\OneDrive\Desktop\Independent Study\stop_times.txt', sep=',' , header=1, names = ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence", "pickup_type", "drop_off_type", "timepoint"])
df_time = pd.read_csv('stop_times.txt', sep=',' , header=1, names = ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence", "pickup_type", "drop_off_type", "timepoint"])


#adding a new column 'Bus_Line' to only include the bus line name
df_time['Bus_Line'] = df_time["trip_id"].str.split("_").map(lambda x: x[2])

#masking a dataframe
df_time_M101 = df_time[["arrival_time", "stop_id", "Bus_Line"]].loc[df_time['Bus_Line']=="M101"]
df_time_M101.drop_duplicates(subset=["stop_id"], keep="first", inplace=True)
df_time_M101.head()

# there are a lot of suplicate values in the set, why?
df_time_M101.drop_duplicates(subset=["stop_id"], keep="first", inplace=True)
df_time_M101.head()

# this code converts time difference into hours (want speed in mph)
df_time_M101["timetravelledinhours"] = pd.to_timedelta(df_time_M101["arrival_time"]).dt.total_seconds()/3600
df_time_M101["timedifference"] = df_time_M101["timetravelledinhours"].diff().abs()

# look at where there are negative times in the dataset and why that is the case
df_time_M101 = df_time_M101.drop(["timetravelledinhours"], axis=1)
#df_time_M101.to_csv(r'C:\Users\minah\OneDrive\Desktop\Independent Study\Time Difference\M101_timedifference.csv', index=False)
df_time_M101.to_csv('M101_timedifference.csv', index=False)
