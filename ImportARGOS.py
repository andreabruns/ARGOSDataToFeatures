##---------------------------------------------------------------------
## ImportARGOS.py
##
## Description: Read in ARGOS formatted tracking data and create a line
##    feature class from the [filtered] tracking points
##
## Usage: ImportArgos <ARGOS folder> <Output feature class> 
##
## Created: Fall 2018
## Author: John.Fay@duke.edu (for ENV859)
##---------------------------------------------------------------------

# Import modules
import sys, os, arcpy

# Set input variables (hard-wired)
inputFile = 'V:/ARGOSTracking/Data/ARGOSData/1997dg.txt'

# Set coordinate sys
outputSR = arcpy.SpatialReference(54002)
outputFC = "V:/ARGOSTracking/Scratch/ARGOStrack.shp"

# allow file overwrite
arcpy.env.overwriteOutput = True

## Prepare a new feature class to which we'll add tracking points
# Create an empty feature class; requires the path and name as searate parameters
outPath,outName = os.path.split(outputFC)
arcpy.CreateFeatureclass_management(outPath, outName, "POINT","","",outputSR)


#%% Construct a while loop to iterate through all lines in the datafile
# Open the ARGOS data file for reading
inputFileObj = open(inputFile, 'r')

# Get the first line of data so we can use a while loop
lineString = inputFileObj.readline()

# Start the while loop
while lineString:
    
    # Set code to run only if the line contains the string "Date: "
    if ("Date :" in lineString):
        
        # Parse the line into a list
        lineData = lineString.split()
        
        # Extract attributes from the datum header line
        tagID = lineData[0]
        obsDate = lineData[3]
        obsTime = lineData[4]
        obsLC = lineData[7]
        
        # Extract location info from the next line
        line2String = inputFileObj.readline()
        
        # Parse the line into a list
        line2Data = line2String.split()
        
        # Extract the ate we need to variables
        obsLat = line2Data[2]
        obsLon = line2Data[5]
        
        # Print results to see how we're doing
        print(tagID, "Date:"+obsDate, "Time:"+obsTime, "LC:"+obsLC, "Lat:"+obsLat,"Long:"+obsLon)
        
    # Move to the next line so the while loop progresses
    lineString = inputFileObj.readline()
    
# Close the file object
inputFileObj.close()