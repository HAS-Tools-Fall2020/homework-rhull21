## Group name: Dell for the Win?
## Team members:
### Quinn Hull, Alexa Marcovecchio, Abigail Kahler


### Week 1 Forecast: 132.72 cfs

### Week 2 forecast: 140.33 cfs

#### Summary of our collaboration:
*What did each team member bring to the table,\
who did what, and how did you decide how to combine things?*

Our group worked well together, with Quinn offering his as the source\
code, Alexa providing her 16 week forecast code, and Abigail exploring computer\
issues while improving her two-week forecast code. We worked\
individually on sections of code and then coordinated their
combination.\
Abigail completed the two-week forecast, the ReadMe documentation, and\
compiled functions into a separate script, Alexa provided the 16 week\
forecast, building upon her previous code by creating loops and a\
function, and Quinn created the multilayered map and the plot, while also\
facilitating communication and coordination of our efforts.


#### Summary of our forecast:
*This should be written as a narrative summary without any blocks of code.\
It should summarize the inputs and approach used and must include at\
least 1 map and one graph.*\
\
Our approach was to center our forecast around Quinn's method of using the\
natural log of flow.
To date, this has given better results than the other processes we have tried.\
We also adopted a "divide and conquer" distribution of work to minimize\
conflicting updates to the repo.

Our code utilizes three functions, which are stored in a separate file. The\
first, *getForecastDates()*, creates a dataframe of forecast dates from csv\
files, within columns separating start and end dates by year, month, and day.\
Another, *forecast*, is specific to the two-week forecast with an input of the\
beginning flow value. The final function, *investigate_gdp*, reads in a\
geodataframe and outputs print statements identifying relevant attributes.\

The map consists of n layers,
# map details here
...... . Centered on the Verde River, it provides\
perspective on tributaries and relevance of other stream gages with respect to\ the river.\
The figure provided is a depictions of...
# plot details here
