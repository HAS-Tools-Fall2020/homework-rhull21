# -------------------------------
# Quinn Hull
# HW 10
# 11012020
# Modified from Week9_starterscript.py
# Modified from Hull_HW09.py
# -------------------------------

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import json
import urllib.request as req
import urllib
from sklearn.linear_model import LinearRegression


# %%
# ----------------------------------------------------------------------------------
# Define functions
# ----------------------------------------------------------------------------------

def makemodel(x, y):
    """returns a multiple regression model

       using sklearn linear regression tool

       returns the model object = model
       returns the score = score

       takes 2 required variables, x and y
       x is the predictive (independent) variable(s)
       y is the predicted (dependent) variable

       both x and y need to be pandas dataframes, where x
       contains ALL of the predictive (independent) variables
       to be used.

       IMPORTANT: 'x' needs to be a list of column titles, even
       if only one predictive variable is passed

       if dimensions[x] = 1, then single predictive variable
       if dimensions[x] > 1, then multiple predictive variables

       example:
       x = train_week[['flow_tm1']] # use double brackets here
       y = train_week['flow'] # use single brackets here
       m, x = makemodel(x,y)
       """

    model = LinearRegression()
    y = y.values
    if x.shape[1] == 1:
        x = x.values.reshape(-1, 1)
    model.fit(x, y)
    score = model.score(x, y)
    return model, score


def extractmasonet(base_url, args):
    """takes
       1) a string of 'base_url'
       2) a dictionary of api arguments
       3) a string of 'token'
       specific to the metamot API

       See more about metamot:
       https://developers.synopticdata.com/mesonet/explorer/
       https://developers.synopticdata.com/about/station-variables/
       https://developers.synopticdata.com/mesonet/v2/getting-started/

       returns a dictionary
       containing the response of a JSON 'query'
       """

    # concat api arguments (careful with commas)
    apiString = urllib.parse.urlencode(args)
    apiString = apiString.replace('%2C', ',')

    # concat the API string to the base_url to create full_URL
    fullUrl = base_url + '?' + apiString
    print('full url =', fullUrl, '\n')

    # process data (use url to query data)
    # return as dictionary
    response = req.urlopen(fullUrl)
    responseDict = json.loads(response.read())

    return responseDict

def assemble_data_masonet(base_url, args, stationDiction,
                          data_join,
                          station_condition='ACTIVE',
                          station_name=False):
    """takes the basics for a data extraction
        and pulls out only the stations that meet a certain condition

        base_url = url at masonet for extraction
        args = arguments, including token and parameters
        station_Dict = a previously created response Dictionary
            of stations
        data_join = an external pandas dataset to join the data to.
            Must contain a datetime index
        station_condition = the condition used to crete response for data
            default is to look for only active stations. Only acceptable
            values are 'ACTIVE' and 'INACTIVE'
        station_name = by default FALSE. If specified a string, will
            only look for stations by the name specified.

        note by default resamples the data daily on the max

        returns a panda dataframe containint he data wanted
        """

    # 2b) Assemble all relevant dictionaries into a list, based on station name
    stationList = []
    for station in stationDict['STATION']:
        # station name and if is active
        print(station['STID'], station['STATUS'], station["PERIOD_OF_RECORD"],
              "\n")
        # time series data args
        args['stids'] = station['STID']
        # extract data from active/inactive stations
        if station['STATUS'] == station_condition:
            # if a station name is specified
            if station_name is not False:
                if (station['STID'] == station_name):
                    # extract data
                    responseDict = extractmasonet(base_url, args)
                    # create a list of all stations
                    stationList.append(responseDict)
            # if station name is not specified
            else:
                # extract data
                responseDict = extractmasonet(base_url, args)
                # create a list of all stations
                stationList.append(responseDict)

    # Checks to see if the API Call returned valid data
    if stationList[0]['SUMMARY']['RESPONSE_CODE'] == -1:
        print(stationList[0]['SUMMARY']['RESPONSE_MESSAGE'])
        return "nothing"

    # 2d) convert all data pd
    # list of keys under observations (for use in inner loop)
    for station in stationList:
        # if station id has the station_name, or station_name is False
        if (station['STATION'][0]['STID'] == station_name) or (station_name is False):
            print(station['STATION'][0]['STID'])
            for key, value in station["STATION"][0]['OBSERVATIONS'].items():
                # creates a list of value related to key
                # temp = station["STATION"][0]['OBSERVATIONS'][key]
                if (key == 'date_time'):
                    # create index
                    df = pd.DataFrame({key: pd.to_datetime(value)})
                else:
                    # concat df
                    df = pd.concat([df, pd.DataFrame({key: value})], axis=1)
            # # set index for df
            df = df.set_index('date_time')
            # resample on day
            df = df.resample('D').max()
            # join df to data dataframe
            data_join = data_join.join(df, rsuffix="_"+station['STATION'][0]['STID'])
            df = pd.DataFrame()
    return data_join


