##import packages
from osgeo import ogr, gdal
gdal.UseExceptions() 
from shapely.geometry import MultiLineString, LineString, Point
from shapely import wkt
import sys, math
import os
import geopandas as gpd
import pandas as pd
import contextily as cx
import numpy as np
import shapely
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def LineString_to_arr(line):
    """
    Makes an array from linestring
    inputs: line
    outputs: array of xy tuples
    """
    listarray = []
    for pp in line.coords:
        listarray.append(pp)
    nparray = np.array(listarray)
    return nparray

def arr_to_LineString(coords):
    """
    Makes a line feature from a list of xy tuples
    inputs: coords
    outputs: line
    """
    points = [None]*len(coords)
    i=0
    for xy in coords:
        points[i] = shapely.geometry.Point(xy)
        i=i+1
    line = shapely.geometry.LineString(points)
    return line

def simplify_lines(lines, tolerance=25):
    """
    Uses shapely simplify function to smooth out the extracted shorelines
    inputs:
    shapefile: path to merged shoreline shapefiles
    tolerance (optional): simplification tolerance (meters)
    outputs:
    save_path: path to smooth shapefile
    """
    lines['geometry'] = lines['geometry'].simplify(tolerance)
    return lines

def chaikins_corner_cutting(coords, refinements=5):
    """
    Smooths out lines or polygons with Chaikin's method
    """
    i=0
    for _ in range(refinements):
        L = coords.repeat(2, axis=0)
        R = np.empty_like(L)
        R[0] = L[0]
        R[2::2] = L[1:-1:2]
        R[1:-1:2] = L[2::2]
        R[-1] = L[-1]
        coords = L * 0.75 + R * 0.25
        i=i+1
    return coords

def smooth_lines(shorelines_path, simplify=50):
    """
    Smooths out shorelines with Chaikin's method
    saves output with '_smooth' appended to original filename in same directory

    inputs:
    shorelines (str): path to extracted shorelines
    outputs:
    save_path (str): path of output file
    """
    shorelines = gpd.read_file(shorelines_path)
    shorelines = simplify_lines(shorelines, tolerance=50)
    new_lines = shorelines.copy()
    for i in range(len(new_lines)):
        line = new_lines.iloc[i]['geometry']
        coords = LineString_to_arr(line)
        refined = chaikins_corner_cutting(coords)
        refined_geom = arr_to_LineString(refined)
        new_lines['geometry'][i] = refined_geom

    new_lines.to_file(shorelines_path)
    return shorelines_path

def smooth_lines_df(shorelines_df):
    """
    Smooths out shorelines with Chaikin's method

    inputs:
    shorelines (geodataframe): shorelines geodataframe
    outputs:
    new_lines (geodataframe): smooth shorelines geodataframe
    """
    new_lines = shorelines_df.copy()
    for i in range(len(new_lines)):
        line = new_lines.iloc[i]['geometry']
        coords = LineString_to_arr(line)
        refined = chaikins_corner_cutting(coords)
        refined_geom = arr_to_LineString(refined)
        new_lines['geometry'][i] = refined_geom

    return new_lines

def utm_to_wgs84_file(geojson_file):
    """
    Converts utm to wgs84
    inputs:
    geojson_file (path): path to a geojson in utm
    outputs:
    geojson_file_wgs84 (path): path to a geojson in wgs84
    """
    geojson_file_wgs84 = os.path.splitext(geojson_file)[0]+'_wgs84.geojson'

    gdf_utm = gpd.read_file(geojson_file)
    wgs84_crs = 'epsg:4326'

    gdf_wgs84 = gdf_utm.to_crs(wgs84_crs)
    gdf_wgs84.to_file(geojson_file_wgs84)
    return geojson_file_wgs84

def wgs84_to_utm_file(geojson_file):
    """
    Converts wgs84 to UTM
    inputs:
    geojson_file (path): path to a geojson in wgs84
    outputs:
    geojson_file_utm (path): path to a geojson in utm
    """

    geojson_file_utm = os.path.splitext(geojson_file)[0]+'_utm.geojson'

    gdf_wgs84 = gpd.read_file(geojson_file)
    utm_crs = gdf_wgs84.estimate_utm_crs()

    gdf_utm = gdf_wgs84.to_crs(utm_crs)
    gdf_utm.to_file(geojson_file_utm)
    return geojson_file_utm
