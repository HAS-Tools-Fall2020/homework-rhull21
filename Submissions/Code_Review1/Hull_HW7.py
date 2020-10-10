# ----------------------------------------------------------------------------------
# Assignment 7
# Robert Hull
# 10092020

# QH - modified from
# Week 6 HW submission
# ----------------------------------------------------------------------------------

# %%
# ----------------------------------------------------------------------------------
# Import modules
# ----------------------------------------------------------------------------------
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# may need to pip install scikit-learn, not available on conda
from sklearn.linear_model import LinearRegression
import datetime
import time

# %%
# ----------------------------------------------------------------------------------
# Import functions
# ----------------------------------------------------------------------------------


def makemodel(x, y):
    """
    function creates multiple regression model
    using sklearn linear regression tool

    returns the model object = model
    returns the score = score

    takes 2 required variables, x and y both dataframes

    if dimensions[x] = 1, then single predictive variable
    if dimensions[x] > 1, then multiple predictive variables
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
# Import data
# ----------------------------------------------------------------------------------
# adjust path as necessary
filename = 'streamflow_week7.txt'
filepath = os.path.join('../../data', filename)
print(os.getcwd())
print(filepath)


# %%
# ----------------------------------------------------------------------------------
# Read in data
# ----------------------------------------------------------------------------------
data = pd.read_table(filepath, sep='\t', skiprows=30,
                     names=['agency_cd', 'site_no',
                            'datetime', 'flow', 'code'],
                     parse_dates=['datetime']
                     )

# Aggregate flow data on weekly (flow_W), and monthly (flowm) basis
l_time = ["w", "m"]
for j in range(len(l_time)):
    nm = "flow{0}".format(l_time[j])
    exec(f'flow{l_time[j]} = data.resample(l_time[j], on="datetime").mean()')

# %%
# ----------------------------------------------------------------------------------
# Build an autoregressive model
# ----------------------------------------------------------------------------------

# Step 1: setup the arrays of lagged data (month and week)
# and merge them so they are available together
for i in range(1, 4):
    nm = "flow_tm{0}".format(i)
    floww[nm] = floww['flow'].shift(i)
    flowm[nm] = flowm['flow'].shift(i)

# merge monthly and weekly together
# note _x = weekly flow, _y = monthly, _sqrt = square root
floww = pd.merge_asof(floww, flowm[['flow', 'flow_tm1', 'flow_tm2',
                      'flow_tm3']], left_index=True, right_index=True,
                      direction="nearest")
floww = floww.join(np.log(floww), rsuffix='_sqrt')

# %%
# Step 2: pick periods of regression (train) and prediction (test)
# 4 scenarios: (see below)
# # train           |          test
# # 082020 : Now    |  082010 : 082015
# # 082019 : Now    |  082010 : 082015
# # 082015 : Now    |  082010 : 082015
# # 082015 : 08219    |  082019 : Now

# make date range to be used to make test and train periods
d_list = [datetime.date(2020, 8, 1), datetime.date(
    2019, 8, 1), datetime.date(2015, 8, 1), datetime.date(2010, 8, 1)]
loc_list = []
for date in d_list:
    loc_list.append(floww.index.get_loc(date, method='nearest'))

# create test and train periods from loc_list
train_list = []
test_list = []
for i in range(3):
    train_list.append(floww.iloc[loc_list[i]:-1])
    test_list.append(floww.iloc[loc_list[-1]:loc_list[1]])
train_list.append(floww.iloc[loc_list[2]:loc_list[1]])
test_list.append(floww.iloc[loc_list[1]:-1])


# %%
# ----------------------------------------------------------------------------------
# Run, assess, and visualize an autoregressive model
# ----------------------------------------------------------------------------------
# Step 3: Fit a linear regression model using sklearn
# Step 4: Assess quality of fit
# Step 5: Visualize output

# regression predictive variable scenarios n = 5
# variables: 1 week, 1 week & 2 week, 1 week & 1 month, 1 week square root,
# 1 week & 1 week square root & 1 month
reg_list = [['flow_tm1_x'], ['flow_tm1_x', 'flow_tm2_x'], [
    'flow_tm1_x', 'flow_tm1_y'], ['flow_tm1_x_sqrt'], [
    'flow_tm1_x', 'flow_tm1_x_sqrt', 'flow_tm1_y']]

# loop through all regression and train/test scenarios
for reg in reg_list:
    for i in range(len(train_list)):
        # 3) fit a linear regression
        train = train_list[i]
        test = test_list[i]
        x = train[reg]
        y = train['flow_x']
        m, s = makemodel(x, y)

        time.sleep(1)

        # 4a) assess quality of fit
        print(reg)
        print("From ", train.index.min(), " to ", train.index.max())
        print('coefficient of determination:', np.round(s, 2))
        print('intercept:', np.round(m.intercept_, 2))
        print('slope:', np.round(m.coef_, 2))
        print("\n")

        # 4b) make a 'test' prediction, first with train and then test
        y_p_train = m.predict(x)
        x_p = test[reg]
        y_p_test = m.predict(x_p)

        # 5) visualize output(s)
        # plot fit of model on autoregressed (train) data
        fig, ax = plt.subplots()
        ax.plot(train['flow_x'], color='grey', linewidth=2, label='observed')
        ax.plot(train.index, y_p_train, color='green', linestyle='--',
                label='simulated')
        ax.set(title="Observed Flow, Train", xlabel="Date",
               ylabel="Weekly Avg Flow [cfs]", yscale='log')
        ax.legend()
        plt.show()

        print("\n")
        # plot fit of model on observed, but not regressed (test) data
        fig, ax = plt.subplots()
        ax.plot(test['flow_x'], color='blue', linewidth=2, label='observed')
        ax.plot(test.index, y_p_test, color='orange', linestyle='--',
                label='simulated')
        ax.set(title="Observed Flow, Test", xlabel="Date",
               ylabel="Weekly Avg Flow [cfs]", yscale='log')
        ax.legend()
        plt.show()

        print("\n")
        print("\n")

# %%
# ----------------------------------------------------------------------------------
# Weekly Forecast
# ----------------------------------------------------------------------------------
# Use simple model
train = train_list[0]
reg = reg_list[0]
x = train[reg]
y = train['flow_x']
m, s = makemodel(x, y)

# make prediction for next week and the week after
x_p = train['flow_x'].iloc[-1]
y_p_w1 = m.intercept_ + m.coef_ * x_p
y_p_w2 = m.intercept_ + m.coef_ * y_p_w1

# weekly predictions from model
print("Model Results of Weekly Predictions")
print(round(y_p_w1[0], 2), ", ", round(y_p_w2[0], 2))
print("\n")

# weekly predictions preferred
print("Weekly Predictions to push to gitub")
print(round(y_p_w1[0], 2) + 5, ", ", round(y_p_w2[0], 2) + 10)
print("\n")

# %%