# %%
# ----------------------------------------------------------------------------------
# Import and assemble flow data
# ----------------------------------------------------------------------------------
# adjust path as necessary
site = '09506000'
start = '1989-01-01'
end = '2020-10-16'
url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on" \
      "&format=rdb&site_no="+site+"&referred_module=sw&" \
      "period=&begin_date="+start+"&end_date="+end

# read in data
data = pd.read_table(url, sep='\t', skiprows=30,
                     names=['agency_cd', 'site_no',
                            'datetime', 'flow', 'code'],
                     parse_dates=['datetime'],
                     index_col='datetime'
                     )

# re-instantiate data with just the natural log of
# its flow values (to be used later)
data = np.log(data[['flow']])
data.index = data.index.tz_localize(tz="UTC")

# %%
# # ----------------------------------------------------------------------------------
# # Mesonet import and assembly
# # ----------------------------------------------------------------------------------
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
stationDict = extractmasonet(base_url, args)

# %%
# 2) Extract time series data from active sites
# 2a) 'Base' URL
base_url_in = "https://api.synopticdata.com/v2/stations/timeseries"
arg_vars = 'air_temp,precip_accum'
arg_units = 'temp|F,precip|mm'
args_in = {
        'start': '199701010000',
        'end': '202009300000',
        'obtimezone': 'UTC',
        'vars': arg_vars,
        'stids': '',
        'units': arg_units,
        'token': mytoken}
station_condition_in = 'ACTIVE'
station_name_in = 'QVDA3'

data = assemble_data_masonet(base_url_in, args_in, stationDict,
                             data_join=data,
                             station_name=station_name_in)

# %%
# ----------------------------------------------------------------------------------
# subset data
# ----------------------------------------------------------------------------------
# 1 sumarize flow, precip, air temp on weekly basis
# (only nearest station QVDA3)
# # 1a flow stuff and save until later
# # # subset flow into data3
data3 = data[['flow']]
# # # resample
data3 = data3.resample("W").mean()
# # # lag one week
data3['flow_tm1'] = data3['flow'].shift(1)
# # # add a weekindex
data3['week'] = data3.index.weekofyear
# # # drop weeks with random values in precip, air dataset
# # # (analysis not shown)
data3 = data3[(data3['week'] > 2) & (data3['week'] != 17)]

# # 1b subset precip and air temp into data2
data2 = data[['precip_accum_set_1', 'air_temp_set_1']]
# # 1c include only data since 2010
data2 = data2[(
            (data2.index.year >= 2010)
            & (data2.index.year < 2020)
            )].dropna()
# # 1d shift precip data one
data2[['precip_accum_set_1_2']] = data2[['precip_accum_set_1']].shift(1)
# # 1e calculate amount of rain on given day 'precip accum diff'
data2['precip_accum_diff'] = data2['precip_accum_set_1'] \
                             - data2['precip_accum_set_1_2']

# 2 summarize precip and air data on weekly basis
# # 2a Add a scaler 'week' column for both data and data2
data2['week'] = data2.index.weekofyear
# # 2b group by and calculate on mean
data2 = data2.groupby('week')[['precip_accum_diff', 'air_temp_set_1']].agg(np.mean)
# # 2c drop random values
# # (analysis not shown)
data2 = data2[(data2.index > 2) & (data2.index != 17)]