def wgs84_to_utm_df(geo_df):
    """
    Converts wgs84 to UTM
    inputs:
    geo_df (geopandas dataframe): a geopandas dataframe in wgs84
    outputs:
    geo_df_utm (geopandas  dataframe): a geopandas dataframe in utm
    """
    utm_crs = geo_df.estimate_utm_crs()
    gdf_utm = geo_df.to_crs(utm_crs)
    return gdf_utm

def utm_to_wgs84_df(geo_df):
    """
    Converts utm to wgs84
    inputs:
    geo_df (geopandas dataframe): a geopandas dataframe in utm
    outputs:
    geo_df_wgs84 (geopandas  dataframe): a geopandas dataframe in wgs84
    """
    wgs84_crs = 'epsg:4326'
    gdf_wgs84 = geo_df.to_crs(wgs84_crs)
    return gdf_wgs84

def geojson_to_shapefile(my_geojson, out_dir=None):
    """
    converts geojson to shapefile
    inputs:
    my_geojson (str): path to the geojson
    out_dir (optional, str): directory to save to
    if this is not provided then shapefile is saved
    to same directory as the input shapefile
    """
    name = os.path.basename(my_geojson)
    name_no_ext = os.path.splitext(my_geojson)[0]
    folder = os.path.dirname(my_geojson)
    
    if out_dir == None:
        new_name = os.path.join(folder, name_no_ext+'.shp')
    else:
        new_name = os.path.join(out_dir, name_no_ext+'.shp')
        
    myshpfile = gpd.read_file(my_geojson)
    try:
        myshpfile['date'] = myshpfile['date'].astype('str')
    except:
        pass
    myshpfile.to_file(new_name)
    return new_name

def shapefile_to_geojson(my_shape_file, out_dir=None):
    """
    converts shapefile to geojson
    inputs:
    my_shape_file (str): path to the shapefile
    out_dir (optional, str): directory to save to
    if this is not provided then geojson is saved
    to same directory as the input shapefile
    """
    name = os.path.basename(my_shape_file)
    name_no_ext = os.path.splitext(my_shape_file)[0]
    folder = os.path.dirname(my_shape_file)
    
    if out_dir == None:
        new_name = os.path.join(folder, name_no_ext+'.geojson')
    else:
        new_name = os.path.join(out_dir, name_no_ext+'.geojson')
        
    my_geojson = gpd.read_file(my_shape_file)
    my_geojson.to_file(new_name, driver='GeoJSON')
    return new_name
"""
Needs to be a shapefile for input reference shoreline
Also the shapefile can only have one line currently
"""
## http://wikicode.wikidot.com/get-angle-of-line-between-two-points
## angle between two points
def getAngle(pt1, pt2):
    x_diff = pt2.x - pt1.x
    y_diff = pt2.y - pt1.y
    return math.degrees(math.atan2(y_diff, x_diff))


## start and end points of chainage tick
## get the first end point of a tick
def getPoint1(pt, bearing, dist):
    angle = bearing + 90
    bearing = math.radians(angle)
    x = pt.x + dist * math.cos(bearing)
    y = pt.y + dist * math.sin(bearing)
    return Point(x, y)


## get the second end point of a tick
def getPoint2(pt, bearing, dist):
    bearing = math.radians(bearing)
    x = pt.x + dist * math.cos(bearing)
    y = pt.y + dist * math.sin(bearing)
    return Point(x, y)

