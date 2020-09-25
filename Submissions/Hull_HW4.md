## Assignment 4
Robert Hull
09172020

---------
### Grade
3/3 - great job.  Next time don't include the actual code snippets here though you can just include a text summary with your graphs :) 
___

### Assignment Questions

1. Include discussion of the quantitative analysis that lead to your prediction. This can include any analysis you complete but must include at least two histograms and some quantitative discussion of flow quantiles that helped you make your decision.
	* Look at the recent (september) data in x, y space adn compare it to past 'drought years'
	* See: https://www.drought.gov/drought/states/arizona#:~:text=Drought%20in%20Arizona&text=The%20U.S.%20Drought%20Monitor%20started,affected%2036.15%25%20of%20Arizona%20land.

			`# Real data
			plt.plot(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2020),2],flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2020),3], 'g', label = 'September Stream Flow - 2020')
			plt.plot(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2019),2],flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2019),3], 'ro', label = 'September Stream Flow - 2019')
			plt.plot(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2015),2],flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2015),3], 'r*', label ='September Stream Flow - 2015')
			plt.plot(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2010),2],flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2010),3], 'r+', label = 'September Stream Flow - 2010')
			# best fit data for sept 2020
			m, b = np.polyfit(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2020),2],flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2020),3],1)
			plt.plot(flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2010),2], m*flow_data_int[(flow_data_int[:,1]==9) & (flow_data_int[:,0] == 2010),2] + b, 'b', label = 'Best FitSeptember Stream Flow - 2020')
			# make plot
			plt.title('Streamflow for September')
			plt.xlabel('Day in September')
			plt.ylabel('Flow [cfs]')
			plt.xlim((0, 30))
			plt.ylim((0,200))
			plt.legend(loc="upper right")
			# shows plot Hull_Figure_4 (2010, 2015, 2019, and 2020 data)
			plt.show()`

	* This generated two observations:

		1) I decided (kind of randomly) that 2010 looked most similar to 2020, and decided to base my seasonal predictions

			a) I sliced the data from 8/25/2020 to 12/12/2020 on 7 day (weekly) intervals and arbitrarily took whatever value there was for that day

			b) After assembling all that in brand new array, I then subtracted 20 cfs from each value (which seems about the difference between the 2010 data and this years data so far)

			c) And those are my results for the seasonal forecast!

		2) I used a best-fit line to 'guess' at the trajectory of flow for
		the next two weeks:

			a) Flow decreasing by about 0.28 cfs / day from a y-int of 52 cfs on Sept 1st

			b) Just semi-quantitatively, that's y = -0.28*x + 52, where x(0) = Sept 1st

			c) So for 09/27 (week 1 forecast), thats x = 27, y = 44 cfs

			d) for 10/03 (week 2 forecast), thats x = 34, y = 42 cfs

2. Describe the variable flow_data:

	a) What is it?
		* The variable `flow_data` is a numpy Array
				`type(flow_data)`
				`# <class 'numpy.ndarray'>`

	b) What type of values is it composed of?
		* The variable is composed of 64-bit floats
			`flow_data.dtype`
			`# dtype('float64')`
		* For me this was a bit difficult to visualize because the outputs are in scientific notation:
			`print(flow_data[0])`
			`# [1.989e+03 1.000e+00 1.000e+00 2.070e+02]`
		* So I converted to ints (since it was easier to look at, and we're not concerned with losing some precision on the daily flows)
			`flow_data_int = flow_data.astype(np.int16)`
			`print(flow_data_int[0])`
			`# [1989    1    1  207]`
	c) What is are its dimensions, and total size?
		* This is a two-dimensional array (rows and columns), with 11582 rows and 4 columns yielding 46328 total items
			`print(flow_data.ndim)
			# 2
			print(flow_data.shape)
			# (11582, 4)
			print(flow_data.size)
			# 46328`
	d) How many times was the daily flow greater than your prediction in the month of September (express your answer in terms of the total number of times and as a percentage)?
		* Qualitatively, my predictions for the September period have been between 40 and 60 cfs
			* I'll answer this question for 40, 50, and 60 cfs, respectively
			* I'll also answer this question excluding all values from september 2020 in the dataset
			* I'll also report the number of times it didn't exceed this value, which may be more interesting				
			`for j in range(40,61,10):
				 flow_count = np.sum((flow_data_int[:,3] > j) & (flow_data_int[:,1]==9) & (flow_data_int[:,0] != 2020))
				 total_count = np.sum((flow_data_int[:,1]==9) & (flow_data_int[:,0] != 2020))
				 print("Flow exceeded", j, " cfs ", flow_count, " times in non-2020 Septembers")
				 print("Flow therefore exceeded", j, " cfs ", int(100*flow_count/total_count), " percent of the time in non-2020 Septembers")

			# Flow exceeded 40  cfs  930  times in non-2020 Septembers
			# Flow therefore exceeded 40  cfs  100  percent of the time in non-2020 Septembers
			# Flow exceeded 50  cfs  925  times in non-2020 Septembers
			# Flow therefore exceeded 50  cfs  99  percent of the time in non-2020 Septembers
			# Flow exceeded 60  cfs  886  times in non-2020 Septembers
			# Flow therefore exceeded 60  cfs  95  percent of the time in non-2020 Septembers`


