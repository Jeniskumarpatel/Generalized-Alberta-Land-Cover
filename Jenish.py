#-------------------------------------------------------------------------------
# Name:        Final_Assignment
# Purpose:
#
# Author:      jenis
#
# Created:     17/08/2023
# Copyright:   (c) jenis 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import required libraries
import os
import sys
import arcpy
from arcpy.sa import *


# Set up workspace and overwrite settings
arcpy.env.workspace = r"C:\GEOS456\Final_Assign"
arcpy.env.overwriteOutput = True


# Check if the GDB already exists and delete if necessary
print("Check The GDB")
GDB = arcpy.Exists("CypressHills.gdb")
print(GDB)



if GDB == True:
    arcpy.Delete_management(r"C:\GEOS456\Final_Assign\CypressHills.gdb")
    print ("Geodatabase delete")
    print ("")
elif GDB == False:
    print ("Geodatabase is now redy")


arcpy.CreateFileGDB_management(r"C:\GEOS456\Final_Assign", "CypressHills")
print(arcpy.GetMessages(0))
print ("")
print("")
print("")


# Create a new file geodatabase
arcpy.env.workspace = r"C:\GEOS456\Final_Assign\DEM_72E09"
Outpath = r"C:\GEOS456\Final_Assign\CypressHills.gdb"
East = (r"C:\GEOS456\Final_Assign\DEM_72E09\072e09_0201_deme.dem")
West = (r"C:\GEOS456\Final_Assign\DEM_72E09\072e09_0201_demw.dem")





# Convert DEM raster datasets East and West to raster format
DEME = arcpy.DEMToRaster_conversion(East, Outpath + "\\East")
DEMW = arcpy.DEMToRaster_conversion(West,Outpath + "\\West")

# Set up workspace and spatial reference for subsequent operations
arcpy.env.workspace = r"C:\GEOS456\Final_Assign\CypressHills.gdb"
In_Raster = ("East","West")
SR = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")





# Mosaic the East and West DEMs into a new raster named "DEM" with a specified bit depth and cell size
arcpy.MosaicToNewRaster_management(In_Raster,Outpath,"DEM",SR,"16_BIT_SIGNED","25","1")
print(arcpy.GetMessages(0))
print("")
print("")
print("")



# Clean up intermediate East and West rasters
arcpy.Delete_management("East")
arcpy.Delete_management("West")


# Enable the Spatial extension for further processing
arcpy.CheckOutExtension("Spatial")
print("Spatial extension check")


# Load the DEM raster and compute slope, then save the slope raster
DEM_Raster = arcpy.Raster("DEM")
DEMSlope = Slope(DEM_Raster)
DEMSlope.save(Outpath + "\\Slope")
print(arcpy.GetMessages(0))
print ("")
print("")
print("")


# Reclassify the slope raster into discrete categories based on value ranges and save the result
Slope_Re = Reclassify("Slope","VALUE",RemapRange([[0,4,1],[4.1,10,2],[10.1,32,3]]))
Slope_Re.save("Slope_RC")
print(arcpy.GetMessages(0))
print ("")
print("")
print("")
print("")



# Set up workspace for creating and populating the "Base_Features" feature dataset
arcpy.env.workspace = r"C:\GEOS456\Final_Assign\Base_72E09"

Base = arcpy.CreateFeatureDataset_management("C:\GEOS456\Final_Assign\CypressHills.gdb", "Base_Features",SR)



FClass = arcpy.ListFiles("*.shp")
for fc in FClass:
    arcpy.FeatureClassToGeodatabase_conversion(fc, Base)


# Set workspace to the feature dataset for further analysi
arcpy.env.workspace = r"C:\GEOS456\Final_Assign\CypressHills.gdb\Base_Features"




# Clip the "river" feature class by the "rec_park" feature class, save result as "River_final"
arcpy.Clip_analysis("river","rec_park","River_final")
print(arcpy.GetMessages(0))
print ("")
print("")
print("")
print("")

# Compute Euclidean Distance for the "River_final" feature class with a 25-unit cell size
River_B = EucDistance("River_final","","25")
River_B.save("River_EU")
print (arcpy.GetMessages(0))
print ("")
print("")
print("")
print("")


# Clip the "roads" feature class by the "rec_park" feature class, save result as "Roads_final"
arcpy.Clip_analysis("roads","rec_park","Roads_final")
print(arcpy.GetMessages(0))
print ("")
print("")
print("")

# Compute Euclidean Distance for the "Roads_final" feature class with a 25-unit cell size
Road_B = EucDistance("Roads_final","","25")
Road_B.save("Road_EU")
print (arcpy.GetMessages(0))
print ("")
print("")
print("")


