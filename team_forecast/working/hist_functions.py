
# %%
# module
import pandas as pd
import matplotlib.pyplot as plt

# %%
# Function


def hist(data_in):
    """This function generates two histograms based on the input of a dataset of
    streamflow stored in natural log format

    Abigail, put in train['flow']

    data_in = a series from a pandas dataframe containing streamflow data in log

    shows two histograms, one of the data represented in log space and
    the other represented in arithmetic space

    the purpose is to show how doing your autoregression with 'log' data helps
    to normalize the underlying data, and generate better fits to training data

    returns nothing

    """
    # Histogram of flow data in natural log space
    textstr1 = '\n'.join((
                        'The flow data have',
                        'a nearly normal distribution',
                        'in log space'))
    fig, ax = plt.subplots()
    ax.hist(data_in, bins=10)
    ax.set(xlabel='flow in natural log scale', ylabel='frequency', ylim=(0, 100))
    ax.text(0.4, 0.95, textstr1, transform=ax.transAxes, fontsize=14,
            verticalalignment='top')
    plt.show()

    # Histogram of flow data in natural log space
    textstr2 = '\n'.join((
                        'The flow data have',
                        'a very skewed distribution',
                        'in arithmetic space'))
    fig, ax = plt.subplots()
    ax.hist(np.exp(data_in), bins=10)
    ax.set(xlabel='flow in arithmetic scale', ylabel='frequency', ylim=(0, 100))
    ax.text(0.4, 0.95, textstr2, transform=ax.transAxes, fontsize=14,
            verticalalignment='top')
    plt.show()


