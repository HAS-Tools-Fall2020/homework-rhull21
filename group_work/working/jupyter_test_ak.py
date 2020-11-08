#!/usr/bin/env python
# coding: utf-8

# Seems okay. Maybe doesn't keep the format on cells marked Raw NB Convert in Jupyter

# In[3]:


# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
import json 
import urllib.request as req
import urllib
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# In[4]:


# Creating a function to explore specific date ranges of flow.
def flow_comparison(current, previous):
    """ This function determines the percentage decrease of flow values from
        historic to present, and is useful in adjusting forecast values.

        current - dataframe
        previous - dataframe

        It outputs a statement which is a useful supplement to looking at
        plots.
        """
    comp = (((current - previous)/previous) * 100).round(2)
    print('change of', comp, 'percent')
    return comp

# %%
# Creating a function to use the model line equation to predict one week values
def week_predict(start_val, percent_change):
    """This function will return a one-week forecast value using the
       coefficient of determination and model intercept with the user inputs.
       
       start_val - array
       percent_change - float
       
       It returns a single numpy array forecast value for an individual week.
       """
    one_week = ((model.intercept_ + model.coef_* start_val * percent_change)-2).round(2)
    print('forecast value', one_week)
    return one_week


# In[5]:


# This is the full url for the first dataset: USGS streamflow for Verde River
url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=09506000"       "&referred_module=sw&period=&begin_date=1989-01-01&end_date=2020-10-19"

# These are the desired values that can be replaced with variables 
site = '09506000'
start = '1990-01-01'
end = '2020-08-24'

# Using variables is more streamlined for changing station or date ranges
url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=" + site +       "&referred_module=sw&period=&begin_date=" + start + "&end_date=" + end
data = pd.read_table(url, skiprows=30, names=['agency_cd', 'site_no',
                                               'datetime', 'flow', 'code'],
                      parse_dates=['datetime']) #, index_col='datetime'


# In[6]:


# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Aggregate flow values to weekly
flow_weekly = data.resample("W", on='datetime').mean()


# In[ ]:





# In[7]:


# This is the second dataset: using json API to access temperature data
mytoken = '1e85cbb5763f4db39d33ab9ca6cb55a9'
#url = "https://api.synopticdata.com/v2/stations/timeseries?&token=\
 #       1e85cbb5763f4db39d33ab9ca6cb55a9&start=202010171201&end=202010251201&timeformat=\
  #      %Y%m%d&obtimezone=local&units=english&output=json&country=us&state=AZ&county=Yavapai"
base_url = "https://api.synopticdata.com/v2/stations/timeseries"

# This is a dictionary of variables that will be used to recreate the url.
args = {
    'start': '201810010000', 
    'end': '202008240000',
    'obtimezone': 'UTC',
    'vars': 'air_temp',
    'stids': 'QVDA3',
    'units': 'temp|F,precip|mm',
    'token': mytoken} 
# %%
# This generates the revised url with variables
apiString = urllib.parse.urlencode(args)
fullUrl = base_url + '?' + apiString


# In[8]:


# This accesses the API formatting
response = req.urlopen(fullUrl)
responseDict = json.loads(response.read())

# %%
# We can get to the data we want like this: 
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']

# Not sure where the 'air_temp_set_1' comes from
airT = responseDict['STATION'][0]['OBSERVATIONS']['air_temp_set_1']

# Combine this into a pandas dataframe
data2 = pd.DataFrame({'Temperature': airT}, index=pd.to_datetime(dateTime))

# Now convert this to daily data using resample
data2_daily = data2.resample('D').mean()
# Convert to weekly values
data2_weekly = data2.resample('W').mean()

# %%
# A one year plot of weekly temperature values
fig, ax = plt.subplots()
ax.plot(data2_weekly.loc['2019-10-24':'2020-10-24'])
#ax.plot(flow_weekly.flow['2019-10-24':'2020-10-24'])
ax.set(title = 'Weekly Air Temp. Oct. 2019-2020', xlabel = 'Date',
       ylabel = 'degrees (F)')
ax.legend()
fig.show()

# %%
# Plotting weekly flow and weekly temp with shared x axis

