#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import the modules we will use
import pandas as pd
import numpy as np
import geopandas as gpd


# In[2]:


def getForecastDates():
    """Get dataframe of forecast dates from csv file.

    -------------------------------------------------
    Parameters: None

    -------------------------------------------------
    Outputs:
    forecast dates = dataframe
                     contains columns with start and end
                     dates split up into
                     year, month, and day
    """
    #  Read in the forecast dates for each week from csv
    filename = "Seasonal_Forecast_Dates.csv"
    forecast_dates = pd.read_csv(filename, skiprows=1,
                                 names=['week', 'start_date', 'end_date'])
    forecast_dates[["start_year", "start_month", "start_day"]]         = forecast_dates["start_date"].        astype(str).str.split("-", expand=True)

    # split forecast start and end dates into year, month, and day
    forecast_dates['start_year'] = forecast_dates['start_year'].astype(int)
    forecast_dates['start_month'] = forecast_dates['start_month'].astype(int)
    forecast_dates['start_day'] = forecast_dates['start_day'].astype(int)
    forecast_dates[["end_year", "end_month", "end_day"]]         = forecast_dates["end_date"].        astype(str).str.split("-", expand=True)
    forecast_dates['end_year'] = forecast_dates['end_year'].astype(int)
    forecast_dates['end_month'] = forecast_dates['end_month'].astype(int)
    forecast_dates['end_day'] = forecast_dates['end_day'].astype(int)

    return forecast_dates


# In[3]:


def forecast(x):
    """Function performing the forecast calculation, where
        x = starting value of streamflow, can be integer or float
    """
    prediction = ((model.intercept_ + model.coef_* x *increase)-2).round(2)
    print('forecast value', prediction)
    return prediction


# In[4]:


def investigate_gdp(gdp):
    """The function reads in a geodataframe
    with the intention of printing interesting
    attributes of that dataframe.

    mostly print statements

    returns the given gdp
    """

    print("Details from the given geodataframe: ", "\n")
    # initial attributes
    print("type =", type(gdp), "\n")
    print("columns =", gdp.columns, "\n")
    print("shape =", gdp.shape, "\n")
    gdp.head()
    print("\n")

    # Looking at the read-only method
    pprint(vars(gdp))
    print("geom =", gdp.geom_type, "\n")
    print("crs =", gdp.crs, "\n")
    print("spatial bounds =", gdp.total_bounds, "\n")


# In[ ]:




