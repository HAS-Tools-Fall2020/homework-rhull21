# %%
# Import necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
from pprint import pprint
from sklearn.linear_model import LinearRegression
import group_functions as gf

# %%
# Prepare 16 week forecasts

# get data from beginning of semester
url_usgs_16wk = 'https://waterdata.usgs.gov/nwis/dv?cb_00060=on' \
           '&format=rdb&site_no=09506000&referred_module=sw' \
           '&period=&begin_date=1989-01-01&end_date=2020-08-29'
data_16wk = pd.read_table(url_usgs_16wk, skiprows=30, names=['agency_cd',
                                                             'site_no',
                                                             'datetime',
                                                             'flow', 'code'],
                          parse_dates=['datetime'])

# Expand the dates to year month day and set them as integers
data_16wk[["year", "month", "day"]] = data_16wk["datetime"].\
                                 astype(str).str.split("-", expand=True)
data_16wk['year'] = data_16wk['year'].astype(int)  # year integer
data_16wk['month'] = data_16wk['month'].astype(int)  # month integer
data_16wk['day'] = data_16wk['day'].astype(int)  # day integer

# get annual average streamflow
year_means = np.zeros((32, 2))
for j in range(1989, 2021):
    year_means[j-1989, 0] = j
    year_means[j-1989, 1] = data_16wk[data_16wk.year == j].flow.mean()

# find the two driest years on record using nsmallest
driest = pd.DataFrame(year_means, columns=['year', 'mean']).\
         nsmallest(2, 'mean')
driest.index = range(2)
driest['year'] = driest['year'].astype(int)

# make a dataframe that only contains data from the driest years
dry_years_data = data_16wk[(data_16wk.year == driest.year[0]) |
                           (data_16wk.year == driest.year[1])]

forecast_dates = gf.getForecastDates()

# initialize list for weekly forecasts
forecasts = []

# go through each week and get the means for each week
for i in range(16):

    # if the forecast week starts and ends in different months
    if (forecast_dates.start_month[i] != forecast_dates.end_month[i]):
        # set the date of the last day of the month
        if(forecast_dates.start_month[i] == 8):
            last_day = 31
        if(forecast_dates.start_month[i] == 9):
            last_day = 30
        if(forecast_dates.start_month[i] == 10):
            last_day = 31
        if(forecast_dates.start_month[i] == 11):
            last_day = 30
        # take average of all dates within the forecast week during dry years
        wk_mean = dry_years_data[((dry_years_data.month ==
                                   forecast_dates.start_month[i]) &
                                 (dry_years_data.day >=
                                  forecast_dates.start_day[i]) &
                                 (dry_years_data.day <= last_day)) |
                                 ((dry_years_data.month ==
                                  forecast_dates.end_month[i]) &
                                 (dry_years_data.day >= 1) &
                                 (dry_years_data.day <=
                                  forecast_dates.end_day[i]))].flow.mean()
        # add weekly mean to forecast lists
        forecasts.append(wk_mean)

    # if the forecast week starts and ends in the same month
    else:
        # take average of all dates within forecast week during dry years
        wk_mean = dry_years_data[(dry_years_data.month ==
                                  forecast_dates.start_month[i]) &
                                 (dry_years_data.day >=
                                  forecast_dates.start_day[i]) &
                                 (dry_years_data.day <=
                                  forecast_dates.end_day[i])].flow.mean()
        # add weekly mean to forecast lists
        forecasts.append(wk_mean)

print('Weekly Forecasts:', forecasts)

# %%

# Input start and end dates
site = '09506000'
start = '1990-01-01'
end = '2020-11-07'

url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=" + \
      site + "&referred_module=sw&period=&begin_date=" + start + \
      "&end_date=" + end
data = pd.read_table(url, skiprows=30, names=['agency_cd', 'site_no',
                                              'datetime', 'flow', 'code'],
                     parse_dates=['datetime'])

data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Aggregate flow values to weekly
flow_weekly = data.resample("W", on='datetime').mean()

# Set flow_weekly to natural log
flow_weekly_log = np.log(flow_weekly)
flow_weekly_log['flow_tm1'] = flow_weekly_log['flow'].shift(1)

# Dry years for training model
train = flow_weekly_log['2017-01-01':'2019-01-01'][['flow', 'flow_tm1']]

# Fitting the model
model = LinearRegression()
x = train['flow_tm1'].values.reshape(-1, 1)
y = train['flow'].values
model.fit(x, y)

r_sq = model.score(x, y)
print('coefficient of determination:', np.round(r_sq, 2))

