# ----------------------
# Modifed from Hull_HW12.py
# 11162020
# Functions to be used by Hull_HW12.py
# ----------------------

# %%
# ----------------------------------------------------------------------------------
# Define modules
# ----------------------------------------------------------------------------------
import pandas as pd
# import geopandas as gpd
import numpy as np
import json
import urllib.request as req
import urllib
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler


# %%
# ----------------------------------------------------------------------------------
# Define functions
# ----------------------------------------------------------------------------------
def clean_dataset(df):
    """Removes all infinity, nan, and numbers out of range
    from: https://stackoverflow.com/questions/31323499/
    sklearn-error-valueerror-input-contains-nan-infinity-or-a-value-too-large-for
    """
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)


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
    print(type(y))
    print(type(x))
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


def assemble_data_masonet(base_url, args, stationDict,
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
        if (station['STATION'][0]['STID'] == station_name) or \
                            (station_name is False):
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
            data_join = data_join.join(df,
                                       rsuffix="_"+station['STATION'][0]['STID'
                                                                         ])
            df = pd.DataFrame()
    return data_join


def Kelvin_2_Faren(K_temp):
    """takes a temperature in Kelvin

    returns a temperature in Fareignheit
        """
    return (K_temp - 273.15)*(9/5) + 32


def norm_it(startdate, enddate, dfin, dfname, l_back=1):
    """
    This function noramlizes a column of data from a pandas dataframe
    using the MinMaxScaler feature of sklearn
    to create a ~ normal distribution
    and allow for better fitting between different types of variables
    in a multivariable regression

    It also lags the data by a specified number of weeks (look_back)

    Takes:
    A start and end date (strings)
        startdate =
        enddate =
    A dataframe (pandas)
        dfin =
    The name of a single column of data to normalize (string)
        dfname =
    A specified number of look backs (integer)
        l_back = [1]

    Returns:
    The dataframe with a column of normalized, and lagged, data
    The scaler model that can be used to 'inverse' transform
        """

    # # subset
    dfin = dfin.loc[startdate:enddate]
    # # normalize
    scaler = MinMaxScaler(feature_range=(0, 1))
    # # add normalized to dataset
    dfin[dfname+'_norm'] = scaler.fit_transform(dfin[
                                            dfname].to_numpy().reshape(-1, 1))
    # # lag
    dfin[dfname+'_norm_tm'+str(l_back)] = dfin[dfname+'_norm'].shift(l_back)
    return dfin, scaler


def denorm_it(val, scaler):
    """De normalizes a single value

    Takes:
    A scaled value (a single number)
        val =
    A scaler from sklearn
        scaler =
    """
    # # inverse transform a single value
    newval = scaler.inverse_transform(val.reshape(1, -1))
    return newval
