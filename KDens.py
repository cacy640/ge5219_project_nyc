# NOTE #
# KDens.py is to define the function to calculate the Kernel Density Estimation of traffic accident in New York City#
# Requires ArcPy license #
# This .py file is embedded in main.py #

# import system modules
import arcpy
from arcpy import env
from arcpy.sa import *
import os

# Set environment settings
#arcpy.env.workspace = r"C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\database\final.gdb"
#arcpy.env.extent = r"C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\code\Community Districts\geo_export_0138f613-3d60-48ca-9db5-74265a2e0afb.shp"
#aprx = arcpy.mp.ArcGISProject(r"C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\database\database.aprx")
#lyt = aprx.listLayouts("Layout*")[0]
#m = aprx.listMaps("Map")[0]


def KDensall(filename, mask, in_path, output_path, m, aprx):
    """
    This is a function to calculate the Kernel Density Estimation.

    :param filename: The file name of the data that is employed in Kernel Density Estimation (KDE) analysis.
    :param mask: The mask feature to clip the output raster.
    :param in_path: The path of data used.
    :param output_path: The path to save the result.
    :param m: The map layer in aprx file.
    :param aprx: The path of the aprx file used in this analysis.
    :return: A jpg image that shows the Kernel Density Estimation.
    """

    # KernelDensity
    # Description: Calculates the crash events concentration pattern
    outKDens_all = arcpy.sa.KernelDensity("Crash_all_Prj", "NONE")
    outKDens_all.save("KD_all_out")
    # return output_feature_class
    print("Kernel Density Estimation successful")

    mask_feature = mask
    lyr_all = os.path.join(in_path, "KD_all_out")

    m.addDataFromPath(mask_feature)
    m.addDataFromPath(lyr_all)
    for lyr in m.listLayers():
        if lyr.name == "World Topographic Map" or lyr.name == "World Hillshade":
            m.removeLayer(lyr)
    lyt = aprx.listLayouts("Layout*")[0]
    lyt.exportToJPEG(os.path.join(output_path, "all.jpg"))


def KDensday(filename, mask, in_path, output_path, m, aprx):

    # KernelDensity
    # Description: Calculates the crash events concentration pattern
    outKDens_day = arcpy.sa.KernelDensity("Crash_day_Prj", "NONE")
    outKDens_day.save("KD_day_out")
    # return output_feature_class
    print("Kernel Density Estimation successful")

    mask_feature = mask
    lyr_day = os.path.join(in_path, "KD_day_out")

    m.addDataFromPath(mask_feature)
    m.addDataFromPath(lyr_day)
    for lyr in m.listLayers():
        if lyr.name == "World Topographic Map" or lyr.name == "World Hillshade":
            m.removeLayer(lyr)
    lyt = aprx.listLayouts("Layout*")[0]
    lyt.exportToJPEG(os.path.join(output_path, "day.jpg"))


def KDensnight(filename, mask, in_path, output_path, m, aprx):

    # KernelDensity
    # Description: Calculates the crash events concentration pattern
    outKDens_night = arcpy.sa.KernelDensity("Crash_night_Prj", "NONE")
    outKDens_night.save("KD_night_out")
    # return output_feature_class
    print("Kernel Density Estimation successful")

    mask_feature = mask
    lyr_night = os.path.join(in_path, "KD_night_out")

    m.addDataFromPath(mask_feature)
    m.addDataFromPath(lyr_night)
    for lyr in m.listLayers():
        if lyr.name == "World Topographic Map" or lyr.name == "World Hillshade":
            m.removeLayer(lyr)
    lyt = aprx.listLayouts("Layout*")[0]
    lyt.exportToJPEG(os.path.join(output_path, "night.jpg"))


def KDensweekday(filename, mask, in_path, output_path, m, aprx):

    # KernelDensity
    # Description: Calculates the crash events concentration pattern
    outKDens_weekday = arcpy.sa.KernelDensity("Crash_weekday_Prj", "NONE")
    outKDens_weekday.save("KD_weekday_out")
    # return output_feature_class
    print("Kernel Density Estimation successful")

    mask_feature = mask
    lyr_weekday = os.path.join(in_path, "KD_weekday_out")

    m.addDataFromPath(mask_feature)
    m.addDataFromPath(lyr_weekday)
    for lyr in m.listLayers():
        if lyr.name == "World Topographic Map" or lyr.name == "World Hillshade":
            m.removeLayer(lyr)
    lyt = aprx.listLayouts("Layout*")[0]
    lyt.exportToJPEG(os.path.join(output_path, "weekday.jpg"))


def KDensweekend(filename, mask, in_path, output_path, m, aprx):

    # KernelDensity
    # Description: Calculates the crash events concentration pattern
    outKDens_weekend = arcpy.sa.KernelDensity("Crash_weekend_Prj", "NONE")
    outKDens_weekend.save("KD_weekend_out")
    # return output_feature_class
    print("Kernel Density Estimation successful")

    mask_feature = mask
    lyr_weekend = os.path.join(in_path, "KD_weekend_out")

    m.addDataFromPath(mask_feature)
    m.addDataFromPath(lyr_weekend)
    for lyr in m.listLayers():
        if lyr.name == "World Topographic Map" or lyr.name == "World Hillshade":
            m.removeLayer(lyr)
    lyt = aprx.listLayouts("Layout*")[0]
    lyt.exportToJPEG(os.path.join(output_path, "weekend.jpg"))


# XYTableToPoint.py
# Description: Creates a point feature class from input table
# Make the XY event layer

#if __name__ == "__main__":
 #   arcpy.env.workspace = r"C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\database\final.gdb"
  #  arcpy.env.extent = r"C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\code\Community Districts\geo_export_0138f613-3d60-48ca-9db5-74265a2e0afb.shp"
   # aprx = arcpy.mp.ArcGISProject(r"C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\database\database.aprx")
    #lyt = aprx.listLayouts("Layout*")[0]
    #m = aprx.listMaps("Map")[0]

    #filename = r"D:\nus\GE5219\prj\Final_Prj\data\crash_weekend.csv"
    #in_path = arcpy.env.workspace
    #output_path = r"C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\code\new"
    #mask = r"C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\code\Community Districts\geo_export_0138f613-3d60-48ca-9db5-74265a2e0afb.shp"
    #KDensweekend(filename, mask, in_path, output_path, m, aprx)
