# Assignment 8 (modified from Ass. 6 and 7)
## Robert Hull
### 10132020

### **SCROLL DOWN TO 'FOR LAURA' FOR QUESTIONS AND ANSWERS**
-------------------------------------------------------------------------

### Overview
This is the readme for `Hull_HW8.py`. Hull_HW8 is an autoregressive streamflow prediction model run in python.

This script is considerably modified and simplified from previous assignments 6 and 7.

The primary 'innovation' is the use of the natural log in making prediction

### Functionality
Its functionality is as follows (described further in steps 1-5 of script)
* Creates one linear regressions each for two forecasts, (i) week 1 and 2 forecasts and (ii) semester forecasts. Two linear regressions total
* For both (i) and (ii):
  * The predictive (independent) variable is the natural logarithm (np.log) of last week's flow data.
  * The predicted (dependent) variable is the natural logarithm (np.log) of this week's flow data
* For (i) week 1 and 2 forecasts:
  * the train ('regression') period is `082020 : Now & 082019 : 122019`
* For (ii) semester forecasts:
  * the train ('regression') period is `year > 2010 and year < 2020`
* iteratively prints the (i) weekly and (ii) semester forecasts in the following forms:
  * (i)
    AR Week 1 and 2 forecast prediction:

        Week 1 =  [69.86]
        Week 2 =  [77.16]

  * (ii)

        AR Semester forecast prediction:
        Week 1 =  [47.17]
        Week 2 =  [56.96]
        Week 3 =  [66.86]
        Week 4 =  [76.6]
        Week 5 =  [85.97]
        Week 6 =  [94.83]
        Week 7 =  [103.06]
        Week 8 =  [110.61]
        Week 9 =  [117.45]
        Week 10 =  [123.59]
        Week 11 =  [129.06]
        Week 12 =  [133.89]
        Week 13 =  [138.13]
        Week 14 =  [141.84]
        Week 15 =  [145.07]
        Week 16 =  [147.86]

### User Interface
A user should be able to run this script from terminal with no alteration.

### Troubleshooting
* install the following packages
  * numpy
  * pandas
  * matplotlib
  * sckit-learn (only available through pip install)
  * datetime
* download the latest daily streamflow data at the Verde river at https://waterdata.usgs.gov/nwis/dv/?site_no=09506000&agency_cd=USGS&amp;referred_module=sw
* ensure the data is saved under the title 'streamflow_week8.txt'
* locate the python script Hull_HW7.py relative to the streamflow waterdata like the following: `../../data`

### For Laura

1. A brief summary of the AR model you built and why. Use whatever graphs you find helpful.
  * My HW7 script included a ton of 'pre-processing' investigation (where there were 20 different regression models) that ultimately impeded my user from being able to run the script.

  * So I wanted to simplify this script as much as possible. I included two regressions, one for (i) the week 1 and 2 forecasts, and (ii) the semester forecasts. Both used a log-log relationship between the predictive variable (1-week lagged streamflow) and the predicted (dependent) variable (streamflow).

  * log-log fit the data much more closely than linear-linear, as seen below:

        **Model = log-log**
          coefficient of determination: 0.72
          intercept: 0.52
          slope: [0.9]

        **Model = linear-linear**
          coefficient of determination: 0.36
          intercept: 85.51
          slope: [0.62]

2. An explanation of how you generated your forecasts and why (i.e. did you use your AR model or not?)
  * I felt like my AR predictions fit a possible reality very well, and so I decided to use them for my forecast

3. A brief summary of what you got out of the peer evaluation. How did you make your script better?
  * My feedback from Scott was SUPER helpful because it just didn't work. Additionally, he found it very confusing and difficult to debug. I think I learned some important lessons here:

    * a) fancy shiny tools (like using exec() to instantiate variables) can be difficult to follow
    * b) anything in a script that is non-essential (like my pre-processing) is an unnecessary opportunity for a script to fail to run
    * c) handling dates, in particular date index, is SUPER tricky (thanks for the links, but I just avoided using the datetime module altogether)
    * d) my documentation / commenting could have been clearer and more thorough

  * I feel like lessons (a-d) are incorporate in my new script, which has:
      - NO shiny tools other than the ones we've learned in class.
      - Doesn't incorporate or use any unnecessary lines of code
      - Takes the most basic approach to slicing dates that I could find
      - is thoroughly (perhaps overly) commented

4. Describe the part of your script that you are most proud of and why.

  *  I'm pretty happy that I figured out the log-log regression, because I've been knocking at the door of that one but getting so hung up on doing fancy things with the code that I didn't have time to explore it very fully.