# Identify starting value for model prediction
start_val = flow_weekly.flow[-1]
# starting value in natural log (needed for regression)
start_val_ln = np.log(start_val)
# create two week forecast (saved in natural log)
# set adjusting value for forecast
adjust = 1.01
two_week_forecast = np.zeros(2)
for i in range(1):
    print('week 1')
    two_week_forecast[0] = gf.single_forecast(model, start_val_ln * adjust)
    print('week 2')
    two_week_forecast[1] = gf.single_forecast(model,
                                              two_week_forecast[0] * adjust)

# %%

# 1) create a df of files, filepath, and name
filepath = '../../spatial_data_nongit/'
gpd_df = pd.DataFrame(columns=['names', 'file', 'gpd'])

names = ['gages', 'rivers', 'gwsi', 'huc', 'az']

gpd_df['names'] = names

filenames = ['gagesII_9322_point_shapefile/gagesII_9322_sept30_2011.shp',
             'USA_Rivers_and_Streams-shp/'
             '9ae73184-d43c-4ab8-940a-c8687f61952f2020328-1-r9gw71.0odx9.shp',
             'GWSI_ZIP_10162020/Shape/GWSI_SITES.shp',
             'Shape/WBDHU10.shp',
             'tl_2016_04_cousub/tl_2016_04_cousub.shp']

gpd_df['file'] = filenames
gpd_df['file'] = filepath + gpd_df['file']

# Import data into df and add to dataframe
for i in range(len(gpd_df)):
    gpd_df.iat[i, 2] = gpd.read_file(gpd_df['file'].iloc[i])

# 2) Add some points
# Stream gauge:  34.44833333, -111.7891667
point_list = np.array([[-111.7891667, 34.44833333]])

# extract crs from huc (desired to apply)
crs_in = gpd_df['gpd'].iloc[
                            gpd_df.index[
                                         gpd_df['names'
                                                ] == 'huc'].tolist()[0]
                            ].crs

# add a line containing point_list to gpd_df including data frame of points
gpd_df = gf.add_pt_gdf(point_list, crs_in, gpd_df, 'points_df')

# 3) fix any crs issues
# 4) Clip data extent for all layers based on extent of arizona

# clip set
clip_set = gpd_df['gpd'].iloc[gpd_df.index[gpd_df['names'] ==
                              'az'].tolist()[0]]

# crs set
# exract crs to set all to (from gages)
crs_set = clip_set.crs

# look through all gdf and (a) fix crs issues and (b) clip domains
for i in range(len(gpd_df)):
    gpd_df['gpd'].iloc[i].to_crs(crs_set, inplace=True)
    pprint(gpd_df['gpd'].iloc[i].crs)
    # clip is not working with this larger dataset
    gpd_df.iat[i, 2] = gpd.clip(gpd_df['gpd'].iloc[i], clip_set, False)

# 6) Make a map of just Verde River Area
extent = gpd_df['gpd'].iloc[1][gpd_df['gpd'].iloc[1]['Name'] == 'Verde River']
salt = gpd_df['gpd'].iloc[1][gpd_df['gpd'].iloc[1]['Name'] == 'Salt River']

rangef = (extent.total_bounds[2] - extent.total_bounds[0])
# clip extent
xmin, xmax, ymin, ymax = extent.total_bounds[0]-rangef, \
                         extent.total_bounds[2]+rangef, \
                         extent.total_bounds[1]-rangef, \
                         extent.total_bounds[3]+rangef

# create plot
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

colorList = ['red', 'blue', 'green', 'grey', 'black', 'yellow']
alphaList = [1, 1, 0.2, 0.5, 0.7, 1]
zorderList = [6, 4, 3, 2, 1, 7]
nameList = ['USGS Stream Gages', 'Arizona Major Rivers',
            'USGS Groundwater Sites', 'HUC 10 Watersheds',
            'AZ', 'Verde River Stream Gage']
markerList = ['X', '_', '.', '_', '_', '*']

# loop through all gdps:
for i in range(len(gpd_df)):
    if gpd_df['names'].iloc[i] == 'huc':
        gpd_df['gpd'].iloc[i].boundary.plot(ax=ax,
                                            label=nameList[i],
                                            zorder=zorderList[i],
                                            edgecolor=colorList[i],
                                            alpha=alphaList[i])

    else:
        gpd_df['gpd'].iloc[i].plot(ax=ax,
                                   label=nameList[i],
                                   zorder=zorderList[i],
                                   color=colorList[i],
                                   alpha=alphaList[i],
                                   marker=markerList[i]
                                   )

# plot just Verde River
extent.plot(ax=ax,
            label='Verde River',
            zorder=5,
            color='purple',
            linestyle='-.',
            linewidth=5)

# plot just Salt River
salt.plot(ax=ax,
          label='Salt River',
          zorder=5,
          color='orange',
          linestyle=':',
          linewidth=5,
          alpha=0.5)

ax.set_title('Arizona Hydrologic Features')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.legend(loc='lower left')
plt.show()

# %%
