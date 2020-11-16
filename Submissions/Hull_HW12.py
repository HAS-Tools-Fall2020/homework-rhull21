# ----------------------
# Modified from Week12_Reanalysis_Netcdf_starter.py in course materials
# QH 11132020

# Modified from Hull_HW_12_Week12_Forecast_Netcdf_starter.py in Week12 HW dir
# Modified from Hull_HW10.py in submissions dir
# Modified form Hull_HW12_MAP.py in Week12 HW dir
# QH 11142020
# ----------------------
# %%
# ----------------------------------------------------------------------------------
# Define modules
# ----------------------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import os
import numpy as np
import Hull_HW12_fxns as fn

# %%
# ----------------------------------------------------------------------------------
# Define global variables
# ----------------------------------------------------------------------------------
start = '2010-01-01'
end = '2020-12-31'


# %%
# ----------------------------------
# Import and assemble NetCDF historical data [NOAA, NARR]
# ----------------------------------
# More on Datasets:
# T and P Description: https://psl.noaa.gov/data/gridded/data.narr.html#

# Load and view data
# Net CDF file historical time series
precip_data_path = os.path.join('../data/netcdfs',
                                '2_Re_precip_X72.210.40.39.318.16.49.38.nc')
temp_data_path = os.path.join('../data/netcdfs',
                              '3_Re_Temp_X72.210.40.39.318.17.14.16.nc')

# Read in the dataset as an x-array
precip_dataset = xr.open_dataset(precip_data_path)
temp_dataset = xr.open_dataset(temp_data_path)

# Describe lat, long
precip_latlong = [round(precip_dataset['lat'].values.item(), 4),
                  round(precip_dataset['lon'].values.item(), 4)]
temp_latlong = [round(temp_dataset['lat'].values.item(), 4),
                round(temp_dataset['lon'].values.item(), 4)]

print("Precipitation lat / long = ", precip_latlong)
print("Temperature lat / long = ", temp_latlong)

# Slice for time, location
precip = precip_dataset['prate'].loc[start:end].sel(lat=precip_latlong[0],
                                                    lon=precip_latlong[1])
temp = temp_dataset['air'].loc[start:end].sel(lat=temp_latlong[0],
                                              lon=temp_latlong[1])

# use x-array to plot timeseries
fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('time (y)')
ax1.set_ylabel(precip.attrs['long_name']+' '+precip.attrs['units'],
               color=color)
ax1.plot(precip['time'], precip, color=color, alpha=0.7)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:orange'
ax2.set_ylabel(temp.attrs['long_name']+' '+temp.attrs['units'], color=color)
ax2.plot(temp['time'], temp, color=color, alpha=0.7)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

# Convert to dataframe
precip = precip.to_dataframe()
temp = temp.to_dataframe()

# %%
# ----------------------------------------------------------------------------------
# Import and assemble forecast and historical weather data [visual crossing]
# ----------------------------------------------------------------------------------
vc_hist_data_path = os.path.join('../data/csv-virtualcrossing',
                                 'QVDA3_history_11152020.csv')
vc_forecast_data_path = os.path.join('../data/csv-virtualcrossing',
                                     'QVDA3_forecast_11152020.csv')

vc_hist_df = pd.read_csv(vc_hist_data_path,
                         parse_dates=['Date_time'],
                         index_col='Date_time'
                         )

vc_forecast_df = pd.read_csv(vc_forecast_data_path,
                             parse_dates=['Date_time'],
                             index_col='Date_time'
                             )

# %%
# ----------------------------------------------------------------------------------
# Import and assemble historical flow data [USGS]
# ----------------------------------------------------------------------------------
# adjust path as necessary
site = '09506000'
url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on" \
      "&format=rdb&site_no="+site+"&referred_module=sw&" \
      "period=&begin_date="+start+"&end_date="+end

# read in data
flow_df = pd.read_table(url, sep='\t', skiprows=30,
                        names=['agency_cd', 'site_no',
                               'datetime', 'flow', 'code'],
                        parse_dates=['datetime'],
                        index_col='datetime'
                        )