3. How would your answer to the previous question change if you considered only daily flows in or before 2000? Same question for the flows in or after the year 2010? (again report total number of times and percentage):

	a and b) For only daily flows in and before 2000, and in and after 2010

		`for j in range(40,61,10):
			 flow_count = np.sum((flow_data_int[:,3] > j) & (flow_data_int[:,1]==9) & (flow_data_int[:,0] <= 2000))
			 total_count = np.sum((flow_data_int[:,1]==9) & (flow_data_int[:,0] <= 2000))
			 print("Flow exceeded", j, " cfs ", flow_count, " times in pre-2000 Septembers")
			 print("Flow therefore exceeded", j, " cfs ", int(100*flow_count/total_count), " percent of the time in pre-2000 Septembers")
			# Flow exceeded 40  cfs  360  times in pre-2000 Septembers
			# Flow therefore exceeded 40  cfs  100  percent of the time in pre-2000 Septembers
			# Flow exceeded 50  cfs  360  times in pre-2000 Septembers
			# Flow therefore exceeded 50  cfs  100  percent of the time in pre-2000 Septembers
			# Flow exceeded 60  cfs  360  times in pre-2000 Septembers
			# Flow therefore exceeded 60  cfs  100  percent of the time in pre-2000 Septembers`

		`for j in range(40,61,10):
			 flow_count = np.sum((flow_data_int[:,3] > j) & (flow_data_int[:,1]==9) & (flow_data_int[:,0] >= 2010))
			 total_count = np.sum((flow_data_int[:,1]==9) & (flow_data_int[:,0] >= 2010))
			 print("Flow exceeded", j, " cfs ", flow_count, " times in post-2000 Septembers")
			 print("Flow therefore exceeded", j, " cfs ", int(100*flow_count/total_count), " percent of the time in post-2000 Septembers")
			# Flow exceeded 40  cfs  312  times in post-2010 Septembers
			# Flow therefore exceeded 40  cfs  98  percent of the time in post-2010 Septembers
			# Flow exceeded 50  cfs  306  times in post-2010 Septembers
			# Flow therefore exceeded 50  cfs  96  percent of the time in post-2010 Septembers
			# Flow exceeded 60  cfs  282  times in post-2010 Septembers
			# Flow therefore exceeded 60  cfs  89  percent of the time in post-2010 Septembers`

4. How does the daily flow generally change from the first half of September to the second?
	* I'll report this three ways:
		a) Mean:
			`flow_mean_beg = np.mean(flow_data_int[(flow_data[:,2]<=15) & (flow_data[:,1]==9) & (flow_data[:,0]!=2020) ,3])
			print("The average flow for the first half of Septembers is ", int(flow_mean_beg))
			# The average flow for the first half of Septembers is  182
			flow_mean_end = np.mean(flow_data_int[(flow_data[:,2]>=16) & (flow_data[:,1]==9) & (flow_data[:,0]!=2020) ,3])
			print("The average flow for the second half of Septembers is ", int(flow_mean_end), "cfs")
			# The average flow for the second half of Septembers is  169 cfs`
		b) Quartiles (min, 25th percentile, median, 75th percentile)
			`flow_quants1 = np.quantile(flow_data_int[(flow_data[:,2]<=15) & (flow_data[:,1]==9) & (flow_data[:,0]!=2020),3], q=[0,0.1, 0.5, 0.9])
			print("The minimum, 25th percentile, median, and 75th percentile for flow in the first half of Septembers is: ", flow_quants1)
			# The minimum, 25th percentile, median, and 75th percentile for flow in the first half of Septembers is:  [ 48.   68.  137.  310.8]
			flow_quants2 = np.quantile(flow_data_int[(flow_data[:,2]>=16) & (flow_data[:,1]==9) & (flow_data[:,0]!=2020),3], q=[0,0.1, 0.5, 0.9])
			print("The minimum, 25th percentile, median, and 75th percentile for flow in the second half of Septembers is: ", flow_quants2)
			# The minimum, 25th percentile, median, and 75th percentile for flow in the second half of Septembers is:  [ 51.  78. 111. 240.]`
		c) Visualization via histograms:
			* Two figures in the assignment_4 directory show histograms for the first half and second half of September
			` # Histogram of first half September data in flow_data_int
				mybins = np.linspace(0, 1000, num=15)
				plt.hist(flow_data[(flow_data_int[:,1]==9) & (flow_data[:,2]<=15) ,3], bins = mybins, density = True)
				plt.title('Streamflow for first half September')
				plt.xlabel('Flow [cfs]')
				plt.ylabel('Probability Density')
				plt.ylim((0,0.01))

			# shows plot Hull_Figure_3 (early September data)
				plt.show()

			# Histogram of first half September data in flow_data_int
				mybins = np.linspace(0, 1000, num=15)
				plt.hist(flow_data[(flow_data_int[:,1]==9) & (flow_data[:,2]>=16) ,3], bins = mybins, density = True)
				plt.title('Streamflow for second half September')
				plt.xlabel('Flow [cfs]')
				plt.ylabel('Probability Density')
				plt.ylim((0,0.01))

			# shows plot Hull_Figure_4 (later September data)
				plt.show()`
	* Using these three outputs, it seems clear there is less 'spread' in the daily flows in late september relative to early september
		* Specifically, the most common (mode) flows for both time periods is between 67 and 133 cfs
		* However, the relative frequency of flows in this 'bin' is much higher in late september than early september
		* A comparison of the histograms shows that there seem to be both fewer low flows (< 66 cfs) and high flows (> 133) in late September relative to early September
		* **Casual causal speculation:**
			* Early september flows are subject to both the tail-end of the intensely hot summer and the monsoon season.
			* As such, we expect to have some very low flow events during early September hot and dry, and some very high flow events during early September rainy
			* Late September flows are less likely to be subjected to (on one hand) intense heat and (on the other) intense rain as both the peak summer and monsoon seasons come to a close
			* So late September flows would tend to be less variable around the median.
			* Who knows?
