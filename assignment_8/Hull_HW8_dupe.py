# ----------------------------------------------------------------------------------
# Assignment 7
# Robert Hull
# 10092020

# QH - modified from
# Week 6 & 7 HW submission
# incorporates feedback from Scott
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
# Define functions
# ----------------------------------------------------------------------------------
def makemodel(x, y):
    """
    function creates multiple regression model
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

#%%
# ----------------------------------------------------------------------------------
# Import and assemble data
# ----------------------------------------------------------------------------------
# adjust path as necessary
filename = 'streamflow_week7.txt'
filepath = os.path.join('../../data', filename)
print(os.getcwd())
print(filepath)

# read in data
data = pd.read_table(filepath, sep='\t', skiprows=30,
                     names=['agency_cd', 'site_no',
                            'datetime', 'flow', 'code'],
                     parse_dates=['datetime']
                     )

# Aggregate flow data on weekly (flow_w) basis
flow_w = data.resample("W", on="datetime").mean()

# setup array of lagged data
flow_w['flow_tm1'] = flow_w['flow'].shift(1)

# re-instantiate flow_w with just the natural log of its flow values (to be used later)
flow_w = np.log(flow_w[['flow', 'flow_tm1']])

#%%
# ----------------------------------------------------------------------------------
# Build an autoregressive model
# ----------------------------------------------------------------------------------
# Step 1: pick regression variables
# # predictive variable = 'flow_tm1' (log of flow last week)
# # dependent variable = 'flow' (log of flow this week)

# Step 2: pick periods of regression
# # description               | dates
# # (i) for 1 and 2 week forecast | 082020 : Now & 082019 : 122019
# # (ii) for semester forecast     | year > 2010 and < 2020

# Step 3: subset data to regression (trains)
# # train_week = training data for weekly forecast
# # train_semester = training data for semester forecast
# # train_list = list of train_week, train_semester

# (i) for 1 and 2 week forecast
train_week = flow_w[(
                    (flow_w.index >= '2020-08-01') & 
                    (flow_w.index <= '2020-12-31')
                    )
                    | (
                        (flow_w.index >= '2019-08-01') & 
                        (flow_w.index <= '2019-12-31')
                        )
                    ]
# (ii) for semester forecast
train_semester= flow_w[(
                        (flow_w.index >= '2010') & 
                        (flow_w.index < '2020')
                        )
                        ]
train_list = [train_week, train_semester]


# Step 4: Fit a linear regression to 'train' data using sklearn
# Step 5: Make a prediction for (i) 1 and 2 week, and (ii) semester forecast
# # note1: this counter will help with ifs later
c = 0 

for t in train_list:
    # Step 4: fit linear regression
    x = t[['flow_tm1']]
    y = t['flow']
    m, s = makemodel(x, y)

    # Step 5: make a prediction
    # # note1: this code will behave differently for
    # # (i) week and (ii) semester forecasts, 
    # # hence the if statement.

    # # week prediction (i), c = 0
    if c == 0:
        j = 2
        x_lastweek = flow_w['flow'].iloc[-1]
        print("AR Week 1 and 2 forecast prediction:")
        
    # # semester prediction (ii), c = 1
    else: 
        j = 16
        x_lastweek = flow_w['flow'][(flow_w.index >= '2020-08-20') & (flow_w.index < '2020-08-27')].values
        print("AR Semester forecast prediction:")

    # # iteratively print predictions
    for i in range(j):
        name = "Week {0} = ".format(i+1)
        x_lastweek = m.intercept_ + m.coef_ * x_lastweek
        print(name, np.round(np.exp(x_lastweek),2))

    print("\n")
    c =+ 1