# re-instantiate data with just the natural log of
# its flow values (to be used later)
flow_df = np.log(flow_df[['flow']])
flow_df.index = flow_df.index.tz_localize(tz="UTC")

# %%
# # --------------------------------------------------------------------------
# # Mesonet import and assembly
# # --------------------------------------------------------------------------
# 1) quickly look for nearby stations
# 1a) Token
# # IMPORTNAT: I overused my token ('a836998da79e4faeac2bf7f5cda57a6e')
# # so I am only able to use the demo token below
mytoken = 'demotoken'
# 1b) 'Base' URL
base_url = "https://api.synopticdata.com/v2/stations/metadata"
# 1c) nearby stations
# look for 10 nearest stations within 10 miles of usgs gaging station
args = {
       'token': mytoken,
       'radius': '34.448333,-111.789167,10',
       'limit': '10',
       }
# 1d) Extract station synoptic data
stationDict = fn.extractmasonet(base_url, args)

# 2) Extract time series data from active sites
# 2a) 'Base' URL
base_url_in = "https://api.synopticdata.com/v2/stations/timeseries"
arg_vars = 'air_temp,precip_accum'
arg_units = 'temp|F,precip|mm'
args_in = {
        'start': start.replace('-', '')+'0000',
        'end': end.replace('-', '')+'0000',
        'obtimezone': 'UTC',
        'vars': arg_vars,
        'stids': '',
        'units': arg_units,
        'token': mytoken}
station_condition_in = 'ACTIVE'
station_name_in = 'QVDA3'

masonet_df = fn.assemble_data_masonet(base_url_in, args_in, stationDict,
                                      data_join=pd.DataFrame(index=flow_df.index),
                                      station_name=station_name_in)

# %%
# ----------------------------------------------------------------------------------
# Compare predictions for temperature
# ----------------------------------------------------------------------------------
# Compare predictions for temperature
# masonet (QVDA3), visual crossing (same lat long), and NOAA NARR
# shows that historical data from VC fits better, due to location
# closer to actual QVDA3 dataset uzed to make model

fig, ax1 = plt.subplots()

color1 = 'tab:blue'
color2 = 'tab:orange'
color3 = 'tab:green'
startdate = start
enddate = end

ax1.set_xlabel('date')
ax1.set_ylabel('temperature in degF at QVDA3')
ax1.plot(temp.loc[startdate:enddate].index,
         fn.Kelvin_2_Faren(temp['air'].loc[startdate:enddate]),
         color=color1, alpha=0.7, label='NETCDF forecast')
ax1.plot(vc_hist_df.loc[startdate:enddate].index,
         vc_hist_df['Temperature'].loc[startdate:enddate],
         color=color2, alpha=0.7, label='VC forecast')
ax1.plot(masonet_df.loc[startdate:enddate].index,
         masonet_df['air_temp_set_1'].loc[startdate:enddate],
         color=color3, alpha=0.7, label='QVDA3 measured')
plt.legend()
plt.show()

# %%
# ----------------------------------------------------------------------------------
# resample, subset, normalize, and lag datasets
# ----------------------------------------------------------------------------------
# sumarize flow, precip, air temp on weekly basis
# # resample
# # # flow
flow_df = flow_df.resample("W").mean()
# # # precip and temp masonet
masonet_df['precip_accum_set_1'] = masonet_df['precip_accum_set_1'] \
                                - masonet_df['precip_accum_set_1'].shift(1)
masonet_df['precip_accum_set_1'].where(
            masonet_df['precip_accum_set_1'] > 0, inplace=True)
p_masonet_df = pd.DataFrame(
                            masonet_df['precip_accum_set_1'].
                            resample("W").sum()
                            )
t_masonet_df = pd.DataFrame(
                            masonet_df['air_temp_set_1'].
                            resample("W").mean()
                            )
# # # precip and temp forecasts
p_vc_forecast_df = pd.DataFrame(
                                vc_forecast_df['Precipitation'].
                                resample("W").sum()
                                )
t_vc_forecast_df = pd.DataFrame(
                                vc_forecast_df['Temperature'].
                                resample("W").mean()
                                )

