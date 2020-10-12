# Assignment 7
## Robert Hull
### 10092020
-------------------------------------------------------------------------

This is the readme for `Hull_HW7.py`. Hull_HW7 is an autoregressive streamflow prediction model run in python. The script uses some simple loops and graphing techniques to predict streamflow on the river we are studying in class.

Specifically, this script runs 4 distinct regression ('train') and prediction ('test') scenarios to test the efficacy of the model. These scenarios are based on strategic slicing of the streamflow dataset, as below. (Step 2 in `Hull_HW7.py`)

    train           |          test
    082020 : Now    |  082010 : 082015
    082019 : Now    |  082010 : 082015
    082015 : Now    |  082010 : 082015
    082015 : 08219  |  082019 : Now

Additionally, it uses 5 different combinations of predictive variables to run linear regressions for each of the above scenarios, as described below. (See `reg_list` in `Hull_HW7.py`)

  - 1 week lag streamflow data
  - 1 week & 2 week lag
  - 1 week & 1 month lag
  - The square root of 1 week lag
  - 1 week & 1 week square root & 1 month lag*

nb: each variable above delimited by '&'

Finally, the script loops through all 4 scenarios, and again through all 5 different combinations of predictive variables to: 1) run, 2) assess, and 3) visualize the fit of 20 separate regressions.

The user will find these 20 results useful in understanding the results of different approaches to regressing and predicting streamflow.

Ultimately, however, our prediction for the next two weeks uses the simplest model at our fingertips. The regression uses the 1-week-lagged weekly flow since August 2020 as its predictive variable. (See `Weekly Forecast`)

Finally, we don't use that for the forecast as is easily seen by the final line in the script.

A user should follow these steps to use:
* install the following packages
  * numpy
  * pandas
  * matplotlib
  * sckit-learn (only available through pip install)
* download the latest daily streamflow data at the Verde river at https://waterdata.usgs.gov/nwis/dv/?site_no=09506000&agency_cd=USGS&amp;referred_module=sw
* ensure the data is saved under the title 'streamflow_week7.txt'
* locate the python script Hull_HW7.py relative to the streamflow waterdata like the following: `../../data`
* run the entire script either from a terminal program (like zsh) or in an IME like VSCode or Spyder
* Look at the pretty graphs
* Utilize the final print statement to find weekly predictions
  * Should say 'Weekly Predictions to push to Github'
* Input said predictions into `hull.csv`, located in the forecast git repo
  * Input the entries into the first two comma-delimited spots on row index 7 10/12/20
* Voila

The developer requests that the reviewer supply the following:

1. The week 1 and 2 forecast submission values
# 0,0 I was unable to get the code to execute fully, there was a fatal "key error" on line 111.
2. The week 1 and 2 regression-based forecast values
# 0,0 See above.
3. The code review following the rubric

## Code review:
1. Is the script easy to read and understand? (2 of 3 points)
 - Are variables and functions named descriptively when useful?
 Many variable names are not clear to the user or descriptively named, i.e. nm, w, m, s.

 - Are the comments helpful?
 The comments helped to orient where in the forecast process I was. A good block was describing steps #'s 3,4,5

 - Can you run the script on your own easily?
    I was unable to run the script successfully, there was a fatal "key error" on line 111.
 - Are the doc-strings useful?
    It helps to define what the function does, but is not clear why those values are important.


2. Does the code follow PEP8 style consistently? (2 of 3 points)
 - If not are there specific instances where the script diverges from this style?
 As run, it has 6 errors, due to variables not being defined.

3. Is the code written succinctly and efficiently? (3 of 3 points)
 - Are there superfluous code sections?
 Depending on your point of view, the sections outputting the slope, y-intercept, coefficient of determination are unnecessary, same goes for the plot.

 - Is the use of functions appropriate?
Yes, the function was helpful for doing something.
 - Is the code written elegantly without decreasing readability?
 I think overall the code was reasonably well written.
