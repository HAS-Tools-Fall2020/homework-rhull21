#QH 0917 Modified from:
# Starter code for Homework 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
#QH 0917 Data retrieved
filename = 'streamflow_week4.txt'
filepath = os.path.join('../data', filename)
print(os.getcwd())
print(filepath)

# %%
# # DON'T change this part -- this creates the lists you 
# # should use for the rest of the assignment
# # no need to worry about how this is being done now we will cover
# # this in later sections. 

# #Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# Make a numpy array of this data
flow_data = data[['year', 'month','day', 'flow']].to_numpy()

# Getting rid of the pandas dataframe since we wont be using it this week
# del(data) (whoops)

# %% 
# Homwork Questions

# 2. Describe the variable flow_data:
	# a) What is it?
		# * The variable flow_data is a numpy Array
print(type(flow_data))
# <class 'numpy.ndarray'>

	# b) What type of values is it composed of?
		# * The variable is composed of 64-bit floats
print(flow_data.dtype)
# dtype('float64')
			# * For me this was a bit difficult to visualize because the outputs are in scientific notation:
print(flow_data[0])
# [1.989e+03 1.000e+00 1.000e+00 2.070e+02]
			# * So I converted to ints (since it was easier to look at, and we're not concerned with losing some precision on the daily flows)
flow_data_int = flow_data.astype(np.int16)
print(flow_data_int[0])
# [1989    1    1  207]
	# c) What is are its dimensions, and total size?
		# * This is a two-dimensional array (rows and columns), with 11582 rows and 4 columns yielding 46328 total items
print(flow_data.ndim)
# 2
print(flow_data.shape)
# (11582, 4)
print(flow_data.size)
# 46328
	# d) How many times was the daily flow greater than your prediction in the month of September (express your answer in terms of the total number of times and as a percentage)?
		# * Qualitatively, my predictions for the September period have been between 40 and 60 cfs
			# * I'll answer this question for 40, 50, and 60 cfs, respectively
			# * I'll also answer this question excluding all values from september 2020 in the dataset
			# * I'll also report the number of times it didn't exceed this value, which may be more interesting				
for j in range(40,61,10):
	 flow_count = np.sum((flow_data_int[:,3] > j) & (flow_data_int[:,1]==9) & (flow_data_int[:,0] != 2020))
	 total_count = np.sum((flow_data_int[:,1]==9) & (flow_data_int[:,0] != 2020))
	 print("Flow exceeded", j, " cfs ", flow_count, " times in non-2020 Septembers")
	 print("Flow therefore exceeded", j, " cfs ", int(100*flow_count/total_count), " percent of the time in non-2020 Septembers")

# Flow exceeded 40  cfs  930  times in non-2020 Septembers
# Flow therefore exceeded 40  cfs  100  percent of the time in non-2020 Septembers
# Flow exceeded 50  cfs  925  times in non-2020 Septembers
# Flow therefore exceeded 50  cfs  99  percent of the time in non-2020 Septembers
# Flow exceeded 60  cfs  886  times in non-2020 Septembers
# Flow therefore exceeded 60  cfs  95  percent of the time in non-2020 Septembers

				
# 3. How would your answer to the previous question change if you considered only daily flows in or before 2000? Same question for the flows in or after the year 2010? (again report total number of times and percentage)
	# a) For only daily flows in and before 2000
for j in range(40,61,10):
	 flow_count = np.sum((flow_data_int[:,3] > j) & (flow_data_int[:,1]==9) & (flow_data_int[:,0] <= 2000))
	 total_count = np.sum((flow_data_int[:,1]==9) & (flow_data_int[:,0] <= 2000))
	 print("Flow exceeded", j, " cfs ", flow_count, " times in pre-2000 Septembers")
	 print("Flow therefore exceeded", j, " cfs ", int(100*flow_count/total_count), " percent of the time in pre-2000 Septembers")