# Reclassify the "River_EU" raster values into specified ranges and save the result as "River_RC"
arcpy.env.workspace = r"C:\GEOS456\Final_Assign\CypressHills.gdb"
River_Reclassify = Reclassify("River_EU", "VALUE",RemapRange([[0,50,3],[50,250,2],[250,100000,1]]))
River_Reclassify.save("River_RC")
print (arcpy.GetMessages(0))
print ("")
print("")
print("")


# Reclassify the "Road_EU" raster values into specified ranges and save the result as "Roads_RC"
Roads_Reclassify = Reclassify("Road_EU", "VALUE",RemapRange([[0,30,1],[30,250,2],[250,100000,3]]))
Roads_Reclassify.save("Roads_RC")
print(arcpy.GetMessages(0))
print ("")
print("")
print("")
print("")

# Delete the "river" and "roads" feature classes
arcpy.Delete_management("river")
arcpy.Delete_management("roads")



# Set input raster and output geodatabase paths for raster conversion
In_Raster = r"C:\GEOS456\Final_Assign\Land_Cover\landcov"
Out_Raster = r"C:\GEOS456\Final_Assign\CypressHills.gdb"
arcpy.RasterToGeodatabase_conversion(In_Raster,Out_Raster)

# Reclassify Landcover raster values using specified mapping and save the result as "Landcover_RC"
Landcov = Reclassify("landcov","VALUE",RemapValue([[1,3],[2,1],[3,1],[4,1],[5,2],[7,3]]))
Landcov.save("Landcover_RC")
print (arcpy.GetMessages(0))
print("")
print("")
print("")
print("")




arcpy.env.workspace = r"C:\GEOS456\Final_Assign\Oil_Gas"

arcpy.CreateFeatureDataset_management("C:\GEOS456\Final_Assign\CypressHills.gdb", "Pipeline",SR)

PL = "C:\GEOS456\Final_Assign\CypressHills.gdb\Pipeline"
arcpy.Select_analysis("facilities.shp", PL + "\\Start_Area", '"UFI" = \'A21605053\'')
print(arcpy.GetMessages(0))
print ("")

arcpy.Select_analysis("wells.shp", PL + "\\End_Area", '"UWID" = \'0074013407000\'')
print(arcpy.GetMessages(0))
print("")
print("")
print("")
print("")




arcpy.env.workspace = r"C:\GEOS456\Final_Assign\CypressHills.gdb"

# Define layer names for various inputs
Layer1 = "Slope_RC"
Layer2 = "Landcover_RC"
Layer3 = "River_RC"
Layer4 = "Roads_RC"
LayerM = RemapValue([[1,1],[2,2],[3,3]])





# Perform weighted overlay analysis with the specified layers and remap values
WOT = WeightedOverlay(WOTable([[Layer1,15,"Value",LayerM],[Layer2,30,"Value",LayerM],[Layer3,40,"Value",LayerM],[Layer4,15,"Value",LayerM]],[1,9,1]))
WOT.save("Weighted_overlay")
print (arcpy.GetMessages(0))
print("")
print("")
print("")

Source_point = r"C:\GEOS456\Final_Assign\CypressHills.gdb\Pipeline\Start_Area"
Dest_point = r"C:\GEOS456\Final_Assign\CypressHills.gdb\Pipeline\End_Area"


# Calculate cost backlink raster using "Weighted_overlay"
Backlink = CostBackLink(Source_point,"Weighted_overlay")
print (arcpy.GetMessages(0))
print("")
print("")


# Calculate cost backlink raster using "Weighted_overlay"
CostDist = CostDistance(Source_point,"Weighted_overlay")
print (arcpy.GetMessages(0))
print("")
print("")





Path_Vec = CostPathAsPolyline(Dest_point,CostDist,Backlink, r"C:\GEOS456\Final_Assign\CypressHills.gdb\Pipeline\Pipeline_Path")
print (arcpy.GetMessages(0))




del Backlink, CostDist

# Delete intermediate rasters and feature classes
arcpy.Delete_management("Landcover_RC")
arcpy.Delete_management("River_EU")
arcpy.Delete_management("River_RC")
arcpy.Delete_management("Road_EU")
arcpy.Delete_management("Roads_RC")
arcpy.Delete_management("Slope_RC")







# Create a feature layer from the "NTS50.shp" file
Input = arcpy.MakeFeatureLayer_management ("C:\\GEOS456\\Final_Assign\\NTS\\NTS-50\\NTS50.shp","NTS_lyr")
Source = arcpy.MakeFeatureLayer_management(r"C:\GEOS456\Final_Assign\CypressHills.gdb\Base_Features\rec_park","Park_lyr")
arcpy.SelectLayerByLocation_management(Input,"INTERSECT",Source)
print (arcpy.GetMessages(0))
print ("")
print("")
print("")






