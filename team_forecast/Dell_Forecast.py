# %%
# Import necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
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
# Prepare 2 week forecasts and plots

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

gf.hist(train['flow'])

# %%
