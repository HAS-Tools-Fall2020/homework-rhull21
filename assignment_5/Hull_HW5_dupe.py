# Example solution for HW 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week5.txt'
filepath = os.path.join('../data', filename)
print(os.getcwd())
print(filepath)

# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# %%

# Investigate the data
print(data.head(5))

## More investigation
        # print(data.shape)
        # print(data.info())
        # print(data.describe())


# create a date column using to_datetime
## eg
        # df = pd.DataFrame({'year': [2015, 2016],
        #                 'month': [2, 3],
        #                 'day': [4, 5]})
        # pd.to_datetime(df)
        # 0   2015-02-04
        # 1   2016-03-05
        # dtype: datetime64[ns]

## subset 'year', 'month', and 'day' columns into a new df (df_date)
df_date = data[['year', 'month', 'day']]
print(df_date)


## run pd.to_datetime of new df, df_date
df_date = pd.to_datetime(df_date)
print(df_date)

## set as index (?)
        ### an example of how to make a date an index using an auto-range
                # # data2 = data
                # # data2.index = pd.date_range('1900/1/30', periods=data2.shape[0])
                # # print(data2)
                # # remove old datetime column
data.index = df_date
print(data)

# remove agency_cd, site_no, datetime,code columns w/ .drop
## a_dataframe.drop(["A", "C"], axis=1, inplace=True)
data.drop(["agency_cd", "site_no", "datetime", "code"], axis=1, inplace=True)
print(data)


# %%
# Question 1
# Provide a summary of the data frames properties.
print(data.head(5))
print(data.shape)
print(data.info())
print(data.describe())

# What are the column names?
## Because I removed some, the column names are flow, year, month, and day. 
## date (formatted yyyy-mo-day) is the index

# What is its index?
## date (formatted as a date yyyy-mo-day) is the index (thought maybe it would be helpful later on)

# What data types do each of the columns have?
print(data.info())
## all of the data types now are numeric
        # #   Column  Non-Null Count  Dtype  
        # ---  ------  --------------  -----  
        # 0   flow    11589 non-null  float64
        # 1   year    11589 non-null  int32  
        # 2   month   11589 non-null  int32  
        # 3   day     11589 non-null  int32


# %%
# Question 2
# Provide a summary of the flow column including the min, mean, max, standard deviation and quartiles.
print(data['flow'].describe())

        # count    11589.000000
        # mean       345.704746
        # std       1411.008023
        # min         19.000000
        # 25%         93.800000
        # 50%        158.000000
        # 75%        216.000000
        # max      63400.000000
        # Name: flow, dtype: float64

# %%
# Question 3
# Provide the same information but on a monthly basis. (Note: you should be able to do this with one or two lines of code)
## group by!
print(data.groupby('month')['flow'].describe())

# Question 3...
        # count        mean          std    min      25%     50%      75%  
        # month                                                                    
        # 1      992.0  706.320565  2749.153983  158.0  202.000  219.50   292.00   
        # 2      904.0  925.252212  3348.821197  136.0  201.000  244.00   631.00   
        # 3      992.0  941.731855  1645.803872   97.0  179.000  387.50  1060.00   
        # 4      960.0  301.240000   548.140912   64.9  112.000  142.00   214.50   
        # 5      992.0  105.442339    50.774743   46.0   77.975   92.95   118.00   
        # 6      960.0   65.998958    28.966451   22.1   49.225   60.50    77.00   
        # 7      992.0   95.571472    83.512343   19.0   53.000   70.90   110.00   
        # 8      992.0  164.354133   274.464099   29.6   76.075  114.00   170.25   
        # 9      953.0  173.047744   287.156384   36.6   88.500  120.00   172.00   
        # 10     961.0  146.168991   111.779072   69.9  107.000  125.00   153.00   
        # 11     930.0  205.105376   235.673534  117.0  156.000  175.00   199.00   
        # 12     961.0  337.097815  1097.280926  155.0  191.000  204.00   228.00   

        #         max  
        # month           
        # 1      63400.0  
        # 2      61000.0  
        # 3      30500.0  
        # 4       4690.0  
        # 5        546.0  
        # 6        481.0  
        # 7       1040.0  
        # 8       5360.0  
        # 9       5590.0  
        # 10      1910.0  
        # 11      4600.0  
        # 12     28700.0 



# %%
# Question 4
# Provide a table with the 5 highest and 5 lowest flow values for the period of record. Include the date, month and flow values in your summary.

## two ways
### df.nlargest(n,columns), df.nsmallest(n,columns)
print('highest')
print(data.nlargest(5,'flow'))
print('\n','lowest')
print(data.nsmallest(5,'flow'))

### using df.sort_values(columns, ascending=True OR False).head(n)
n = 5
print('\n','highest')
print(data.sort_values('flow', ascending=False).head(n))
print('\n','lowest')
print(data.sort_values('flow', ascending=True).head(n))

# %%
# Question 5
# Find the highest and lowest flow values for every month of the year (i.e. you will find 12 maxes and 12 mins) and report back what year these occurred in.
## Aggregate! 
print('highest')
print(data.groupby('month')['flow'].nlargest(5))
        # 1      1993-01-08    63400.0
        # 1993-01-17    27900.0
        # 2005-01-12    26000.0
        # 1993-01-09    18800.0
        # 1993-01-18    17400.0
        # 2      1993-02-20    61000.0
        # 1995-02-15    45500.0
        # 2005-02-12    35600.0
        # 2005-02-13    23200.0
        # 2019-02-15    22200.0
        # 3      1995-03-06    30500.0
        # 2015-03-03    14600.0
        # 2020-03-14    13100.0
        # 1995-03-07     9900.0
        # 1991-03-02     9010.0
        # 4      1991-04-02     4690.0
        # 1998-04-13     4670.0
        # 1991-04-03     4410.0
        # 1998-04-12     4410.0
        # 1991-04-04     4210.0
        # 5      1992-05-31      546.0
        # 1994-05-01      545.0
        # 1998-05-01      480.0
        # 1998-05-02      431.0
        # 1994-05-02      426.0
        # 6      1992-06-01      481.0
        # 1992-06-02      343.0
        # 1992-06-03      269.0
        # 1992-06-04      199.0
        # 2000-06-29      179.0
        # 7      2006-07-31     1040.0
        # 1999-07-28      791.0
        # 1999-07-16      715.0
        # 1990-07-16      705.0
        # 2007-07-31      581.0
        # 8      1992-08-23     5360.0
        # 1992-08-24     4120.0
        # 2010-08-02     3490.0
        # 1992-08-25     1760.0
        # 2012-08-24     1340.0
        # 9      2004-09-21     5590.0
        # 1999-09-24     5260.0
        # 1999-09-25     1540.0
        # 2002-09-11     1280.0
        # 1994-09-03     1220.0
        # 10     2010-10-07     1910.0
        # 2004-10-30     1230.0
        # 2004-10-31     1180.0
        # 2018-10-04     1160.0
        # 2000-10-28     1070.0
        # 11     2004-11-23     4600.0
        # 2004-11-22     3300.0
        # 2004-11-24     2840.0
        # 2004-11-09     2300.0
        # 2004-11-25     1890.0
        # 12     2004-12-30    28700.0
        # 2004-12-29     7430.0
        # 2007-12-08     7210.0
        # 2004-12-31     6900.0
        # 1992-12-30     6600.0
        # Name: flow, dtype: float64
print('\n','lowest')
print(data.groupby('month')['flow'].nsmallest(5))

# %%
# Question 6
# Provide a list of historical dates with flows that are within 10% of your week 1 forecast value. If there are none than increase the %10 window until you have at least one other value and report the date and the new window you used
# week 1 forecast for last week was '44'

## dim fcast
fcast = 44
## calculate interval around +- fcast
fcast_rng = [fcast-fcast*0.1, fcast+fcast*0.1]


## use upper and lower sides of interval to filter out flow data within the desired range
###one way
####data[(data['flow'] > fcast_rng[0]) & (data['flow'] < fcast_rng[1])]

### another way
####data[(data.flow > fcast_rng[0]) & (data.flow < fcast_rng[1])]

### a final way to get just the dates
dates = data[(data.flow > fcast_rng[0]) & (data.flow < fcast_rng[1])].index.tolist()
print(*dates, sep="\n")
        # 1989-07-04 00:00:00
        # 1989-07-05 00:00:00
        # 1989-07-06 00:00:00
        # 1989-07-07 00:00:00
        # 1989-07-08 00:00:00
        # 1990-06-24 00:00:00
        # 1990-06-28 00:00:00
        # 1990-06-29 00:00:00
        # 1990-06-30 00:00:00
        # 1991-07-04 00:00:00
        # 1996-06-29 00:00:00
        # 1997-06-27 00:00:00
        # 1997-07-02 00:00:00
        # 1997-07-04 00:00:00
        # 1997-07-05 00:00:00
        # 1997-07-08 00:00:00
        # 1997-07-09 00:00:00
        # 1997-07-11 00:00:00
        # 1997-07-12 00:00:00
        # 1997-07-13 00:00:00
        # 1997-07-14 00:00:00
        # 1997-07-16 00:00:00
        # 1997-07-20 00:00:00
        # 1997-07-22 00:00:00
        # 1997-08-01 00:00:00
        # 1998-07-01 00:00:00
        # 1998-07-02 00:00:00
        # 1998-07-04 00:00:00
        # 1999-07-01 00:00:00
        # 1999-07-02 00:00:00
        # 1999-07-03 00:00:00
        # 1999-07-04 00:00:00
        # 1999-07-06 00:00:00
        # 2000-06-02 00:00:00
        # 2000-06-04 00:00:00
        # 2000-06-11 00:00:00
        # 2000-06-15 00:00:00
        # 2000-06-18 00:00:00
        # 2000-07-19 00:00:00
        # 2000-07-20 00:00:00
        # 2000-07-21 00:00:00
        # 2000-07-30 00:00:00
        # 2000-07-31 00:00:00
        # 2000-08-01 00:00:00
        # 2001-06-13 00:00:00
        # 2001-06-16 00:00:00
        # 2001-06-17 00:00:00
        # 2001-06-19 00:00:00
        # 2001-06-20 00:00:00
        # 2002-07-07 00:00:00
        # 2002-07-08 00:00:00
        # 2003-06-28 00:00:00
        # 2003-07-01 00:00:00
        # 2003-07-02 00:00:00
        # 2003-07-08 00:00:00
        # 2003-07-09 00:00:00
        # 2003-07-10 00:00:00
        # 2003-07-11 00:00:00
        # 2003-07-12 00:00:00
        # 2003-07-13 00:00:00
        # 2004-05-22 00:00:00
        # 2004-06-01 00:00:00
        # 2004-06-04 00:00:00
        # 2004-06-05 00:00:00
        # 2004-06-06 00:00:00
        # 2004-06-07 00:00:00
        # 2004-06-13 00:00:00
        # 2004-06-14 00:00:00
        # 2004-06-15 00:00:00
        # 2004-06-20 00:00:00
        # 2004-08-04 00:00:00
        # 2004-08-05 00:00:00
        # 2004-08-06 00:00:00
        # 2005-07-15 00:00:00
        # 2006-06-07 00:00:00
        # 2006-06-08 00:00:00
        # 2006-06-13 00:00:00
        # 2006-06-15 00:00:00
        # 2006-06-18 00:00:00
        # 2006-06-19 00:00:00
        # 2006-06-20 00:00:00
        # 2006-06-21 00:00:00
        # 2006-06-22 00:00:00
        # 2006-06-24 00:00:00
        # 2006-06-25 00:00:00
        # 2006-06-26 00:00:00
        # 2006-06-27 00:00:00
        # 2006-06-28 00:00:00
        # 2007-06-20 00:00:00
        # 2007-06-21 00:00:00
        # 2007-06-22 00:00:00
        # 2007-06-23 00:00:00
        # 2007-07-09 00:00:00
        # 2007-07-13 00:00:00
        # 2007-07-16 00:00:00
        # 2007-07-17 00:00:00
        # 2008-06-25 00:00:00
        # 2008-06-26 00:00:00
        # 2008-06-27 00:00:00
        # 2008-06-28 00:00:00
        # 2008-07-01 00:00:00
        # 2008-07-04 00:00:00
        # 2008-08-03 00:00:00
        # 2009-07-01 00:00:00
        # 2009-07-02 00:00:00
        # 2009-07-16 00:00:00
        # 2009-07-17 00:00:00
        # 2009-07-19 00:00:00
        # 2009-07-20 00:00:00
        # 2009-08-03 00:00:00
        # 2009-08-04 00:00:00
        # 2009-08-05 00:00:00
        # 2009-08-13 00:00:00
        # 2009-08-20 00:00:00
        # 2009-08-21 00:00:00
        # 2009-08-22 00:00:00
        # 2009-08-23 00:00:00
        # 2012-06-06 00:00:00
        # 2012-06-07 00:00:00
        # 2012-06-08 00:00:00
        # 2012-06-09 00:00:00
        # 2012-06-10 00:00:00
        # 2012-06-18 00:00:00
        # 2013-06-09 00:00:00
        # 2013-06-10 00:00:00
        # 2013-07-10 00:00:00
        # 2013-07-11 00:00:00
        # 2013-08-15 00:00:00
        # 2013-08-16 00:00:00
        # 2013-08-18 00:00:00
        # 2014-06-05 00:00:00
        # 2014-06-06 00:00:00
        # 2014-06-07 00:00:00
        # 2014-06-08 00:00:00
        # 2014-06-09 00:00:00
        # 2014-06-11 00:00:00
        # 2014-06-15 00:00:00
        # 2014-06-16 00:00:00
        # 2014-06-17 00:00:00
        # 2014-06-24 00:00:00
        # 2014-06-25 00:00:00
        # 2014-07-06 00:00:00
        # 2015-06-26 00:00:00
        # 2015-06-27 00:00:00
        # 2015-06-28 00:00:00
        # 2015-06-29 00:00:00
        # 2015-06-30 00:00:00
        # 2016-06-04 00:00:00
        # 2016-06-05 00:00:00
        # 2016-06-06 00:00:00
        # 2016-06-07 00:00:00
        # 2016-06-08 00:00:00
        # 2016-06-10 00:00:00
        # 2016-06-11 00:00:00
        # 2016-06-18 00:00:00
        # 2016-06-19 00:00:00
        # 2016-06-20 00:00:00
        # 2016-06-21 00:00:00
        # 2016-06-24 00:00:00
        # 2016-06-27 00:00:00
        # 2016-06-29 00:00:00
        # 2016-07-11 00:00:00
        # 2016-07-12 00:00:00
        # 2016-07-13 00:00:00
        # 2016-07-20 00:00:00
        # 2017-06-10 00:00:00
        # 2017-06-16 00:00:00
        # 2017-06-22 00:00:00
        # 2017-06-23 00:00:00
        # 2017-06-24 00:00:00
        # 2017-06-25 00:00:00
        # 2017-06-26 00:00:00
        # 2017-06-27 00:00:00
        # 2017-06-29 00:00:00
        # 2017-06-30 00:00:00
        # 2017-07-01 00:00:00
        # 2017-07-02 00:00:00
        # 2017-07-03 00:00:00
        # 2017-07-04 00:00:00
        # 2017-07-05 00:00:00
        # 2017-07-06 00:00:00
        # 2017-07-07 00:00:00
        # 2017-07-08 00:00:00
        # 2017-07-09 00:00:00
        # 2018-06-02 00:00:00
        # 2018-06-04 00:00:00
        # 2018-06-05 00:00:00
        # 2018-06-06 00:00:00
        # 2018-06-07 00:00:00
        # 2018-06-08 00:00:00
        # 2018-06-09 00:00:00
        # 2018-06-10 00:00:00
        # 2018-06-11 00:00:00
        # 2018-06-12 00:00:00
        # 2018-06-14 00:00:00
        # 2018-06-15 00:00:00
        # 2018-06-23 00:00:00
        # 2018-06-24 00:00:00
        # 2018-06-25 00:00:00
        # 2018-06-27 00:00:00
        # 2018-06-28 00:00:00
        # 2018-07-10 00:00:00
        # 2019-06-28 00:00:00
        # 2019-06-29 00:00:00
        # 2019-06-30 00:00:00
        # 2019-07-01 00:00:00
        # 2019-07-02 00:00:00
        # 2019-07-03 00:00:00
        # 2019-07-04 00:00:00
        # 2019-07-05 00:00:00
        # 2019-07-06 00:00:00
        # 2019-07-07 00:00:00
        # 2019-07-08 00:00:00
        # 2019-07-09 00:00:00
        # 2019-07-10 00:00:00
        # 2019-07-11 00:00:00
        # 2019-07-12 00:00:00
        # 2019-07-13 00:00:00
        # 2019-07-14 00:00:00
        # 2019-07-15 00:00:00
        # 2019-07-16 00:00:00
        # 2019-07-17 00:00:00
        # 2019-07-18 00:00:00
        # 2019-07-19 00:00:00
        # 2019-07-20 00:00:00
        # 2019-07-21 00:00:00
        # 2019-07-23 00:00:00
        # 2019-07-24 00:00:00
        # 2019-07-25 00:00:00
        # 2019-07-26 00:00:00
        # 2019-07-27 00:00:00
        # 2019-07-28 00:00:00
        # 2019-07-29 00:00:00
        # 2019-07-30 00:00:00
        # 2019-07-31 00:00:00
        # 2019-08-16 00:00:00
        # 2019-08-19 00:00:00
        # 2019-08-29 00:00:00
        # 2019-08-31 00:00:00
        # 2020-05-30 00:00:00
        # 2020-05-31 00:00:00
        # 2020-06-12 00:00:00
        # 2020-06-13 00:00:00
        # 2020-06-14 00:00:00
        # 2020-06-15 00:00:00
        # 2020-06-19 00:00:00
        # 2020-06-20 00:00:00
        # 2020-06-21 00:00:00
        # 2020-06-22 00:00:00
        # 2020-06-23 00:00:00
        # 2020-06-25 00:00:00
        # 2020-07-02 00:00:00
        # 2020-07-03 00:00:00
        # 2020-07-06 00:00:00
        # 2020-07-07 00:00:00
        # 2020-07-08 00:00:00
        # 2020-07-17 00:00:00
        # 2020-07-18 00:00:00
        # 2020-07-19 00:00:00
        # 2020-07-20 00:00:00
        # 2020-07-22 00:00:00
        # 2020-08-04 00:00:00
        # 2020-08-05 00:00:00
        # 2020-08-06 00:00:00
        # 2020-08-07 00:00:00
        # 2020-08-21 00:00:00
        # 2020-08-22 00:00:00
        # 2020-08-28 00:00:00
        # 2020-08-29 00:00:00
        # 2020-09-05 00:00:00
        # 2020-09-06 00:00:00
        # 2020-09-07 00:00:00
        # 2020-09-11 00:00:00

# %%
## Make a simple linear function
def line(x,m,b):
# give y, in y = mx + b
  return m*x + b


# %%
# Forecast
# Similar approach as last time

## Generate best fit lines for both 2019 and 2020 (similar dry years)

### first generate for only 09/01 - present for 2019, 2020
m20, b20 = np.polyfit(data[(data.month == 9) & (data.year == 2020)].day, data[(data.month == 9) & (data.year == 2020)].flow,1)
m19, b19 = np.polyfit(data[(data.month == 9) & (data.year == 2019)].day, data[(data.month == 9) & (data.year == 2019)].flow,1)

print("September 2020: y= ", round(m20,3), "*x + ", round(b20,3))
print("September 2019: y= ", round(m19,3), "*x + ", round(b19,3))

### Extrapolate from best fit line results for next two weeks (2020 only) 
#### 09-27 to 10/03
##### using 'line' function "y = mx + b", where x = 30 (roughly the mid-point)
w1p = round(line(30,m20,b20),1)

#### 10/03 to 10/10
##### using 'line' function "y = mx + b", where x = 37 (roughly the mid-point)
w2p = round(line(37,m20,b20),1)

print(w1p, w2p, sep=", ")
        #57.9, 60.0

### Extrapolate difference between best fit lines for 2019 and 2020
#### Calculate the 'correction factor' of average distance between the best fit lines in September
##### difference of 'flow' at midpoint (x = 12)
corrf = round(line(12,m19,b19),1) - round(line(12,m20,b20),1)
        # 16.1

# %%
### use this 'difference' to calculate mean values by subtracting from 2019 linear regression for all of 2019
#### In the 2019 series, select by date
sdate = pd.to_datetime('2019-08-25', infer_datetime_format=True)
edate = pd.to_datetime('2019-12-12', infer_datetime_format=True)
datepd = data.loc[sdate:edate:7].index.to_frame()

#### extract the number of days from 09/02/2019 
# from https://stackoverflow.com/questions/37840812/pandas-subtracting-two-date-columns-and-the-result-being-an-integer
datepd = datepd[0].sub(pd.to_datetime('2019-09-01', infer_datetime_format=True), axis=0) / np.timedelta64(1, 'D')
datepd = datepd.to_frame()

#### Calculate a new regression for all 2019 data
##### add a new column to data called 'days_s', which is days since 09-01-2019
idate = pd.to_datetime('2019-09-01', infer_datetime_format=True)
data.insert(0,"days_s",data.index.to_frame().sub(idate,axis= 0) / np.timedelta64(1, 'D'))

##### best fit
# %%
m19b, b19b = np.polyfit(data[(data.month >= 9) & (data.year == 2019)].days_s, data[(data.month >= 9) & (data.year == 2019)].flow,1)

#### Use number of days in regression line (m19b, b19b), subtracting corrf for good measure
datepd.insert(0,"flow", line(datepd[0],m19b,b19b)-corrf)

# This yields really weird results early (negative flow) but I'm tired
#### -211,-157,-103,-49,4,58,111,165,219,273,327,381,435,488,542,596