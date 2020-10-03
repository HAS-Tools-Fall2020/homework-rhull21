# Assignment 6
# Robert Hull
# 10022020

# QH - modified from
# Starter code for week 6 illustrating how to build an AR model 
# and plot it

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
#note you may need to do pip install for sklearn

# %%
# Set the file name and path to where you have stored the data
filename = 'streamflow_week6.txt'
filepath = os.path.join('../data', filename)
print(os.getcwd())
print(filepath)


# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code'],
        parse_dates=['datetime']
        )

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Aggregate flow values to weekly 
## a) QH ADDED: 3T and M (3 days, and monthly)
flow_weekly = data.resample("W", on='datetime').mean()
flow_thrice = data.resample("3D", on='datetime').mean()
flow_month = data.resample("M", on='datetime').mean()

# %%
# Building an autoregressive model 
# You can learn more about the approach I'm following by walking 
# Through this tutorial
# https://realpython.com/linear-regression-in-python/

# Step 1: setup the arrays you will build your model on
# This is an autoregressive model so we will be building
# it based on the lagged timeseries

## b) QH ADDED: logs for 3T and monthly data, add a .shift(3) for each
flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)
flow_weekly['flow_tm2'] = flow_weekly['flow'].shift(2)
flow_weekly['flow_tm3'] = flow_weekly['flow'].shift(3)

flow_thrice['flow_tm1'] = flow_thrice['flow'].shift(1)
flow_thrice['flow_tm2'] = flow_thrice['flow'].shift(2)
flow_thrice['flow_tm3'] = flow_thrice['flow'].shift(3)

flow_month['flow_tm1'] = flow_month['flow'].shift(1)
flow_month['flow_tm2'] = flow_month['flow'].shift(2)
flow_month['flow_tm3'] = flow_month['flow'].shift(3)

# %%
# Step 2 - pick what portion of the time series you want to use as training data
# here I'm grabbing the first 800 weeks 
# Note1 - dropping the first two weeks since they wont have lagged data
# to go with them  

# c) QH ADDED: subsample 'train' through 2015 (iloc 1305 for flow_weekly) to capture
# c) cont. Need to figure out how to better capture the lower values in our prediction
# some of the more recent 'drought' data in developing our regression

i = 1305
train = flow_weekly[3:i][['flow', 'flow_tm1', 'flow_tm2', 'flow_tm3']]
test = flow_weekly[i:][['flow', 'flow_tm1', 'flow_tm2', 'flow_tm3']]

# i = 3167
# train = flow_thrice[3:i][['flow', 'flow_tm1', 'flow_tm2', 'flow_tm3']]
# test = flow_thrice[i:][['flow', 'flow_tm1', 'flow_tm2', 'flow_tm3']]

# i = 312
# train = flow_month[3:i][['flow', 'flow_tm1', 'flow_tm2', 'flow_tm3']]
# test = flow_month[i:][['flow', 'flow_tm1', 'flow_tm2', 'flow_tm3']]



# %%
# Another example but this time using two time lags as inputs to the model 
# multiple variable linear regression


# d) decided to a logarithmic regression
# including the first, second, and third time shifts
# for weekly data only

# e) use multiple regression using built in sklearn
model2 = LinearRegression() # from sklearn.linear_model 
x2=np.log(train[['flow_tm1','flow_tm2', 'flow_tm3']])
y= np.log(train['flow'].values)
model2.fit(x2,y)
r_sq = model2.score(x2, y)
print('coefficient of determination:', np.round(r_sq,2))
print('intercept:', np.round(model2.intercept_, 2))
print('slope:', np.round(model2.coef_, 2))

q_pred_train = model2.predict(train[['flow_tm1','flow_tm2','flow_tm3']])
q_pred_test = model2.predict(test[['flow_tm1','flow_tm2','flow_tm3']])