arcpy.CopyFeatures_management(Input,"NTS_50_Final")

FcList = arcpy.ListFeatureClasses()
for fc in FcList:
    fcDesc =  arcpy.Describe(fc)
    print("Spatial Reference: " + fcDesc.spatialReference.Name)
    print("Feature Class: " + fc)
    print("Geometry: " + fcDesc.ShapeType)






# List and describe feature classes in the workspace

RasterList = arcpy.ListRasters()
for raster in RasterList:
    RDesc =  arcpy.Describe(raster)
    print ("Spatial Reference: " + RDesc.spatialReference.Name)
    print ("Raster: " + raster)
    print ("Cell Size: " , RDesc.MeanCellWidth)






# List and describe feature classes in the workspace
arcpy.env.workspace = r"C:\GEOS456\Final_Assign\CypressHills.gdb\Pipeline"
FcList = arcpy.ListFeatureClasses()
for fc in FcList:
    fcDesc =  arcpy.Describe(fc)
    print("Feature Class: " + fc)
    print("Geometry: " + fcDesc.ShapeType)
    print("Spatial Reference: " + fcDesc.spatialReference.Name)







arcpy.env.workspace = r"C:\GEOS456\Final_Assign\CypressHills.gdb\Base_Features"
FcList = arcpy.ListFeatureClasses()
for fc in FcList:
    fcDesc =  arcpy.Describe(fc)
    print("Spatial Reference: " + fcDesc.spatialReference.Name)
    print("Feature Class: " + fc)
    print("Geometry: " + fcDesc.ShapeType)







arcpy.env.workspace = r"C:\GEOS456\Final_Assign\CypressHills.gdb"
in_Zone = r"C:\GEOS456\Final_Assign\CypressHills.gdb\Base_Features\rec_park"
Elevation = "DEM"

# Calculate zonal statistics for elevation
ZonalStatisticsAsTable(in_Zone,"LAYER",Elevation,"Elevation_Zonal")
print(arcpy.GetMessages(0))








# Calculate zonal statistics for slope
Slope_DEM = "Slope"
ZonalStatisticsAsTable(in_Zone,"LAYER",Slope_DEM,"Slope_Final_Zonal")
print(arcpy.GetMessages(0))







tables = arcpy.ListTables()
# Add a new field "Landcov_Type" of type TEXT to the "landcov" table
AT = "landcov"
arcpy.AddField_management(AT,"Landcov_Type","TEXT","","","20")
print(arcpy.GetMessages(0))

# Update the "Landcov_Type" field values based on specified conditions
UCursor = arcpy.da.UpdateCursor(AT, ["VALUE","Landcov_Type"])
for row in UCursor:
    if row[0] == 1:
        row[1] = "Cropland"
    elif row[0] == 2:
        row[1] = "Forage"
    elif row[0] == 3:
        row[1] = "Grasslands"
    elif row[0] == 4:
        row[1] ="Shrubs"
    elif row[0] == 5:
        row[1] = "Trees"
    elif row[0] == 7:
        row[1] = "Water"
    UCursor.updateRow(row)





# Calculate area using Tabulate Area tool and save result as "Land_Cover_Area_Final" table
TabulateArea(AT,"Landcov_Type",in_Zone,"LAYER","Land_Cover_Area_Final")
print(arcpy.GetMessages(0))



for table in tables:
    SCursor = arcpy.da.SearchCursor(table, "MEAN")
    for row in SCursor:
        if table == "Elevation_Zonal":
            print("The Average Elevation of park is" , row[0])
        elif table == "Slope_Final_Zonal":
            print("The Average Slope of Park is", row[0])
print("")
print("")
print("")
print("")






print ("")
SCursor = arcpy.da.SearchCursor("Land_Cover_Area_Final",["LANDCOV_TYPE","PROVINCIAL_PARK"])
for row in SCursor:

    print("The Area of" , row[0] , row[1])
print ("")
print("")
print("")






#selecting the feature class to access the geometry properties
fc = "C:\GEOS456\Final_Assign\CypressHills.gdb\Pipeline\Pipeline_Path"

#describe the spatial reference and units
SR = arcpy.Describe(fc).spatialReference
Unit = SR.linearUnitName

#use a search cursor to use and access the geometry area of the featureclass
SCursor = arcpy.da.SearchCursor(fc, ["SHAPE@LENGTH"])
#iterate through the feature to print the area
print ("")
for row in SCursor:
    print("Area of piple line: ", row[0], Unit)
print ("")
print("")
print("")






SCursor = arcpy.da.SearchCursor("NTS_50_Final",["OBJECTID","NAME"])



for row in SCursor:
    if row[0] == 1:
        print(row[0],":",row[1])
    if row[0] == 2:
        print(row[0],":",row[1])
print ("")
print("")
print("")
print("")







