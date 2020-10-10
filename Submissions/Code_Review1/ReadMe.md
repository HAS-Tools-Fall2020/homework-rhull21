# Assignment 7
## Robert Hull
### 10092020
-------------------------------------------------------------------------

This is the readme for `Hull_HW7.py`. Hull_HW7 is an autoregressive streamflow prediction model run in python. The script uses some simple loops and graphing techniques to predict streamflow on the river we are studying in class.

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
