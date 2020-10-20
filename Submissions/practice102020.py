# %%
import os
import numpy as np
import pandas as pd
# may need to pip install scikit-learn, not available on conda
from sklearn.linear_model import LinearRegression

# adjust path as necessary
filename = 'streamflow_week1.txt'
filepath = os.path.join('../data', filename)
print(os.getcwd())
print(filepath)

# read in data
data = pd.read_table(filepath, sep='\t', skiprows=30,
                     names=['agency_cd', 'site_no',
                            'datetime', 'flow', 'code'],
                     parse_dates=['datetime'],
                     index_col='datetime'
                     )
# %%
# January 3-5
data.iloc[2:5][['flow']]
data.iloc[2:5,2]
# These are the same

# %%
data.loc['1989-01-03':'1989-01-05']

# %%
data[(data.index >= '1989-01-03') & (data.index <= '1989-01-05')]

# %%
data[(data.index.month == 1) & (data.index.year == 1989) & (data.index.day >= 3) & (data.index.day <= 5)]

# %%
data[(data.index == '1989') & (data.index.month == 1)]