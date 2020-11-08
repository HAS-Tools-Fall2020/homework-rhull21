# -------------------------------
# Group Name: ????
# Source Forecast Codde
# 11032020
# Modified from Week9_starterscript.py
# Modified from Hull_HW09.py
# Modified from Hull_HW10.py
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


# %%
# ----------------------------------------------------------------------------------
# Import and assemble flow data
# ----------------------------------------------------------------------------------
# adjust path as necessary
site = '09506000'
start = '1989-01-01'
end = '2020-12-31'
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
# resample
data = data.resample("W").mean()
# lag one week
data['flow_tm1'] = data['flow'].shift(1)

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
train_week = data[(
                    (data.index >= '2020-08-01')
                    & (data.index <= '2020-12-31')
                    )
                    | (
                        (data.index >= '2019-08-01')
                        & (data.index <= '2019-12-31')
                        )]

# (ii) for semester forecast
# # description               | dates
# # (ii) for semester forecast     | year > 2010 and < 2020
# # train_semester = training data for semester forecast
train_semester = data[(
                        (data.index.year >= 2010)
                        & (data.index.year < 2020)
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
    x = t[['flow_tm1']]
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
        x_lastweekflow = data['flow'].iloc[-1]
        print("AR Week 1 and 2 forecast prediction:")

    # # semester prediction (ii), c = 1
    else:
        # limit to 16 weeks of model results
        j = 16
        # set lastweekflow data as first week of semester
        x_lastweekflow = data['flow'][
                                    (data.index >= '2020-08-20') &
                                    (data.index < '2020-08-27')
                                    ].values
        print("AR Semester forecast prediction:")

    # # iteratively print predictions for 'j' weeks
    for i in range(j):
        # set the week i name
        name = "Week {0}:".format(i+1)
        # predict week i flow, using flow
        x_lastweekflow = m.intercept_ + m.coef_[0] * x_lastweekflow
        # print week, flow (forecast), precip and temp (predictive variables)
        print(name, np.round(np.exp(x_lastweekflow), 2))
    print("\n")
    # iterate to the next forecast predction
    c = + 1

# %%