ax1 = plt.subplot(311)
plt.plot(flow_weekly.flow['2019-10-24':'2020-10-24'])
plt.setp(ax1.get_xticklabels())
ax1.set(title = 'Weekly Flow Oct. 2019-2020', ylabel = 'Flow (cfs)')
ax2 = plt.subplot(313, sharex=ax1)
plt.plot(data2_weekly.loc['2019-10-24':'2020-10-24'],color='red')
ax2.set(title = 'Weekly Temp. Oct. 2019-2020', ylabel = 'Degrees (F)')
ax.legend()
fig.show()

# A two month plot of aggregated streamflow and temp
fig, ax = plt.subplots()
ax.plot(data2_weekly.loc['2020-09-01':'2020-10-24'], label = 'temp')
ax.plot(flow_weekly.flow['2020-09-01':'2020-10-24'], label = 'flow')
ax.set(title = 'Weekly Air Temp. and Flow Sept-Oct 2020', xlabel = 'Date (month, day)',
       ylabel = 'degrees (F) flow (cfs)')
date_form = DateFormatter("%m-%d")
ax.xaxis.set_major_formatter(date_form)
ax.legend()
fig.show()

# In[11]:


# Building an autoregressive model
# Setting up arrays to be used for the model
flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)
flow_weekly['flow_tm2'] = flow_weekly['flow'].shift(2)


# %%
# Selecting a date range of interest for detailed comparison.
oct_2019 = flow_weekly[(flow_weekly.year == 2019) & (flow_weekly.month == 10) & (flow_weekly.day <= 17)]
oct_2020 = flow_weekly[(flow_weekly.year == 2020) & (flow_weekly.month == 9) & (flow_weekly.day <= 17)]

# %%
# Utilizing the new function to inform the percent decrease chosen for my
# forecast calculations
#weeks = np.zeros(3)
#for i in range(3):   
 #   weeks[i] = flow_comparison(oct_2020.flow[i], oct_2019.flow[i])


# In[12]:


# Jan 2017 through Jan 2019 for training, based on the relevance
# of recent history and the coefficient of determination produced
train = flow_weekly['2017-01-01':'2019-01-01']
[['flow', 'flow_tm1', 'flow_tm2']]
test = flow_weekly['2019-01-01':'2020-08-24'][['flow', 'flow_tm1', 'flow_tm2']]

# %%
# Fitting a linear regression model using sklearn
model = LinearRegression()
x = train['flow_tm1'].values.reshape(-1, 1)
y = train['flow'].values
model.fit(x, y)

# This shows the results of the model calculations
r_sq = model.score(x, y)
print('coefficient of determination:', np.round(r_sq, 2))
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))


# In[13]:


# This predicts the model response for a  given flow value
q_pred_train = model.predict(train['flow_tm1'].values.reshape(-1, 1))
q_pred_test = model.predict(test['flow_tm1'].values.reshape(-1, 1))

# %%
# Plotting training and observed flow from training start date
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], color='green', label='full date range')
ax.plot(train['flow'], '2', color='red', label='training period')
ax.set(title="Observed Flow", xlabel='Date',
       ylabel="Weekly Avg Flow [cfs]",
       yscale='log', xlim=[datetime.date(2017, 1, 1),
                           datetime.date(2020, 10, 3)])
ax.legend()


# In[14]:


# Using the most recent shifted flow value as a starting point for 
# autoregressive one and two week forecast values
start_val = flow_weekly.flow_tm1.tail(1)

AR_one = (model.intercept_ + model.coef_ * start_val).round(2).values
print(AR_one, 'is the AR model value for my one week prediction')
AR_two = (model.intercept_ + model.coef_ * AR_one).round(2)
print(AR_two, 'is the AR model value for my two week prediction')

# %%
# Calculations for my official one and two week predictions
decrease_by = .50
one_week = ((model.intercept_ + model.coef_ * start_val*decrease_by)-2).round(2).values
two_week = ((model.intercept_ + model.coef_ * one_week*decrease_by)-2).round(2)
print('One week official forecast:', one_week,'Two week official forecast:', two_week)


# In[ ]:






# %%
week_predict(start_val, percent_change)


# MAKE A LOOP FOR THE CELL ABOVE, TWO WEEK FORECAST
two_week = np.zeros(2)
aug = 2
for i in range(aug):
    two_week[i] = 


weeks = np.zeros(3)
for i in range(3):   
    weeks[i] = flow_comparison(oct_2020.flow[i], oct_2019.flow[i])



# In[ ]:




