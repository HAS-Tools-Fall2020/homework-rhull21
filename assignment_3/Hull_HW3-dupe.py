# Modified from 'week3_lists_start.py (Start code for assignment 3)
# Similar to week3_lists_start_qh.py in homework working directory

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFIED FROM SOURCE CODE TO ADJUST PATH ** 
# Set the file name and path to where you have stored the data
filename = 'streamflow_week3.txt'
filepath = os.path.join('..\..\homework-rhull21\data', filename)
print(os.getcwd())
print(filepath)

# %%
# DON'T change this part -- this creates the lists you 
# should use for the rest of the assignment
# no need to worry about how this is being done now we will cover
# this in later sections. 

#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

#make lists of the data
flow = data.flow.values.tolist()
date = data.datetime.values.tolist()
year = data.year.values.tolist()
month = data.month.values.tolist()
day = data.day.values.tolist()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%

# ATIQUATED: Originally Modified because wrong dataset was used 

#Read the data into a pandas dataframe
# ** MODIFIED TO DELETE FIRST 33 ROWS - qh
# ** MODIFIED TO INCLUDE TZ_CD IN COLUMN HEADERS
# data=pd.read_table(filepath, sep = '\t', skiprows=33,
#         names=['agency_cd', 'site_no', 'datetime', 'tz', 'flow', 'code']
#         )

# ** MODIFIED TO ACCOMODATE DELETE TIME
# Expand the dates to year month day\

# data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
# data['year'] = data['year'].astype(int)
# data['month'] = data['month'].astype(int)
# data['day'] = data['day'].str[:-6]
# data['day'] = data['day'].astype(int)

# # # #make lists of the data
# flow = data.flow.values.tolist()
# date = data.datetime.values.tolist()
# year = data.year.values.tolist()
# month = data.month.values.tolist()
# day = data.day.values.tolist()

# # # # Getting rid of the pandas dataframe since we wont be using it this week
# del(data)

# %% 
# Answering Question 1

# (1a) what type of objects are they?
print(type(day))
# <class 'list'>

# (1b) what type of objects are they composed of?
type(date[1]) # str
type(flow[1]) # float
type(day[1]) # int
type(month[1]) # int
type(year[1]) # int

# (1c) how long are they?
len(date) # 11575


# %% 
# Answerin Question 2, 3
# (2) How many times was daily flow greater than your prediction in September

# # for 2020
# list_092020 = []
# list_092020_all = []
# for i in range(len(flow)):
#         # 2020 only, prediction = 60 cfs
#         if month[i] == 9 and year[i] == 2020:
#             list_092020_all.append(flow[i])
#             if flow [i] > 60:
#                 list_092020.append(flow[i])


# # for all Septembers back to 1989 
# list_092020 = []
# list_092020_all = []
# for i in range(len(flow)):
#         #prediction = 60 cfs
#         if month[i] == 9:
#             list_092020_all.append(flow[i])
#             if flow [i] > 60:
#                 list_092020.append(flow[i])


# for all Septembers 1989 - 2000
# list_092020 = []
# list_092020_all = []
# for i in range(len(flow)):
#         # prediction = 60 cfs
#         if month[i] == 9 and year[i] <= 2000:
#             list_092020_all.append(flow[i])
#             if flow [i] > 60:
#                 list_092020.append(flow[i])


# for all Septembers 2010 - present
# list_092020 = []
# list_092020_all = []
# for i in range(len(flow)):
#         # prediction = 60 cfs
#         if month[i] == 9 and year[i] >= 2010:
#             list_092020_all.append(flow[i])
#             if flow [i] > 60:
#                 list_092020.append(flow[i])

num_exceed = len(list_092020)
num_total = len(list_092020_all)

print("Flow exceeded expections ", num_exceed, "times in September, or", 100*num_exceed/num_total, "percent of times")

# %% 
# Answer Question 4 

# Create list of beginning and end of September flows
list_09_begin = []
list_09_end = []
for i in range(len(flow)):
        # prediction = 60 cfs
        if month[i] == 9:
            if day[i] <= 15:
                list_09_begin.append(flow[i])
            else:
                list_09_end.append(flow[i])

# Create statistics for each list
stats_begin = [min(list_09_begin), max(list_09_begin), np.mean(list_09_begin), np.std(list_09_begin)]
stats_end = [min(list_09_end), max(list_09_end), np.mean(list_09_end), np.std(list_09_end)]

# # Show results
print("For the first half of Septembers, Min = ", stats_begin[0], " Max = ",  stats_begin[1], " Mean = ",  stats_begin[2], " Std = ",  stats_begin[3])
print("For the second half of Septembers, Min = ", stats_end[0], " Max = ",  stats_end[1], " Mean = ",  stats_end[2], " Std = ",  stats_end[3])

# %% 
# Forecast

# Take average for every week-long subset
    # from week 1 to week 16
# an output list anticipating 12 entries
list_flows = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]

for i in range(len(flow)): 
    # optional year toggle
    if year[i] >= 2010:   
        if month[i] == 8:
            # week 1
            if day[i] >= 22 and day[i] <= 29:
                list_flows[0].append(flow[i])
            # week 2
            elif day[i] >= 30:
                list_flows[1].append(flow[i])
        elif month[i] == 9:
            # week 2
            if day[i] <= 5:
                list_flows[1].append(flow[i])
            # week 3
            elif day[i] >= 6 and day[i] <= 12:
                list_flows[2].append(flow[i])
            # week 4
            elif day[i] >= 13 and day[i] <= 20:
                list_flows[3].append(flow[i])
            # week 5
            elif day[i] >= 20 and day[i] <= 26:
                list_flows[4].append(flow[i])
            # week 6
            elif day[i] >= 27:
                list_flows[5].append(flow[i])
        elif month[i] == 10:
            # week 6
            if day[i] <= 3:
                list_flows[5].append(flow[i])
            # week 7
            elif day[i] >= 4 and day[i] <= 10:
                list_flows[6].append(flow[i])
            # week 8
            elif day[i] >= 11 and day[i] <= 17:
                list_flows[7].append(flow[i])
            # week 9
            elif day[i] >= 18 and day[i] <= 24:
                list_flows[8].append(flow[i])
            # week 10
            elif day[i] >= 25 and day[i] <= 31:
                list_flows[9].append(flow[i])
        elif month[i] == 11:
            # week 11
            if day[i] >= 1 and day[i] <= 7:
                list_flows[10].append(flow[i])
            # week 12
            elif day[i] >= 8 and day[i] <= 14:
                list_flows[11].append(flow[i])
            # week 13
            elif day[i] >= 15 and day[i] <= 21:
                list_flows[12].append(flow[i])
            # week 14
            elif day[i] >= 22 and day[i] <= 28:
                list_flows[13].append(flow[i])
            # week 15
            elif day[i] >= 29:
                list_flows[14].append(flow[i])
        elif month[i] == 12:
            if day[i] <= 5:
                list_flows[14].append(flow[i])
            # week 16
            elif day[i] >= 6 and day[i] <= 12:
                list_flows[15].append(flow[i])

# return results
list_flows_avg = []                
for j in range(0,16):
    list_flows_avg.append(int(np.mean(list_flows[j])))

print(list_flows_avg, sep=',')




# %%