arcpy.CheckInExtension("Spatial")
print ("")
print ("Spatial extension turned off")
print ("")
print("")
print("")
print("")









import arcpy
import arcpy.mp as MAP


#MAPPING

mxdworkspace = r"C:\GEOS456\Final_Assign\GEOS456_FinalProject_Template.mxd"

output_APRX = os.path.join(r"C:\GEOS456\Final_Assign", 'GEOS456_FinalProject_Template.aprx')

arcpy.env.overwriteOutput = True

aprx = arcpy.mp.ArcGISProject(r"C:\GEOS456\Final_Assign\GEOS456_FinalProject_Template.aprx")

arcpy.env.workspace = mxdworkspace



#listing and importing files for mxd

listFiles = arcpy.ListFiles("*.mxd")

for files in listFiles:

  mxdinput = os.path.join(mxdworkspace, files)

  print (inputMXD)

  aprx.importDocument(mxdinput)

  aprx.saveACopy(output_APRX)





# List all the maps in the project and print their properties
maps = aprx.listMaps()
for maps in maps:
    print(maps.name)
    print(maps.mapType)
    print(maps.mapUnits)
    print(maps.referenceScale)

print(arcpy.GetMessages())

for fc in arcpy.ListFeatureClasses():
    print(fc)
    layers = arcpy.management.MakeFeatureLayer(fc)
    lyrFile = arcpy.management.SaveToLayerFile(layers,"C:\\Final_Assign\\" + fc + ".lyrx", True)

# List all the feature classes in the workspace and create layer files for each
##aprx = arcpy.mp.ArcGISProject("CURRENT")
arcpy.env.overwriteOutput = True

##m = aprx.listMaps("Layers")[0]
#defining workspace and aprx project

arcpy.env.workspace = r"C:\GEOS456\Final_Assign\CypressHills.gdb"

aprx = MAP.ArcGISProject(r"C:\GEOS456\Final_Assign\GEOS456_FinalProject_Template.aprx")


#listing and creating feature classes

fclist = arcpy.ListFeatureClasses()

for fc in fclist:

    layer = arcpy.management.MakeFeatureLayer(fc)

    lyrFile = arcpy.SaveToLayerFile_management(layer, r"C:\\GEOS456\\Final_Assign\\" + fc +".lyrx")

    lyrFile = MAP.LayerFile(lyrFile)


#defining map and incorporating layers

##m = aprx.listMaps("Pipeline Route") [0]
##
##arcpy.env.overwriteOutput = True
##
##LF1 = arcpy.mp.LayerFile(r"C:\GEOS456\Final_Assign\River_final.lyrx")
##
##Layer = arcpy.mp.LayerFile(LF1)
##
##m.addLayer(LF1)
##
##LF2 = arcpy.mp.LayerFile(r"C:\GEOS456\Final_Assign\Roads_final.lyrx")
##
##Layer = arcpy.mp.LayerFile(LF2)
##
##m.addLayer(LF2)
##
##LF3 = arcpy.mp.LayerFile(r"C:\GEOS456\Final_Assign\CypressHills.gdb\Pipeline\Start_Area.lyrx")
##
##Layer = arcpy.mp.LayerFile(LF3)
##
##m.addLayer(LF3)
##
##LF4 = arcpy.mp.LayerFile(r"C:\GEOS456\Final_Assign\CypressHills.gdb\Pipeline\End_Area.lyrx")
##
##Layer = arcpy.mp.LayerFile(LF4)
##
##m.addLayer(LF4)
##
##LF5 = arcpy.mp.LayerFile(r"C:\GEOS456\Final_Assign\CypressHills.gdb\Pipeline\End_Area.lyrx")
##
##Layer = arcpy.mp.LayerFile(LF5)
##
##m.addLayer(LF5)
##
##LF6 = arcpy.mp.LayerFile(r"C:\GEOS456\Final_Assign\CypressHills.gdb\Base_Features\rec_park.lyrx")
##
##Layer = arcpy.mp.LayerFile(LF6)
##
##m.addLayer(LF6)


#List the layout elements and replace with necessary information

layout = aprx.listLayouts()[0]

elements = layout.listElements()


for elem in elements:

    if elem.name == "Legend":

        elem.elementWidth = 2.5

        elem.elementHeight = 3.00

        elem.fittingStrategy = "AdjustColumnsAndFont"

        elem.elementPositionX = 14.5

        elem.elementPositionY = 8.6

    if elem.name == "Text 11":

        elem.text = "Jeniskumar Patel"

    if elem.name == "Text 12":

        elem.text = "Jay Reid"


#export layout pdf

layout.exportToPDF(r"C:\GEOS456\Final_Assign\GEOS456_FP_Patel_Jeniskumar.pdf")

print("Layout exported successfully!")






