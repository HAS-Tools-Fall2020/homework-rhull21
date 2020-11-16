# Note this is a workflow analyzing historical data from NOAA. 
# Here is more information: https://psl.noaa.gov/data/gridded_help/howtosub.html
# And here: https://psl.noaa.gov/cgi-bin/db_search/SearchMenus.pl

# ----------------------
# Modified from Week12_Reanalysis_Netcdf_starter.py in course materials
# QH 11132020
# ----------------------

# %%
import pandas as pd
import matplotlib.pyplot as plt
# netcdf4 needs to be installed in your environment for this to work
import xarray as xr
import rioxarray
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
# import geopandas as gpd
import fiona
import shapely
from netCDF4 import Dataset
import os

# %%
# Load and view data
# Net CDF file historical time series
precip_data_path = os.path.join('../data/netcdfs',
                         '2_Re_precip_X72.210.40.39.318.16.49.38.nc')
temp_data_path = os.path.join('../data/netcdfs',
                         '3_Re_Temp_X72.210.40.39.318.17.14.16.nc')

# Read in the dataset as an x-array
precip_dataset = xr.open_dataset(precip_data_path)
temp_dataset = xr.open_dataset(temp_data_path)

# %%
# Describe lat, long
precip_latlong = [round(precip_dataset['lat'].values.item(), 4),
                  round(precip_dataset['lon'].values.item(), 4)]
temp_latlong = [round(temp_dataset['lat'].values.item(), 4),
                  round(temp_dataset['lon'].values.item(), 4)]
print("Precipitation lat / long = ", precip_latlong)
print("Temperature lat / long = ", temp_latlong)

# %%
# # Focus on just the precip and temp values
# precip = precip_dataset['prate']
# temp = temp_dataset['air']

# %%
# Slice for time, location
precip = precip_dataset['prate'].loc['2010-01-01':'2020-12-31'].sel(lat=precip_latlong[0], lon=precip_latlong[1])
temp = temp_dataset['air'].loc['2010-01-01':'2020-12-31'].sel(lat=temp_latlong[0], lon=temp_latlong[1])

# %% 
# use x-array to plot timeseries
fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('time (y)')
ax1.set_ylabel(precip.attrs['long_name']+' '+precip.attrs['units'], color=color)
ax1.plot(precip['time'], precip, color=color, alpha=0.7)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:orange'
ax2.set_ylabel(temp.attrs['long_name']+' '+temp.attrs['units'], color=color)
ax2.plot(temp['time'], temp, color=color, alpha=0.7)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

# %%
# Conver to dataframe
precip = precip.to_dataframe()
temp = temp.to_dataframe()
