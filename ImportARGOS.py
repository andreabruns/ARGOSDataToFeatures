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

# allow file overwrite
arcpy.env.overwriteOutput = True

# Set input variables (hard-wired)
inputFile = 'V:/ARGOSTracking/Data/ARGOSData/1997dg.txt'
outputSR = arcpy.SpatialReference(54002)
outputFC = "V:/ARGOSTracking/Scratch/ARGOStrack.shp"

## Prepare a new feature class to which we'll add tracking points
outPath,outName = os.path.split(outputFC)
arcpy.CreateFeatureclass_management(outPath, outName, "POINT","","","",outputSR)

# Add TagID, LC, IQ, and Date fields to the output feature class
arcpy.management.AddField(outputFC,"TagID","LONG")
arcpy.management.AddField(outputFC,"LC","TEXT")
arcpy.management.AddField(outputFC,"Date","DATE")

# Create the insert cursor
cur = arcpy.da.InsertCursor(outputFC,['Shape@','TagID','LC','Date'])

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
        
        # Extract location info from the next line
        line2String = inputFileObj.readline()
        
        # Parse the line into a list
        line2Data = line2String.split()
        
        # Extract the data we need to variables
        obsLat = line2Data[2]
        obsLon = line2Data[5]
        
        # Extract date, time, and LC vars
        obsDate = lineData[3]
        obsTime = lineData[4]
        obsLC = lineData[7]
        
        # Print results to see how we're doing
        # print(tagID, "Date:"+obsDate, "Time:"+obsTime, "LC:"+obsLC, "Lat:"+obsLat,"Long:"+obsLon)
        
        # Try t convert coordinates to point object
        try:
            # Convert raw coordinate strings to numbers
            if obsLat[-1] == 'N':
                obsLat = float(obsLat[:-1])
            else:
                obsLat = float(obsLat[:-1]) * -1
            if obsLon[-1] == 'E':
                obsLon = float(obsLon[:-1])
            else:
                obsLon = float(obsLon[:-1]) * -1
            
            # Construct a point object from the feature class
            obsPoint = arcpy.Point()
            obsPoint.X = obsLon
            obsPoint.Y = obsLat
            
            # Convert point obj to geometry obj
            inputSR = arcpy.SpatialReference(4326)
            obsPointGeom = arcpy.PointGeometry(obsPoint, inputSR)
            
            # Create a feature object
            feature = cur.insertRow((obsPointGeom,tagID,obsLC,obsDate.replace(".","/") + " " + obsTime))
        
        # handle any error
        except Exception as e:
            print(f"Error adding record {tagID} to the output: {e}")
                    
    # Move to the next line so the while loop progresses
    lineString = inputFileObj.readline()
    
# Close the file object
inputFileObj.close()

# Delete cursor
del cur