# %%
# Import the modules we will use
import pandas as pd
import numpy as np


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

#  Read in the forecast dates for each week from csv
filename = "Seasonal_Forecast_Dates.csv"
forecast_dates = pd.read_csv(filename, skiprows=1,
                             names=['week', 'start_date', 'end_date'])
forecast_dates[["start_year", "start_month", "start_day"]] \
              = forecast_dates["start_date"].\
              astype(str).str.split("-", expand=True)

# split forecast start and end dates into year, month, and day
forecast_dates['start_year'] = forecast_dates['start_year'].astype(int)
forecast_dates['start_month'] = forecast_dates['start_month'].astype(int)
forecast_dates['start_day'] = forecast_dates['start_day'].astype(int)
forecast_dates[["end_year", "end_month", "end_day"]] \
              = forecast_dates["end_date"].\
              astype(str).str.split("-", expand=True)
forecast_dates['end_year'] = forecast_dates['end_year'].astype(int)
forecast_dates['end_month'] = forecast_dates['end_month'].astype(int)
forecast_dates['end_day'] = forecast_dates['end_day'].astype(int)

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
print(driest.year[0])

# make a dataframe that only contains data from the driest years
dry_years_data = data_16wk[(data_16wk.year == driest.year[0]) |
                           (data_16wk.year == driest.year[1])]

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