def make_transects(input_path,
                   transect_spacing,
                   transect_length):
    """
    Generates normal transects to an input line shapefile
    inputs:
    input_path: path to shapefile containing the input line
    transect_spacing: distance between each transect in meters
    transect_length: length of each transect in meters
    outputs:
    output_path: path to output shapefile containing transects
    """

    output_path = os.path.splitext(input_path)[0]+'_transects_'+str(transect_spacing)+'m.shp'
    ## set the driver for the data
    driver = ogr.GetDriverByName("Esri Shapefile")
    
    ## open the shapefile in write mode (1)
    ds = driver.Open(input_path)
    shape = ds.GetLayer(0)
    
    ## distance between each points
    distance = transect_spacing
    ## the length of each tick
    tick_length = transect_length

    ## output tick line fc name
    ds_out = driver.CreateDataSource(output_path)
    layer_out = ds_out.CreateLayer('line',shape.GetSpatialRef(),ogr.wkbLineString)

    ## list to hold all the point coords
    list_points = []


    ## distance/chainage attribute
    chainage_fld = ogr.FieldDefn("CHAINAGE", ogr.OFTReal)
    layer_out.CreateField(chainage_fld)
    ## check the geometry is a line
    first_feat = shape.GetFeature(0)

    ln = first_feat
    ## list to hold all the point coords
    list_points = []
    ## set the current distance to place the point
    current_dist = distance
    ## get the geometry of the line as wkt
    line_geom = ln.geometry().ExportToWkt()
    ## make shapely LineString object
    shapely_line = LineString(wkt.loads(line_geom))
    ## get the total length of the line
    line_length = shapely_line.length
    ## append the starting coordinate to the list
    list_points.append(Point(list(shapely_line.coords)[0]))
    ## https://nathanw.net/2012/08/05/generating-chainage-distance-nodes-in-qgis/
    ## while the current cumulative distance is less than the total length of the line
    while current_dist < line_length:
        ## use interpolate and increase the current distance
        list_points.append(shapely_line.interpolate(current_dist))
        current_dist += distance
    ## append end coordinate to the list
    list_points.append(Point(list(shapely_line.coords)[-1]))
    list_points = list_points[1:-1]

    ## add lines to the layer
    ## this can probably be cleaned up better
    ## but it works and is fast!
    for num, pt in enumerate(list_points, 1):
        ## start chainage 0
        if num == 1:
            angle = getAngle(pt, list_points[num])
            line_end_1 = getPoint1(pt, angle, tick_length/2)
            angle = getAngle(line_end_1, pt)
            line_end_2 = getPoint2(line_end_1, angle, tick_length)
            tick = LineString([(line_end_1.x, line_end_1.y), (line_end_2.x, line_end_2.y)])
            feat_dfn_ln = layer_out.GetLayerDefn()
            feat_ln = ogr.Feature(feat_dfn_ln)
            feat_ln.SetGeometry(ogr.CreateGeometryFromWkt(tick.wkt))
            feat_ln.SetField("CHAINAGE", 0)
            layer_out.CreateFeature(feat_ln)

        ## everything in between
        if num < len(list_points) - 1:
            angle = getAngle(pt, list_points[num])
            line_end_1 = getPoint1(list_points[num], angle, tick_length/2)
            angle = getAngle(line_end_1, list_points[num])
            line_end_2 = getPoint2(line_end_1, angle, tick_length)
            tick = LineString([(line_end_1.x, line_end_1.y), (line_end_2.x, line_end_2.y)])
            feat_dfn_ln = layer_out.GetLayerDefn()
            feat_ln = ogr.Feature(feat_dfn_ln)
            feat_ln.SetGeometry(ogr.CreateGeometryFromWkt(tick.wkt))
            feat_ln.SetField("CHAINAGE", distance * num)
            layer_out.CreateFeature(feat_ln)

        ## end chainage
        if num == len(list_points):
            angle = getAngle(list_points[num - 2], pt)
            line_end_1 = getPoint1(pt, angle, tick_length/2)
            angle = getAngle(line_end_1, pt)
            line_end_2 = getPoint2(line_end_1, angle, tick_length)
            tick = LineString([(line_end_1.x, line_end_1.y), (line_end_2.x, line_end_2.y)])
            feat_dfn_ln = layer_out.GetLayerDefn()
            feat_ln = ogr.Feature(feat_dfn_ln)
            feat_ln.SetGeometry(ogr.CreateGeometryFromWkt(tick.wkt))
            feat_ln.SetField("CHAINAGE", int(line_length))
            layer_out.CreateFeature(feat_ln)

    del ds
    return output_path

def clip_transects(transects_path, area_path):
    """
    Clips transects to a given area, saves to new geojson
    inputs:
    transects_path (str): path to the transects (geojson)
    area_path (str): path to the polygon (geojson)
    outputs:
    save_path (str): path to the clipped transects
    """
    save_path = os.path.splitext(transects_path)[0]+'_clipped.geojson'
    transects = gpd.read_file(transects_path)
    area = gpd.read_file(area_path)
    clipped_transects = gpd.clip(transects, area)
    clipped_transects.to_file(save_path)
    return save_path