# # subset, normalize, and lag
flow_df, scale1 = fn.norm_it(start, end, flow_df, 'flow', l_back=1)
p_masonet_df, scale2 = fn.norm_it(start, end, p_masonet_df,
                                  'precip_accum_set_1', l_back=1)
t_masonet_df, scale3 = fn.norm_it(start, end, t_masonet_df,
                                  'air_temp_set_1', l_back=1)

# %%
# ----------------------------------------------------------------------------------
# Build an autoregressive model
# ----------------------------------------------------------------------------------
# Step 1: pick regression variables
# Step 2: pick periods of regression (train)
# Step 3: subset data to regression (trains)
t = pd.concat([flow_df, p_masonet_df, t_masonet_df], axis=1)
t = fn.clean_dataset(t)
t = t.reset_index()

# Step 4: Fit a linear regression to 'train' data using sklearn
# for (i) 1 and 2 week prediction
# # predictive variables (all normalized between 0 and 1) =
# # # 1) 'flow_norm_tm1' (log of flow last week)
# # # 2) 'air_temp_set_1_norm' (mean weekly temperature, over 10 years)
# # # 2) 'precip_accum_set_1_norm' (sum weekly preciptation, over 10 years)
x = t[['flow_norm_tm1',
       'air_temp_set_1_norm',
       'precip_accum_set_1_norm']]
# # dependent variable = 'flow' (log of flow this week)
y = t['flow_norm']
# # use predifined function (makemodel) to generate model
m, s = fn.makemodel(x, y)

# Step 5: Make a prediction for (i) 1 and 2 week,

# (i) week prediction
# set lastweekflow data as most recent week of data
x_lastweekflow = t['flow_norm'].iloc[-1]
# # set last week precip variation and temperature
# x_lastweektemp = t['air_temp_set_1_norm'].iloc[-1]
# x_lastweekprecip = t['precip_accum_set_1_norm'].iloc[-1]

print("AR Week 1 and 2 forecast prediction:")

for i in range(2):
    # set last week precip variation and temperature
    x_lastweekprecip = scale2.transform(p_vc_forecast_df['Precipitation'].
                                        iloc[i].reshape(1, -1))
    x_lastweektemp = scale3.transform(t_vc_forecast_df['Temperature'].
                                      iloc[i].reshape(1, -1))
    # set the week i name
    name = "Week {0}:".format(i+1)
    # predict week i flow, using flow, temperature, and precip
    x_lastweekflow = m.intercept_ + m.coef_[0] * x_lastweekflow \
                                  + m.coef_[1] * x_lastweektemp \
                                  + m.coef_[2] * x_lastweekprecip
    # print week, flow (forecast), precip and temp (predictive variables)
    print(name, "Flow (cfs) =",
                np.round(np.exp(fn.denorm_it(x_lastweekflow, scale1)), 2),
                "Precip (mm)=",
                np.round(fn.denorm_it(x_lastweekprecip, scale2), 2),
                "Temp (deg F)=",
                np.round(fn.denorm_it(x_lastweektemp, scale3), 2))


print("\n")

# Step 4: Fit a linear regression to 'train' data using sklearn
# for (ii) semester forecast
x = t[['flow_norm_tm1']]
# # dependent variable = 'flow' (log of flow this week)
y = t['flow_norm']
# # use predifined function (makemodel) to generate model
m, s = fn.makemodel(x, y)

# Step 5: Make a prediction for (ii) semester forecast

# (ii) semester forecast
# set lastweek as first week of semester
x_lastweekflow = t['flow_norm'][
                            (t['datetime'] >= '2020-08-20') &
                            (t['datetime'] < '2020-08-27')
                            ].values

print("AR Semester forecast prediction:")

for i in range(16):
    name = "Week {0}:".format(i+1)
    # predict week i flow, using flow, temperature, and precip
    x_lastweekflow = m.intercept_ + m.coef_[0] * x_lastweekflow
    # print week, flow (forecast)
    print(name, "Flow (cfs) =",
                np.round(np.exp(fn.denorm_it(x_lastweekflow, scale1)), 2))

# %%
