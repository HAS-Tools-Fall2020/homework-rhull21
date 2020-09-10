## Assignment 3
Robert Hull
09102020

-------

### Assignment Questions

1. Describe the variables flow, year, month, and day. What type of objects are they, what are they composed of, and how long are they?
    * flow, date, year, month, and day are all lists
    * they are composed of many items of type:
        * flow -> 'float'
        * month -> 'int'
        * year -> 'int'
        * day -> 'int'
        * date -> 'str' 
    * each list is identical in length (1106346 items)

2. How many times was the daily flow greater than your prediction in the month of September (express your answer in terms of the total number of times and as a percentage)?
    * My prediction (I'm assuming) is my prediction from row 8/31/2020, column 'week1'. 
        * = 60 cfs
    * For the first 10 days of September in 2020 (through 09/10/2020)
        * = 3 times
        * = 3 times / 9 days = 33%
    * For all Septembers back to 1989
        * Flow exceeded expections  893 times in September, or 95 percent of times

3. How would your answer to the previous question change if you considered only daily flows in or before 2000? Same question for the flows in or after the year 2010? (again report total number of times and percentage)
    * For all Septembers in and before 2000
        * Flow exceeded expections  360 times in September, or 100.0 percent of times
    * For all flows in and after 2010
        * Flow exceeded expections  285 times in September, or 92 percent of times

4. How does the daily flow generally change from the first half of September to the second?
    * For the first half of Septembers, Min =  36.6  Max =  1280.0  Mean =  179.68713080168774  Std =  171.4750267303949
    * For the second half of Septembers, Min =  51.2  Max =  5590.0  Mean =  169.8541935483871  Std =  371.9750870786179

    * I would summarize by saying there is a lot of variation year-to-year in September and that although the mean is slightly lower in the second half in September than in the first half, its not statistically significant. Flow in the latter half tends to be more variable (larger std)

### Justification for Forecast
    * I made this enormous for-loop conditional thing that is probably super inefficient (it takes a long time to run) but I couldn't figure out the list collections things well enough. 

    * From this I decided to find the average for every single week in the forecast 1-16 from previous years starting in 2010. I used those as my projections:

    `196, 160, 157, 137, 112, 115, 188, 132, 130, 135, 145, 157, 179, 186, 264, 389`



