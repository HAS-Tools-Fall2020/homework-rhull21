#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import json
import urllib.request as req
import urllib
from sklearn.linear_model import LinearRegression


# In[2]:


# Input start and end dates 
site = '09506000'
start = '1990-01-01'
end = '2020-11-07'

url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=" + site +       "&referred_module=sw&period=&begin_date=" + start + "&end_date=" + end
data = pd.read_table(url, skiprows=30, names=['agency_cd', 'site_no',
                                               'datetime', 'flow', 'code'],
                      parse_dates=['datetime']) 


# In[3]:


data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Aggregate flow values to weekly
flow_weekly = data.resample("W", on='datetime').mean()


# In[4]:


# Set flow_weekly to natural log 
flow_weekly_log = np.log(flow_weekly)
flow_weekly_log['flow_tm1'] = flow_weekly_log['flow'].shift(1)


# In[5]:


# Dry years for training model
train = flow_weekly_log['2017-01-01':'2019-01-01'][['flow', 'flow_tm1']]

# Fitting the model
model = LinearRegression()
x = train['flow_tm1'].values.reshape(-1, 1)
y = train['flow'].values
model.fit(x, y)

r_sq = model.score(x, y)
print('coefficient of determination:', np.round(r_sq, 2))


# In[6]:


def forecast(model, x):
    """Function performing the forecast calculation, where
        model = model used to generate prediction
            (must be a log to log scale autoregression)
        x = starting value of streamflow, can be integer or float
            (input must be in natural log scale!)

        returns: a prediction
            (note the prediction is returned in natural log scale)
            (however, the result is printed in nonlog scale)
    """
    # makes a prediction (in log space)
    prediction = (model.intercept_ + model.coef_ * x)
    # prints a prediction (in arithmetic space)
    print('forecast value', np.exp(prediction).round(2))
    # returns prediction (in log space)
    return prediction


# In[7]:

# Identify starting value for model prediction and set adjusting value
start_val = flow_weekly.flow[-1]
# starting value in natural log (needed for regression)
start_val_ln = np.log(start_val)

# create two week forecast (saved in natural log)
two_week_forecast = np.zeros(2)
for i in range(1):
    print('week 1')
    two_week_forecast[0] = forecast(model, start_val_ln)
    print('week 2')
    two_week_forecast[1] = forecast(model, two_week_forecast[0])


# %%
# QH Addition (1)
start_val = np.log(flow_weekly.flow[-1])
print('start value in log =', start_val)
print('start value in arith =', np.exp(start_val))
prediction = (model.intercept_ + model.coef_* start_val)
print('prediction in log =', prediction)
print('prediction in arith =', np.exp(prediction))

# %%
# QH Addition (2)
# Histogram of flow data in natural log space
textstr1 = '\n'.join((
                    'The flow data have',
                    'a nearly normal distribution',
                    'in log space'))
fig, ax = plt.subplots()
ax.hist(train['flow'], bins=10)
ax.set(xlabel='flow in natural log scale', ylabel='frequency', ylim=(0, 100))
ax.text(0.4, 0.95, textstr1, transform=ax.transAxes, fontsize=14,
        verticalalignment='top')
plt.show()

# Histogram of flow data in natural log space
textstr2 = '\n'.join((
                    'The flow data have',
                    'a very skewed distribution',
                    'in arithmetic space'))
fig, ax = plt.subplots()
ax.hist(np.exp(train['flow']), bins=10)
ax.set(xlabel='flow in arithmetic scale', ylabel='frequency', ylim=(0, 100))
ax.text(0.4, 0.95, textstr2, transform=ax.transAxes, fontsize=14,
        verticalalignment='top')
plt.show()

# %%
