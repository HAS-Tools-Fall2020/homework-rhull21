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

2. The week 1 and 2 regression-based forecast values

3. The code review following the rubric
