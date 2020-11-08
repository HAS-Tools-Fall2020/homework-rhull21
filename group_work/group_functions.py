#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import the modules we will use
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt


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


def single_forecast(model, x):
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

# %% functions


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

# %%

def add_pt_gdf(point_l, crs_i, gpd_in, nm_pts):
    """The function reads in a numpy array of one or multiple spatial data values
    with the intention of converting that into a pandas dataframe
    and then appending this to the end of an existing pandas geodataframe

    inputs:
    point_l = a 2-D numpy array of spatial data values (like easting, northing)
        or (like lat, long)
    crs_in = the coordinate system of the dataframe, a crs object
    gpd_in = the pandas dataframe containing geodataframe info
    nm_pts = the name you would like to give the new row in the dataframe

    output:
    the inputted pandas dataframe container of gdp and other info
    with a new record containing a gdp oflat / long data
    """

    # make these into spatial features
    point_geom = [Point(xy) for xy in point_l]

    # create point_df geodataframe
    point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                                crs=crs_i)

    # add to gpd_df
    gpd_in = gpd_in.append({'names': nm_pts,
                            'file': '', 'gpd': point_df},
                           ignore_index=True)

    return gpd_in


# In[ ]:


def hist(data_in):
    """This function generates two histograms based on the input of a dataset of
    streamflow stored in natural log format

    Abigail, put in train['flow']

    data_in = a series from a pandas dataframe containing streamflow data in log

    shows two histograms, one of the data represented in log space and
    the other represented in arithmetic space

    the purpose is to show how doing your autoregression with 'log' data helps
    to normalize the underlying data, and generate better fits to training data

    returns nothing

    """
    # Histogram of flow data in natural log space
    textstr1 = '\n'.join((
                        'The flow data have',
                        'a nearly normal distribution',
                        'in log space'))
    fig, ax = plt.subplots()
    ax.hist(data_in, bins=10)
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
    ax.hist(np.exp(data_in), bins=10)
    ax.set(xlabel='flow in arithmetic scale', ylabel='frequency', ylim=(0, 100))
    ax.text(0.4, 0.95, textstr2, transform=ax.transAxes, fontsize=14,
            verticalalignment='top')
    plt.show()

