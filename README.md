# TransectTools

Basic script to make transects with naming scheme. See the comments in the only file here for how to use.

You need a reference shoreline and reference polygon for each section. The idea is to make transects along the reference shoreline and then clip to the polygon. Then it checks that they are in order. Then it updates the attributes to a naming scheme we are using at the USGS. 

Directory structure
G
-C
--RR
----SSS
-------GCRRSSS_reference_shoreline.geojson
-------GCRRSSS_reference_polygon.geojson
-------GCRRSSS_transects.geojson (this is the file that gets made)

It should have the following attributes (longshore_length, G, C, RR, SSS, V, transect_id).

transect_id is GCRRRSSSVlongshore_length. The longshore_length should have six digits.

# Requirements

Python>=3.10, geopandas, pandas, gdal, shapely, sys, math, os, contextily, numpy, warnings, matplotlib