def re_index_with_ref_shoreline(transects_path, ref_shore_path, G, C, RR, SSS, version_name, tolerance=50, dist_int=5):
    """
    takes a set of transects with jumbled up index and uses reference shoreline
    to reset the index
    the tolerance might need to be played with for certain sections of coastline
    inputs:
    transects_path (str): path to the transects
    ref_shore_path (str): path to the reference shoreline
    G (str): global region
    C (str): coastal usa region
    RR (str): sub region
    SSS (str): shoreline section
    tolerance (int, optional, default=10): tolerance for simplifying the reference shoreline, meters
    dist_int (int, optional, default=30): when to stop computing cumulative distance along ref shoreline,
                                          basically how close to get to the transect intersection before
                                          finishing computing the cumulative distance
    outputs:
    new_transects_path (str): path to the new transects
    """
    transects = gpd.read_file(transects_path)
    transects = wgs84_to_utm_df(transects)
    ref_shore = gpd.read_file(ref_shore_path)
    ref_shore = wgs84_to_utm_df(ref_shore)
    ref_shore = simplify_lines(ref_shore, tolerance=tolerance)
    ref_shore = smooth_lines_df(ref_shore)
    ref_shore = ref_shore.sort_values('OBJECTID',ascending=True).reset_index()
    points = []
    for shore in ref_shore['geometry']:
        for point in shore.coords:
            points.append(point)
    ref_shore_real = shapely.LineString(points)
    gdf = gpd.GeoDataFrame(pd.DataFrame({'OBJECTID':['1']}),geometry=[ref_shore_real], crs=ref_shore.crs)
    f, ax = plt.subplots()
    gdf.plot(ax=ax, column='OBJECTID', legend=True)
    plt.show()

##    ##check that there is only one reference shoreline and that it looks correct
##    ref_shore_check = input('Save? yes(y) or no (n)')
##    if ref_shore_check == 'y':
##        ref_shore_real_wgs84 = utm_to_wgs84_df(gdf)
##        ref_shore_real_wgs84.to_file(ref_shore_path)
##        print('ref_shore_saved to ' + ref_shore_path)

    ##loop over transects
    intersections = [None]*len(transects)
    distances = [None]*len(transects)
    for i in range(len(transects)):
        t = transects.iloc[i]
        ##find the intersection point with the reference shoreline
        intersect = ref_shore_real.intersection(t['geometry'])
        cumulative_distance = 0
        j=0
        for j in range(1, len(ref_shore_real.coords)):
            start_point = shapely.Point(ref_shore_real.coords[j-1])
            end_point = shapely.Point(ref_shore_real.coords[j])
            distance = end_point.distance(start_point)
            distance_int = intersect.distance(end_point)
            if distance_int <=30:
                break
            else:
                cumulative_distance = cumulative_distance + distance
        distances[i] = cumulative_distance
    if np.any(np.isnan(distances))==True:
        return
    transects['distances'] = distances
    transects = transects.sort_values('distances').reset_index(drop=True)
    transects['longshore_length'] = 50*transects.index
    names = [None]*len(transects)
    for index, row in transects.iterrows():
        name = G + C + RR + SSS + version_name + str(row['longshore_length']).zfill(6)
        names[index] = name
    transects['transect_id'] = names

    
    transects = transects.to_crs(epsg=3857)
    ax = transects.plot(column='distances', legend=True)
    gdf = gdf.to_crs(epsg=3857)
    gdf.plot(ax=ax)
    cx.add_basemap(ax,
               source=cx.providers.Esri.WorldImagery,
               attribution=False)
    plt.show()
    transects = transects.drop(columns=['distances'])
    try:
        transects = transects.drop(columns=['Shape_Length'])
    except:
        continue
    ##Check that transects are ordered by longshore distance along reference shoreline
    yes_or_no = input('Save? yes(y) or no (n)?')
    if yes_or_no == 'y':
        transects_wgs84 = utm_to_wgs84_df(transects)
        transects_wgs84.to_file(transects_path)
        print('transects save to '+ transects_path)

    ##If the order needs to be reversed, reverse them
    reverse = input('Reverse order? yes(y) or no(n)')
    if reverse == 'y':
        new_gdf = transects.reindex(index=transects.index[::-1]).reset_index(drop=True)
        new_gdf['longshore_length'] = 50*new_gdf.index
        names = [None]*len(new_gdf)
        for index, row in new_gdf.iterrows():
            name = G + C + RR + SSS + version_name  + str(row['longshore_length']).zfill(6)
            names[index] = name
        new_gdf['transect_id'] = names
        new_gdf.to_file(transects_path)
        