# %% 
# f) QH ADDED: Changed the coloring of this
plt.style.use('seaborn')
# 1. Timeseries of observed flow values
# Note that date is the index for the dataframe so it will 
# automatically treat this as our x axis unless we tell it otherwise
fig, ax = plt.subplots()
ax.plot(data['datetime'],data['flow'], label='full data set')
ax.plot(flow_weekly['flow'], label='resampled')
ax.plot(train['flow'], label='portion to make prediction')
ax.set(title="Observed Flow vs. Resampled Flow", xlabel="Date", 
        ylabel="Weekly Avg Flow [cfs]",
        yscale='log')
ax.legend()

# an example of saving your figure to a file
fig.set_size_inches(5,3)
fig.savefig("Observed_Flow_v_resampled_flow.png")

# %%
#2. Time series of flow values with the x axis range limited
fig, ax = plt.subplots()

ax.plot(data['datetime'],data['flow'], label='full data set')
ax.plot(flow_weekly['flow'], label='resampled')
ax.plot(flow_weekly['flow_tm1'],  label='resampled, 1 shift')
ax.plot(flow_weekly['flow_tm2'],  label='resampled, 2 shift')
ax.plot(flow_weekly['flow_tm3'],  label='resampled, 3 shift')

ax.set(title="Observed Flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        yscale='log', xlim=[datetime.date(2016,1,1), datetime.date(2017, 1, 1)])
ax.legend()

fig.set_size_inches(5,3)
fig.savefig("time_shifts.png")

# %% 
# 3. Line  plot comparison of predicted and observed flows
fig, ax = plt.subplots()

ax.plot(train['flow'], color='grey', linewidth=2, label='resampled-observed')
ax.plot(train.index, q_pred_train, color='green', linestyle='--', 
        label='simulated')
ax.plot(test['flow'], color='red', linewidth=2, label='resampled-observed')
ax.plot(test.index, q_pred_test, color='blue', linestyle='--', 
        label='simulated')


ax.set(title="Observed Flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        yscale='log')
ax.legend()

fig.set_size_inches(5,3)
fig.savefig("simulation.png")

# %% 
# 4. Scatter plot of t vs t-1 flow with log log axes
plt.style.use('classic')

fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='p',
              color='blueviolet', label='obs')
ax.set(xlabel='flow t-1', ylabel='flow t', yscale='log', xscale='log')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model')
ax.legend()

fig.set_size_inches(5,3)
fig.savefig("log-scale-comp.png")

# %% 
# 5. Scatter plot of t vs t-1 flow with normal axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='p',
              color='blueviolet', label='observations')
ax.set(xlabel='flow t-1', ylabel='flow t')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model')
ax.legend()

fig.set_size_inches(5,3)
fig.savefig("comp.png")

# %%
# Forecast

# weekly predictions
f1 = flow_weekly['flow'].iloc[1657]
f2 = flow_weekly['flow_tm1'].iloc[1657]
f3 = flow_weekly['flow_tm2'].iloc[1657]
flor_arr = np.array([f1,f2,f3]).reshape(1,-1)

# # next weeks flow
r1 = model2.predict(flow_arr)
flor_arr = np.array([r1,f1,f2]).reshape(1,-1) 
# next next weeks flow
r2 = model2.predict(flor_arr)

print(r1, r2)


# %%

# long term prediction
f1 = flow_weekly['flow'].iloc[1652]
f2 = flow_weekly['flow_tm1'].iloc[1652]
f3 = flow_weekly['flow_tm2'].iloc[1652]
flor_arr = np.array([f1,f2,f3]).reshape(1,-1)

# predict week 1, add to array
for i in range (0,14): 
    r = model2.predict(flor_arr[i:i+3].reshape(1,-1))
    flor_arr = np.append(flor_arr,r)

# array([54.        , 37.77142857, 35.        , 45.48883514, 33.41081847,
#        30.21233972, 38.47130065, 29.53062407, 26.24714091, 32.68814316,
#        26.10616459, 22.94783823, 27.92328735, 23.10491884, 20.19121979,
#        23.99733032, 20.49025687])




# %%
pred = round(flow_weekly[['flow']].iloc[1599:1599+16],2)
# %%
