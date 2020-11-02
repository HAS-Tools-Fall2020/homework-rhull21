# -------------------------------
# Quinn Hull
# HW 10 - mapping
# 11012020
# Modified from Week10_starterscript.py
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


# %%
# 1) Gages II USGS stream gauge dataset:
# Download here:
# https://water.usgs.gov/GIS/metadata/usgswrd/XML/gagesII_Sept2011.xml#stdorder

# 1a) file
file = os.path.join('../../spatial_data_nongit/gagesII_9322_point_shapefile',
                    'gagesII_9322_sept30_2011.shp')
gages = gpd.read_file(file)

# 1b) Investigate
investigate_gdp(gages)


# %%
# 2) Rivers
# Download here: 
# https://www.sciencebase.gov/catalog/item/4fb55df0e4b04cb937751e02

# 2a) file
filepath = '../../spatial_data_nongit/Lakes_and_Rivers_Shapefile/' \
            'NA_Lakes_and_Rivers/data'
filename = 'hydrography_l_rivers_v2.shp'
file = os.path.join(filepath,
                    filename)
rivers = gpd.read_file(file)

# 2b) Investigate
investigate_gdp(rivers)

# %%
# 3) GWSI (Groundwater Site Inventory)
# https://new.azwater.gov/gis
# 3a) file
filepath = '../../spatial_data_nongit/GWSI_ZIP_10162020/Shape/'
filename = 'GWSI_SITES.shp'
file = os.path.join(filepath,
                    filename)
gwsi = gpd.read_file(file)

# 3b) Investigate
investigate_gdp(gwsi)

# %%
# 4) 	NHD 20200616 for Arizona State or Territory Shapefile Model Version 2.2.1
# https://www.usgs.gov/core-science-systems/ngp/national-hydrography/access-national-hydrography-products
# https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View
# https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View#productSearch

# 4a)
filepath = '../../spatial_data_nongit/Shape/'
filename = 'WBDHU6.shp'
file = os.path.join(filepath,
                    filename)
huc = gpd.read_file(file)
# 4b) Investigate
investigate_gdp(huc)


# %%
# 4c) Arizona extent
# tl_2016_04_cousub/
# https://catalog.data.gov/dataset/tiger-line-shapefile-2016-state-arizona-current-county-subdivision-state-based
# 4e)
filepath = '../../spatial_data_nongit/tl_2016_04_cousub/'
filename = 'tl_2016_04_cousub.shp'
file = os.path.join(filepath,
                    filename)
az = gpd.read_file(file)
# 4f) Investigate
investigate_gdp(az)

# %%
# Add some points
# UA:  32.22877495, -110.97688412
# STream gauge:  34.44833333, -111.7891667
point_list = np.array([[-111.7891667, 34.44833333]])

# make these into spatial features
point_geom = [Point(xy) for xy in point_list]
point_geom

# map a dataframe of these points
point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs=huc.crs)


# %%
# 5) fix any crs issues
# 5a) Check crs
print("gages crs =", gages.crs, "\n")
print("rivers crs =", rivers.crs, "\n")
print("gwsi crs =", gwsi.crs, "\n")
print("huc crs =", huc.crs, "\n")
print("az crs =", az.crs, "\n")
print("point crs =", point_df.crs, "\n")

# 5b) Convert each crs to be the same
rivers_proj = rivers.to_crs(gages.crs)
gwsi_proj = gwsi.to_crs(gages.crs)
huc_proj = huc.to_crs(gages.crs)
az_proj = az.to_crs(gages.crs)
point_df_proj = point_df.to_crs(gages.crs)

# 5c) Check to see if results stuck
print("gages crs =", gages.crs, "\n")
print("rivers crs =", rivers_proj.crs, "\n")
print("gwsi crs =", gwsi_proj.crs, "\n")
print("huc crs =", huc_proj.crs, "\n")
print("az crs =", az_proj.crs, "\n")
print("az crs =", point_df_proj.crs, "\n")

# %%
# 6) Clip data extent for rivers, gwsi, and gages based on huc
# From: https://geopandas.org/reference/geopandas.clip.html
rivers_proj_az = gpd.clip(rivers_proj, az_proj, True)
gwsi_proj_az = gpd.clip(gwsi_proj, az_proj, True)
gages_az = gpd.clip(gages, az_proj, True)

# %%
# 7) Make a map
xmin, xmax, ymin, ymax = az_proj.total_bounds[0], az_proj.total_bounds[2], \
                            az_proj.total_bounds[1], az_proj.total_bounds[3]

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
az_proj.plot(ax=ax, color='grey', zorder=0)
huc_proj.boundary.plot(ax=ax, color='black', label='huc', zorder=5)
rivers_proj_az.plot(ax=ax, color='blue', label='big rivers', zorder=6)
gwsi_proj_az.plot(ax=ax, color='green', label='groundwater sites',
                  zorder=3)
gages_az.plot(ax=ax, color='red', marker='*',
              label='river gages', zorder=4)
point_df_proj.plot(ax=ax, color='orange', markersize=45,
                   label='Verde River Gage', zorder=10)
ax.set_title('Arizona Hydrogeologic Features')
ax.set_xlabel('Easting')
ax.set_ylabel('Northing')
ax.legend()
plt.show()

# %%