def main(ref_shoreline_path,
         ref_area_path,
         transects_path_final,
         G,
         C,
         RR,
         SSS,
         version_name,
         transect_spacing,
         transect_length):
    """
    Makes transects given a single reference shoreline and a single reference polygon
    inputs:
    ref_shoreline_path (str): path to the reference shoreline (geojson)
    ref_area_path (str): path to the reference polygon (geojson)
    transect_spacing (float): spacing in meters
    transect_length (float): length in meters, set this to something wider than the area
    outputs:
    transects_path (str): path to the output transects (geojson)
    """
    ref_shoreline_path_utm = wgs84_to_utm_file(ref_shoreline_path)
    ref_shoreline_path_smooth_utm = smooth_lines(ref_shoreline_path_utm, simplify=transect_spacing)
    ref_shoreline_path_shp_utm = geojson_to_shapefile(ref_shoreline_path_smooth_utm)
    transects_path_shp_utm = make_transects(ref_shoreline_path_shp_utm, transect_spacing, transect_length)
    transects_path_geojson_utm = shapefile_to_geojson(transects_path_shp_utm)
    transects_path_unclipped = utm_to_wgs84_file(transects_path_geojson_utm)
    transects_path = clip_transects(transects_path_unclipped, ref_area_path)
    transects = gpd.read_file(transects_path)
    transects['longshore_length'] = transects.index*50
    names = [None]*len(transects)
    for index, row in transects.iterrows():
        name = G+C+RR+SSS+version_name+str(row['longshore_length']).zfill(6)
        names[index] = name
    transects['G'] = [G]*len(transects)
    transects['C'] = [C]*len(transects)
    transects['RR'] = [RR]*len(transects)
    transects['SSS'] = [SSS]*len(transects)
    transects['V'] = [version_name]*len(transects)
    transects['transect_id'] = names
    transects = transects.drop(columns=['CHAINAGE'])
    transects.to_file(transects_path_final)
    files_to_keep = [transects_path_final, ref_shoreline_path, ref_area_path]
    folder = os.path.dirname(transects_path_final)
    files = os.listdir(folder)
    for file in files:
        file = os.path.join(folder, file)
        if file in files_to_keep:
            continue
        else:
            os.remove(file)
    re_index_with_ref_shoreline(transects_path_final, ref_shoreline_path, G, C, RR, SSS, version_name, tolerance=10, dist_int=30)
    return transects_path_final

def make_and_merge_transects_for_region(home, G, C, RR, version_name, transect_spacing=50, transect_length=500):
    """
    Makes transects for whole subregion and then merges them
    inputs:
    home (str): path to the region directory
    G (str): global region
    C (str): coastal area
    RR (str): subregion
    transect_spacing (float): spacing in meters
    transect_length (float): length in meters
    outputs:
    merged_transects (str): path to the merged transects geojson
    """
    subdirs = get_immediate_subdirectories(home)
    trans_gdfs = [None]*len(subdirs)
    c_str = G + C + RR
    i=0
    for SSS in subdirs:
        folder = os.path.join(home, SSS)
        input_path = os.path.join(folder, c_str+SSS[3:]+'_reference_shoreline.geojson')
        area_path = os.path.join(folder, c_str+SSS[3:]+'_reference_polygon.geojson')
        transects_path_final = os.path.join(folder, c_str+SSS[3:]+'_transects.geojson')
        transect_path = main(input_path, area_path, transects_path_final, G, C, RR, SSS[3:], version_name, transect_spacing, transect_length)
        gdf = gpd.read_file(transect_path)
        trans_gdfs[i] = gdf
        i=i+1
    merged_transects_path = os.path.join(home, G + C + RR  + '_prelim_transects.geojson')
    merged_transects = pd.concat(trans_gdfs)
    merged_transects.to_file(merged_transects_path)
    return merged_transects_path

"""
Here you need to set home to the path to the subregion you are working on
Also set G, C, RR, version_name
"""
home = """insert/path/to/subregion/folder"""
G= """G"""
C="""4"""
RR="""RR"""
version_name="""0"""

##This is the function call that will make transect files for the subregion
make_and_merge_transects_for_region(home, G, C, RR, version_name, transect_spacing=50, transect_length=700)