# Flow exceeded 40  cfs  360  times in pre-2000 Septembers
# Flow therefore exceeded 40  cfs  100  percent of the time in pre-2000 Septembers
# Flow exceeded 50  cfs  360  times in pre-2000 Septembers
# Flow therefore exceeded 50  cfs  100  percent of the time in pre-2000 Septembers
# Flow exceeded 60  cfs  360  times in pre-2000 Septembers
# Flow therefore exceeded 60  cfs  100  percent of the time in pre-2000 Septembers
			
		
#	b) For only daily flows in and after 2010
for j in range(40,61,10):
	 flow_count = np.sum((flow_data_int[:,3] > j) & (flow_data_int[:,1]==9) & (flow_data_int[:,0] >= 2010))
	 total_count = np.sum((flow_data_int[:,1]==9) & (flow_data_int[:,0] >= 2010))
	 print("Flow exceeded", j, " cfs ", flow_count, " times in post-2000 Septembers")
	 print("Flow therefore exceeded", j, " cfs ", int(100*flow_count/total_count), " percent of the time in post-2000 Septembers")

# Flow exceeded 40  cfs  312  times in post-2010 Septembers
# Flow therefore exceeded 40  cfs  98  percent of the time in post-2010 Septembers
# Flow exceeded 50  cfs  306  times in post-2010 Septembers
# Flow therefore exceeded 50  cfs  96  percent of the time in post-2010 Septembers
# Flow exceeded 60  cfs  282  times in post-2010 Septembers
# Flow therefore exceeded 60  cfs  89  percent of the time in post-2010 Septembers
	
			 
# 4. How does the daily flow generally change from the first half of September to the second?
	# * I'll report this three ways: 
		# a) Mean:
flow_mean_beg = np.mean(flow_data_int[(flow_data[:,2]<=15) & (flow_data[:,1]==9) & (flow_data[:,0]!=2020) ,3])
print("The average flow for the first half of Septembers is ", int(flow_mean_beg))
# The average flow for the first half of Septembers is  182
flow_mean_end = np.mean(flow_data_int[(flow_data[:,2]>=16) & (flow_data[:,1]==9) & (flow_data[:,0]!=2020) ,3])
print("The average flow for the second half of Septembers is ", int(flow_mean_end), "cfs")
# The average flow for the second half of Septembers is  169 cfs
		# b) Quartiles (min, 25th percentile, median, 75th percentile)
flow_quants1 = np.quantile(flow_data_int[(flow_data[:,2]<=15) & (flow_data[:,1]==9) & (flow_data[:,0]!=2020),3], q=[0,0.1, 0.5, 0.9])
print("The minimum, 25th percentile, median, and 75th percentile for flow in the first half of Septembers is: ", flow_quants1)
# The minimum, 25th percentile, median, and 75th percentile for flow in the first half of Septembers is:  [ 48.   68.  137.  310.8]
flow_quants2 = np.quantile(flow_data_int[(flow_data[:,2]>=16) & (flow_data[:,1]==9) & (flow_data[:,0]!=2020),3], q=[0,0.1, 0.5, 0.9])
print("The minimum, 25th percentile, median, and 75th percentile for flow in the second half of Septembers is: ", flow_quants2)
# The minimum, 25th percentile, median, and 75th percentile for flow in the second half of Septembers is:  [ 51.  78. 111. 240.]
		# c) Visualization via histograms
			# # Histogram of all data in flow_data_int
# mybins = np.linspace(0, 1000, num=15) 
# plt.hist(flow_data_int[:,3], bins = mybins, density = True)
# plt.title('Streamflow for All Dates')
# plt.xlabel('Flow [cfs]')
# plt.ylabel('Probability Density')
# plt.ylim((0,0.005))

			# # shows plot Hull_Figure_1 (all data)
# plt.show()

			# # Histogram of all September data in flow_data_int
