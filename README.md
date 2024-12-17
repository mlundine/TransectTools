# TransectTools

Basic script to make transects with naming scheme. See the comments in generate_transects.py for how to use.

You need a reference shoreline and reference polygon for each section. The idea is to make transects along the reference shoreline and then clip to the polygon. Then it checks that they are in order. Then it updates the attributes to a naming scheme we are using at the USGS. 

There is a PyQt UI that can be used as well in transect_tools.py.

Some basic functions are 
* making transects from reference shorelines and reference polygons
* re-ordering jumbled up transects along a given reference shoreline
* flipping transects that are pointed landward
* reversing the index of transects (order along the shoreline)
* extending transects in the seaward or landward direction

The below directory structure is how to set up your folders for organizing files needed.

Directory structure

G#

-C#

--RR##

----SSS###

-------GCRRSSS_reference_shoreline.geojson (you provide this)

-------GCRRSSS_reference_polygon.geojson (you provide this)

-------GCRRSSS_transects.geojson (this is the file that gets made)

It should have the following attributes (longshore_length, G, C, RR, SSS, V, transect_id).

transect_id is GCRRSSSVlongshore_length. The longshore_length should have six digits.

# Requirements/Setup

If you have a CoastSeg conda environment set up already, this code should work in that environment.

Python>=3.10, geopandas, pandas, gdal, shapely, sys, math, os, numpy, warnings, matplotlib