# 3 join data2 (precip) and data into data3 (with flow)
data3 = data3.join(data2, on='week')


# %%
# ----------------------------------------------------------------------------------
# Build an autoregressive model
# ----------------------------------------------------------------------------------
# Step 1: pick regression variables
# Step 2: pick periods of regression (train)
# Step 3: subset data to regression (trains)
# (i) for 1 and 2 week forecast
# # description               | dates
# # (i) for 1 and 2 week forecast | 082020 : Now & 082019 : 122019
# # train_week = training data for weekly forecast
train_week = data3[(
                    (data3.index >= '2020-08-01')
                    & (data3.index <= '2020-12-31')
                    )
                    | (
                        (data3.index >= '2019-08-01')
                        & (data3.index <= '2019-12-31')
                        )]

# (ii) for semester forecast
# # description               | dates
# # (ii) for semester forecast     | year > 2010 and < 2020
# # train_semester = training data for semester forecast
train_semester = data3[(
                        (data3.index.year >= 2010)
                        & (data3.index.year < 2020)
                        )]

# # train_list = list of train_week, train_semester
train_list = [train_week, train_semester]

# # note1: this counter (c) differentiates betwen (i) and (ii)
# # in the for loops
c = 0
for t in train_list:
    # Step 4: Fit a linear regression to 'train' data using sklearn
    # # predictive variables =
    # # # 1) 'flow_tm1' (log of flow last week)
    # # # 2) 'air_temp_set_1' (mean weekly temperature, over 10 years)
    # # # 2) 'precip_accum_diff' (mean weekly preciptation, over 10 years)
    x = t[['flow_tm1',
           'air_temp_set_1',
           'precip_accum_diff']]
    # # dependent variable = 'flow' (log of flow this week)
    y = t['flow']
    # # use predifined function (makemodel) to generate model
    m, s = makemodel(x, y)

    # Step 5: Make a prediction for (i) 1 and 2 week,
    # and (ii) semester forecast

    # # week prediction (i), c = 0
    if c == 0:
        # limit to 2 weeks of model results
        j = 2
        # set lastweekflow data as most recent week of data
        x_lastweekflow = data3['flow'].iloc[-1]
        # set lastweek as most recent week
        x_lastweek = data3['week'].iloc[-1]
        print("AR Week 1 and 2 forecast prediction:")

    # # semester prediction (ii), c = 1
    else:
        # limit to 16 weeks of model results
        j = 16
        # set lastweekflow data as first week of semester
        x_lastweekflow = data3['flow'][
                                    (data3.index >= '2020-08-20') &
                                    (data3.index < '2020-08-27')
                                    ].values
        # set lastweek as first week of semester
        x_lastweek = data3['week'][
                                    (data3.index >= '2020-08-20') &
                                    (data3.index < '2020-08-27')
                                    ].values.item()
        print("AR Semester forecast prediction:")

    # # iteratively print predictions for 'j' weeks
    for i in range(j):
        # set the week i name
        name = "Week {0}:".format(i+1)
        # set last week precip variation and temperature
        x_lastweektemp = data2['air_temp_set_1'][
                                 (data2.index == x_lastweek)].values
        x_lastweekprecip = data2['precip_accum_diff'][
                                 (data2.index == x_lastweek)].values
        # predict week i flow, using flow, temperature, and precip
        x_lastweekflow = m.intercept_ + m.coef_[0] * x_lastweekflow \
                                      + m.coef_[1] * x_lastweektemp \
                                      + m.coef_[2] * x_lastweekprecip
        # print week, flow (forecast), precip and temp (predictive variables)
        print(name, "Flow (cfs) =", np.round(np.exp(x_lastweekflow), 2),
                    "Precip (mm)=", np.round(x_lastweekprecip, 2),
                    "Temp (deg F)=", np.round(x_lastweektemp, 2),
                    "Week (int; 0 = Jan01) =", x_lastweek)
        # iterate to the next week
        x_lastweek = x_lastweek + 1
    print("\n")
    # iterate to the next forecast predction
    c = + 1

# %%
