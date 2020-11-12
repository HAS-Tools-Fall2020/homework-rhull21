# Forecast Eval Quinn and Ben

## Forecast Eval Tasks:

### 'git' organized
  0. Create branch of repo
    * follow readme

  1. Archive old scripts
    * taking care to make sure there are no hidden dependencies
    * Take note of which need archival below in ('existing scripts in forecast eval repo')
    * annotate that these are 'archived' in header and in commit message (and readme?)

  2. create bonus folder
    * old bonus scripts won't work, but it doesn't matter
    * annotate that these are 'archived' in header and in commit message
    * edit the 'write_bonus' function so that (and readme?)

  3. create an 'asset' file to contain all pngs
    * ensure that the readme.md file know to look in asset file
    * ensure that the n

  4. Document the forecast_evaluation workflow (i.e. what the code is really doing)
    * Create an illustrator file showing the workflow/connectivity of functions / scripts
      * add both file and png to assets file
    * Add this workflow chart to the readme with descriptive text

  5. Update the readme
    * Add step 4 (above)
    * Ensure filenames and steps described are consistent
    * Include an 'etiquette' notice so that the directory doesn't get trashed and confusing in the future


### plot pretty
  0. Wait until 'git organized' is complete
  1. Keep in mind new dependencies establish in prior step

### bonus pt function
  * note the function 'write_bonus' needs to be called by the bonus function we write
  * note that the files and functions called by our bonus pt function need to respect the new location of the function

## Misc

### ToDo:
  * Get up and running with Discord

### Ben's contact info
  * 5209094886

### Existing Scripts in Forecast Eval Repo

  1. Summarzie_Scores.py
  * This script summarizes the scores from the weekly evaluations

  * Potential additions:
  * Get weekly totals
  * get totals by forecast type and bonus points
  * Condense the bonus points for each week into one column
  * Calculate ranks and write this out

  2. Bonus_week11.py
  * Abigail and Danielle's Week 11 Bonus script
  * %%
  * This week's bonus points will go to those with lowest cumulative
  * bonus points

  3. Get_Observations.py
  * This script downloads the observations from USGS aggreages
  * to weekly and saves as a csv

  * Potential additions:
  * Make this a function

  * Modify so it reads in the previous observation file
  * and only adds in the new obs

  * Have this automatically check what day it is
  * and figure out what weeks are complete
  * rather than requiring a week number input

  4. Score_Seasonal.py
  * This script summarizes the scores from the weekly evaluations
  * Potential additions:
  * Adding a scoring component
  * Adding something to output ranks by week

  5. Score_Weekly.py
  * This script is used to score the 1 week and 2 week forecasts

  6. Scoreboard.py
  * This script calcualtes the total scores for everyone using
  * the summary outputs from the score_weekly.py

  7. Summarzie_Scores.py
  * Potential additions:
  * Get weekly totals
  * get totals by forecast type and bonus points
  * Condense the bonus points for each week into one column
  * Calculate ranks and write this out

  8. crosscheck_teams.py
  * This script is to make sure all individual team members have the same forecast
  * Created by Danielle and Abigail (11/10/2020)

  9. eval_functions.py
  * Forecast Functions Week 8

  10. forecast_analysis.py
  *

  11. plot_functions.py
  * This script contains the functions used for plotting different plots in
  * other scripts used for evaluation.\
  * Author: Shweta Narkhede and Camilo Salcedo
  * Created on: Oct 24th, 2020
