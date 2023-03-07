# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 00:10:15 2023

@author: minah
"""
import pandas as pd
import matplotlib.pyplot as plt


#%% plotting bus lane shapefile
import geopandas as gpd
bus_lanes = gpd.read_file("NYC_Bus_Lane.shp").set_crs('epsg:3587')
bus_lanes.plot(figsize=(20,20))
plt.scatter(x=df_ts_M101_n["stop_name"], y=df_ts_M101_n["speed"])
plt.show()
#%% This section creates data visualizations for the above data and bus lanes
# using only matplotlib

fig = df_ts_M101_n[["stop_name", "speed"]].plot(x="stop_name", y="speed", title = "FT GEORGE 193 ST via 3 AV via AMSTERDAM Bus Speeds", figsize=(40,20))
# code to creat multicoloured line graph: https://matplotlib.org/stable/gallery/lines_bars_and_markers/multicolored_line.html#sphx-glr-gallery-lines-bars-and-markers-multicolored-line-py

#%% using Folium
import folium
map = folium.Map(location=[df_ts_M101_n.stop_lat.mean(), df_ts_M101_n.stop_lon.mean()], zoom_start = 14, control_scale = True)
for index, location_info in df_ts_M101_n.iterrows():
    folium.Marker([location_info["stop_lat"], location_info["stop_lon"]], popup=location_info["speed"]).add_to(map)
style = {'fillColor': '#8B2222', 'color': '#8B2222'} 
bus_lanes = gpd.read_file("NYC_Bus_Lane.shp").set_crs('epsg:3587')
folium.GeoJson(data=bus_lanes["geometry"], name="bus lane", style_function=lambda x:style).add_to(map)
map.save("map.html")

#%% heat map
#import seaborn as sns
#heatmapdata = df_ts_M101_n.pivot("speed", "stop_name")
#ax = sns.heatmap(heatmapdata)
#plt.title = "Heat Map showing speeds according to stop names for M101 northbound"
#plt.show()