# mybins = np.linspace(0, 1000, num=15) 
# plt.hist(flow_data_int[(flow_data_int[:,1]==9),3], bins = mybins, density = True)
# plt.title('Streamflow for September')
# plt.xlabel('Flow [cfs]')
# plt.ylabel('Probability Density')
# plt.ylim((0,0.01))

			# # shows plot Hull_Figure_2 (September data)
# plt.show()

			# # Histogram of first half September data in flow_data_int
# mybins = np.linspace(0, 1000, num=15) 
# plt.hist(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,2]<=15) ,3], bins = mybins, density = True)
# plt.title('Streamflow for first half September')
# plt.xlabel('Flow [cfs]')
# plt.ylabel('Probability Density')
# plt.ylim((0,0.01))

			# # shows plot Hull_Figure_3 (early September data)
# plt.show()

			# # Histogram of first half September data in flow_data_int
# mybins = np.linspace(0, 1000, num=15) 
# plt.hist(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,2]>=16) ,3], bins = mybins, density = True)
# plt.title('Streamflow for second half September')
# plt.xlabel('Flow [cfs]')
# plt.ylabel('Probability Density')
# plt.ylim((0,0.01))

			# # shows plot Hull_Figure_4 (later September data)
# plt.show()

# 1. Include discussion of the quantitative analysis that lead to your prediction. This can include any analysis you complete but must include at least two histograms and some quantitative discussion of flow quantiles that helped you make your decision.

			# # Real data
# plt.plot(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2020),2],flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2020),3], 'g', label = 'September Stream Flow - 2020')
# plt.plot(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2019),2],flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2019),3], 'ro', label = 'September Stream Flow - 2019')
# plt.plot(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2015),2],flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2015),3], 'r*', label ='September Stream Flow - 2015')
# plt.plot(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2010),2],flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2010),3], 'r+', label = 'September Stream Flow - 2010')
			# # best fit data for sept 2020
# m, b = np.polyfit(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2020),2],flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2020),3],1)
# plt.plot(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2010),2], m*flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2010),2] + b, 'b', label = 'Best FitSeptember Stream Flow - 2020')


# plt.title('Streamflow for September')
# plt.xlabel('Day in September')
# plt.ylabel('Flow [cfs]')
# plt.xlim((0, 30))
# plt.ylim((0,200))
# plt.legend(loc="upper right")

			# # shows plot Hull_Figure_4 (2010, 2015, 2019, and 2020 data)
# plt.show()

			# # create a date field (so we can see the full date) 
flow_data_2 = data[['year', 'month','day', 'flow', 'datetime']].to_numpy()			

			# # replot the 2010 flow data with a proper date scale
# plt.plot(flow_data_2[(flow_data_2[:,1]>=9) & (flow_data_2[:,0] == 2010),4],flow_data_2[(flow_data_2[:,1]>=9) & (flow_data_2[:,0] == 2010),3], 'ro', label = 'Stream Flow - 2010')

# plt.title('Streamflow for 2010')
# plt.xlabel('Date')
# plt.ylabel('Flow [cfs]')
# plt.legend(loc="upper right")
			# # Hull figure 6
# plt.show()

			# Slice starting at 8/25/2010 (for week 1 of seasonal forecase)
result = np.where(flow_data_2[:,4] == '2010-08-25')
result_end = np.where(flow_data_2[:,4] == '2010-12-12')
print("starting index is ", result[0][0] ,  "and to check ", flow_data_2[result[0][0] ,4])
print("finishing index is ", result_end[0][0] ,  "and to check ", flow_data_2[result_end[0][0] ,4])

flow_dates = flow_data_2[(result[0][0]):(result_end[0][0]):7 ,4]
flow_flows = flow_data_2[(result[0][0]):(result_end[0][0]):7 ,3]
print(flow_dates)
print(flow_flows)
			# subtract ~ 20 cfs per flow, and thats the prediction
nflow_flows = np.subtract(flow_flows,20)
print(nflow_flows.astype(np.int32), sep=",")

