# -------------------------------
# Group Name: ??
# source mapping
# 11032020
# Modified from Week10_starterscript.py
# Modified form Hull_HW10_maps.py
# -------------------------------
# %%
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import os
import geopandas as gpd
import fiona
from shapely.geometry import Point
# import contextily as ctx
from pprint import pprint

# %% functions


def investigate_gdp(gdp):
    """The function reads in a geodataframe
    with the intention of printing interesting
    attributes of that dataframe.

    mostly print statements

    returns the given gdp
    """

    print("Details from the given geodataframe: ", "\n")
    # initial attributes
    print("type =", type(gdp), "\n")
    print("columns =", gdp.columns, "\n")
    print("shape =", gdp.shape, "\n")
    gdp.head()
    print("\n")

    # Looking at the read-only method
    pprint(vars(gdp))
    print("geom =", gdp.geom_type, "\n")
    print("crs =", gdp.crs, "\n")
    print("spatial bounds =", gdp.total_bounds, "\n")


def add_pt_gdf(point_l, crs_i, gpd_in, nm_pts):
    """The function reads in a numpy array of one or multiple spatial data values
    with the intention of converting that into a pandas dataframe
    and then appending this to the end of an existing pandas geodataframe

    inputs:
    point_l = a 2-D numpy array of spatial data values (like easting, northing)
        or (like lat, long)
    crs_in = the coordinate system of the dataframe, a crs object
    gpd_in = the pandas dataframe containing geodataframe info
    nm_pts = the name you would like to give the new row in the dataframe

    output:
    the inputted pandas dataframe container of gdp and other info
    with a new record containing a gdp oflat / long data
    """

    # make these into spatial features
    point_geom = [Point(xy) for xy in point_l]

    # create point_df geodataframe
    point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                                crs=crs_i)

    # add to gpd_df
    gpd_in = gpd_in.append({'names': nm_pts,
                            'file': '', 'gpd': point_df},
                           ignore_index=True)

    return gpd_in


# %%
# 1) create a df of files, filepath, and name
filepath = '../../spatial_data_nongit/'
gpd_df = pd.DataFrame(columns=['names', 'file', 'gpd'])

names = ['gages', 'rivers', 'gwsi', 'huc', 'az']

gpd_df['names'] = names

filenames = ['gagesII_9322_point_shapefile/gagesII_9322_sept30_2011.shp',
             'USA_Rivers_and_Streams-shp/'
             '9ae73184-d43c-4ab8-940a-c8687f61952f2020328-1-r9gw71.0odx9.shp',
             'GWSI_ZIP_10162020/Shape/GWSI_SITES.shp',
             'Shape/WBDHU10.shp',
             'tl_2016_04_cousub/tl_2016_04_cousub.shp']

gpd_df['file'] = filenames
gpd_df['file'] = filepath + gpd_df['file']

# Import data into df and add to dataframe
for i in range(len(gpd_df)):
    gpd_df.iat[i, 2] = gpd.read_file(gpd_df['file'].iloc[i])

# %%
# 2) Add some points
# Stream gauge:  34.44833333, -111.7891667
point_list = np.array([[-111.7891667, 34.44833333]])

# extract crs from huc (desired to apply)
crs_in = gpd_df['gpd'].iloc[
                            gpd_df.index[
                                         gpd_df['names'
                                                ] == 'huc'].tolist()[0]
                            ].crs

# add a line containing point_list to gpd_df including data frame of points
gpd_df = add_pt_gdf(point_list, crs_in, gpd_df, 'points_df')

# %%
# 3) fix any crs issues
# 4) Clip data extent for all layers based on extent of arizona

# clip set
clip_set = gpd_df['gpd'].iloc[
                            gpd_df.index[
                            gpd_df['names'
                                   ] == 'az'].tolist()[0]]

# crs set
# exract crs to set all to (from gages)
crs_set = clip_set.crs

# look through all gdf and (a) fix crs issues and (b) clip domains
for i in range(len(gpd_df)):
    gpd_df['gpd'].iloc[i].to_crs(crs_set, inplace=True)
    print(gpd_df['gpd'].iloc[i].crs)
    # clip is not working with this larger dataset
    gpd_df.iat[i, 2] = gpd.clip(gpd_df['gpd'].iloc[i], clip_set, False)


# %%
# 6) Make a map of just Verde River Area
extent = gpd_df['gpd'].iloc[1][gpd_df['gpd'].iloc[1]['Name'] == 'Verde River']
salt = gpd_df['gpd'].iloc[1][gpd_df['gpd'].iloc[1]['Name'] == 'Salt River']

rangef = (extent.total_bounds[2] - extent.total_bounds[0])
# clip extent
xmin, xmax, ymin, ymax = extent.total_bounds[0]-rangef, \
                         extent.total_bounds[2]+rangef, \
                         extent.total_bounds[1]-rangef, \
                         extent.total_bounds[3]+rangef

# create plot
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

colorList = ['red', 'blue', 'green', 'grey', 'black', 'yellow']
alphaList = [1, 1, 0.2, 0.5, 0.7, 1]
zorderList = [6, 4, 3, 2, 1, 7]
nameList = ['USGS Stream Gages', 'Arizona Major Rivers',
            'USGS Groundwater Sites', 'HUC 10 Watersheds',
            'AZ', 'Verde River Stream Gage']
markerList = ['X', '_', '.', '_', '_', '*']

# loop through all gdps:
for i in range(len(gpd_df)):
    if gpd_df['names'].iloc[i] == 'huc':
        gpd_df['gpd'].iloc[i].boundary.plot(ax=ax,
                                            label=nameList[i],
                                            zorder=zorderList[i],
                                            edgecolor=colorList[i],
                                            alpha=alphaList[i])

    else:
        gpd_df['gpd'].iloc[i].plot(ax=ax,
                                   label=nameList[i],
                                   zorder=zorderList[i],
                                   color=colorList[i],
                                   alpha=alphaList[i],
                                   marker=markerList[i]
                                   )

# plot just Verde River
extent.plot(ax=ax,
            label='Verde River',
            zorder=5,
            color='purple',
            linestyle='-.',
            linewidth=5)

# plot just Salt River
salt.plot(ax=ax,
          label='Salt River',
          zorder=5,
          color='orange',
          linestyle=':',
          linewidth=5,
          alpha=0.5)

ax.set_title('Arizona Hydrologic Features')
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.legend(loc='lower left')
plt.show()

# %%
