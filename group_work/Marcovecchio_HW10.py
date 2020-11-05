# %%
# Import the modules we will use
import pandas as pd
import json
import matplotlib.pyplot as plt
import urllib.request as req


# %%
# Read the data into a pandas dataframe
url_usgs = 'https://waterdata.usgs.gov/nwis/dv?cb_00060=on' \
           '&format=rdb&site_no=09506000&referred_module=sw' \
           '&period=&begin_date=1989-01-01&end_date=2020-11-01'

data = pd.read_table(url_usgs, skiprows=30, names=['agency_cd', 'site_no',
                                                   'datetime', 'flow', 'code'],
                     parse_dates=['datetime'])

# print(data.info())

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Aggregate flow values to weekly
flow_weekly = data.resample("W", on='datetime').mean()

# %%
# Mesonet Data Input
start_meso = '20201018'
stop_meso = '20201101'
my_token = '65e9ee97251c4df881c319b8d639981c'

meso_url = 'https://api.synopticdata.com/v2/stations/precip?'\
           'stid=ksez&start=' + start_meso + '0000&end=' + \
           stop_meso + '0000&pmode=intervals&interval=day&' \
           'token=' + my_token

# open mesonet URL
meso_page = req.urlopen(meso_url)

# make dictionary from mesonet API
meso_dict = json.loads(meso_page.read())
# get keys
print(meso_dict['STATION'][0]['OBSERVATIONS']['precipitation'][0].keys())

# ----- get dates and precipitation totals -----

# make temporary dataframe index w/ same number of entries a data
ct = range(14)
# create dataframe using temporary index
meso_data = pd.DataFrame(meso_dict['STATION'][0]
                         ['OBSERVATIONS']['precipitation'],
                         index=ct)
# convert first report column into datetime format
meso_data['first_report'] = pd.to_datetime(meso_data['first_report'],
                                           format='%Y-%m-%dT%H:%M:%SZ')
# make column of dates w/o time stamp
meso_data['date'] = pd.DatetimeIndex(meso_data['first_report']).date
# set the column of dates as permanent index to the dataframe
meso_data.index = meso_data['date']


# %%
# Make Plots!

# Plot daily streamflow
fig, ax = plt.subplots()
ax.plot(data['datetime'].tail(14), data['flow'].tail(14), color='C0')
ax.set(title="Streamflow from Past Two Weeks",
       xlabel="Date", ylabel="Daily Flow [cfs]")
ax.legend()
fig.set_size_inches(10, 6)

# Plot daily precip
fig, bx = plt.subplots()
bx.plot(meso_data['total'], color='violet')
bx.set(title="Precipitation at Sedona, AZ from Past Two Weeks",
       xlabel="Date", ylabel="Rainfall mm/hr")
bx.legend()
fig.set_size_inches(10, 6)

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


# get averages for forecasting based on dates for each
# forecasting week of the semester

# LC - This is something you could put into a loop.
# you would just have to define the the months and days
# as lists outside your loop

# Week 1: 8/24-8/30
wk1mean = data_16wk[(data_16wk.month == 8) & (data_16wk.day >= 24) &
                    (data_16wk.day <= 30)].flow.mean()

# Week 2: 8/31-9/6
wk2mean = data_16wk[((data_16wk.month == 8) & (data_16wk.day == 31)) |
                    ((data_16wk.month == 9) &
                    (data_16wk.day >= 1) & (data_16wk.day <= 6))].flow.mean()

# Week 3: 9/7-9/13
wk3mean = data_16wk[(data_16wk.month == 9) &
                    (data_16wk.day >= 7) & (data_16wk.day <= 13)].flow.mean()

# Week 4: 9/14-9/20
wk4mean = data_16wk[(data_16wk.month == 9) &
                    (data_16wk.day >= 14) & (data_16wk.day <= 20)].flow.mean()

# Week 5: 9/21-9/27
wk5mean = data_16wk[(data_16wk.month == 9) &
                    (data_16wk.day >= 21) & (data_16wk.day <= 27)].flow.mean()

# Week 6: 9/28-10/4
wk6mean = data_16wk[((data_16wk.month == 9) &
                    (data_16wk.day >= 28) & (data_16wk.day <= 30)) |
                    ((data_16wk.month == 10) &
                    (data_16wk.month >= 1) & (data_16wk.month <= 4))
                    ].flow.mean()

# Week 7: 10/5-10/11
wk7mean = data_16wk[(data_16wk.month == 10) &
                    (data_16wk.day >= 5) & (data_16wk.day <= 11)].flow.mean()

# Week 8: 10/12-10/18
wk8mean = data_16wk[(data_16wk.month == 10) &
                    (data_16wk.day >= 12) & (data_16wk.day <= 18)].flow.mean()

# Week 9: 10/19-10/25
wk9mean = data_16wk[(data_16wk.month == 10) &
                    (data_16wk.day >= 19) & (data_16wk.day <= 25)].flow.mean()

# Week 10: 10/26-11/1
wk10mean = data_16wk[((data_16wk.month == 10) &
                     (data_16wk.day >= 26) & (data_16wk.day <= 31)) |
                     ((data_16wk.month == 11) & (data_16wk.day == 1))
                     ].flow.mean()

# Week 11: 11/2-11/8
wk11mean = data_16wk[(data_16wk.month == 11) &
                     (data_16wk.day >= 2) & (data_16wk.day <= 8)].flow.mean()

# Week 12: 11/9-11/15
wk12mean = data_16wk[(data_16wk.month == 11) &
                     (data_16wk.day >= 9) & (data_16wk.day <= 15)].flow.mean()

# Week 13: 11/16-11/22
wk13mean = data_16wk[(data_16wk.month == 11) &
                     (data_16wk.day >= 16) & (data_16wk.day <= 22)].flow.mean()

# Week 14: 11/23-11/29
wk14mean = data_16wk[(data_16wk.month == 11) &
                     (data_16wk.day >= 23) & (data_16wk.day <= 29)].flow.mean()

# Week 15: 11/30-12/6
wk15mean = data_16wk[((data_16wk.month == 11) & (data_16wk.day == 30)) |
                     ((data_16wk.month == 12) &
                     (data_16wk.day >= 1) & (data_16wk.day <= 6))].flow.mean()

# Week 16: 12/7-12/13
wk16mean = data_16wk[(data_16wk.month == 12) &
                     (data_16wk.day >= 7) & (data_16wk.day <= 13)].flow.mean()


# Put each week's forecast into a comma separated list
forecasts = [wk1mean, wk2mean, wk3mean, wk4mean,
             wk5mean, wk6mean, wk7mean, wk8mean,
             wk9mean, wk10mean, wk11mean, wk12mean,
             wk13mean, wk14mean, wk15mean, wk16mean]
print('Weekly Forecasts:', forecasts)

# %%
