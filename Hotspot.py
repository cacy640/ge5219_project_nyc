# NOTE #
# Hotspot.py is to define the function to calculate the hotspots of traffic accident in New York City#
# Requires ArcPy license #
# This .py file is embedded in main.py #

# import system modules
import arcpy
from arcpy import env
from arcpy.sa import *
import os

def Hotspotall(filename, mask, in_path, output_path, m, aprx):
    """
    This is a function to conduct Hotspot Analysis.

    :param filename: The file name of the data that is employed in Hotspot Analysis.
    :param mask: The mask feature to clip the output raster.
    :param in_path: The path of data used.
    :param output_path: The path to save the result.
    :param m: The map layer in aprx file.
    :param aprx: The path of the aprx file used in this analysis.
    :return: A jpg image that shows the Hotspot Analysis result.
    """

    # Hot spot analysis
    # Description: Calculates the crash events places with identifying statistically significant hot spots and cold spots
    arcpy.HotSpots_stats("Crash_all_Prj", "injured_killed", "Crash_all_HotSpots",
                         "INVERSE_DISTANCE", "EUCLIDEAN_DISTANCE",
                         "NONE")


    print("Hot spot analysis successful")

    mask_feature = mask
    lyr_all = os.path.join(in_path, "Crash_all_HotSpots")

    m.addDataFromPath(mask_feature)
    m.addDataFromPath(lyr_all)
    for lyr in m.listLayers():
        if lyr.name == "World Topographic Map" or lyr.name == "World Hillshade":
            m.removeLayer(lyr)
    lyt = aprx.listLayouts("Layout*")[0]
    lyt.exportToJPEG(os.path.join(output_path, "hotspotall.jpg"))


def Hotspotday(filename, mask, in_path, output_path, m, aprx):

    # Hot spot analysis
    # Description: Calculates the crash events places with identifying statistically significant hot spots and cold spots
    arcpy.HotSpots_stats("Crash_day_Prj", "injured_killed", "Crash_day_HotSpots",
                         "INVERSE_DISTANCE", "EUCLIDEAN_DISTANCE",
                         "NONE")

    print("Hot spot analysis successful")

    mask_feature = mask
    lyr_day = os.path.join(in_path, "Crash_day_HotSpots")

    m.addDataFromPath(mask_feature)
    m.addDataFromPath(lyr_day)
    for lyr in m.listLayers():
        if lyr.name == "World Topographic Map" or lyr.name == "World Hillshade":
            m.removeLayer(lyr)
    lyt = aprx.listLayouts("Layout*")[0]
    lyt.exportToJPEG(os.path.join(output_path, "hotspotday.jpg"))


def Hotspotnight(filename, mask, in_path, output_path, m, aprx):

    # Hot spot analysis
    # Description: Calculates the crash events places with identifying statistically significant hot spots and cold spots
    arcpy.HotSpots_stats("Crash_night_Prj", "injured_killed", "Crash_night_HotSpots",
                         "INVERSE_DISTANCE", "EUCLIDEAN_DISTANCE",
                         "NONE")

    print("Hot spot analysis successful")

    mask_feature = mask
    lyr_night = os.path.join(in_path, "Crash_night_HotSpots")

    m.addDataFromPath(mask_feature)
    m.addDataFromPath(lyr_night)
    for lyr in m.listLayers():
        if lyr.name == "World Topographic Map" or lyr.name == "World Hillshade":
            m.removeLayer(lyr)
    lyt = aprx.listLayouts("Layout*")[0]
    lyt.exportToJPEG(os.path.join(output_path, "hotspotnight.jpg"))


def Hotspotweekday(filename, mask, in_path, output_path, m, aprx):
    # Hot spot analysis
    # Description: Calculates the crash events places with identifying statistically significant hot spots and cold spots
    arcpy.HotSpots_stats("Crash_weekday_Prj", "injured_killed", "Crash_weekday_HotSpots",
                         "INVERSE_DISTANCE", "EUCLIDEAN_DISTANCE",
                         "NONE")

    print("Hot spot analysis successful")

    mask_feature = mask
    lyr_weekday = os.path.join(in_path, "Crash_weekday_HotSpots")

    m.addDataFromPath(mask_feature)
    m.addDataFromPath(lyr_weekday)
    for lyr in m.listLayers():
        if lyr.name == "World Topographic Map" or lyr.name == "World Hillshade":
            m.removeLayer(lyr)
    lyt = aprx.listLayouts("Layout*")[0]
    lyt.exportToJPEG(os.path.join(output_path, "hotspotweekday.jpg"))


def Hotspotweekend(filename, mask, in_path, output_path, m, aprx):
    # Hot spot analysis
    # Description: Calculates the crash events places with identifying statistically significant hot spots and cold spots
    arcpy.HotSpots_stats("Crash_weekend_Prj", "injured_killed", "Crash_weekend_HotSpots",
                         "INVERSE_DISTANCE", "EUCLIDEAN_DISTANCE",
                         "NONE")

    print("Hot spot analysis successful")

    mask_feature = mask
    lyr_weekend = os.path.join(in_path, "Crash_weekend_HotSpots")

    m.addDataFromPath(mask_feature)
    m.addDataFromPath(lyr_weekend)
    for lyr in m.listLayers():
        if lyr.name == "World Topographic Map" or lyr.name == "World Hillshade":
            m.removeLayer(lyr)
    lyt = aprx.listLayouts("Layout*")[0]
    lyt.exportToJPEG(os.path.join(output_path, "hotspotweekend.jpg"))


#if __name__ == "__main__":
#    arcpy.env.workspace = r"C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\database\final.gdb"
#    arcpy.env.extent = r"C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\code\Community Districts\geo_export_0138f613-3d60-48ca-9db5-74265a2e0afb.shp"
#    aprx = arcpy.mp.ArcGISProject(r"C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\database\database.aprx")
#    lyt = aprx.listLayouts("Layout*")[0]
#    m = aprx.listMaps("Map")[0]

