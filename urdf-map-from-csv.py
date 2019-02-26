#!/usr/bin/env python

# Authors: Juan G Victores
# CopyPolicy: released under the terms of the LGPLv2.1
# URL: https://github.com/roboticslab-uc3m/gazebo-tools

from lxml import etree

#-- User variables
boxHeight = 1.0
inFileStr = 'assets/map1.csv'

resolution = 1.0  # Just to make similar to MATLAB [pixel/meter]
meterPerPixel = 1 / resolution  # [meter/pixel]

#-- Program
from numpy import genfromtxt
inFile = genfromtxt(inFileStr, delimiter=',')
print inFile

nX = inFile.shape[0]
nY = inFile.shape[1]
print "lines = X =",inFile.shape[0]
print "columns = Y =",inFile.shape[1]

#-- Default to X=rows,Y=columns. Uncomment the next 3 lines to transpose.
# print "transposing"
# from numpy import transpose
# inFile = transpose(inFile)

Ez = boxHeight  # Box size is actually double the extent

Ex = meterPerPixel
Ey = meterPerPixel

robot = etree.Element("robot", name="yetAnotherRobot")

#-- Create Floor
floorEx = Ex * nX
floorEy = Ey * nY
floorEz = boxHeight / 8.0  # arbitrary

link = etree.SubElement(robot, "link", name="floor")
visual = etree.SubElement(link, "visual")
visual_origin = etree.SubElement(visual, "origin", xyz=str(floorEx/2.0)+" "+ str(floorEy/2.0)+" "+str(-floorEz/2.0))
visual_geometry = etree.SubElement(visual, "geometry")
visual_box = etree.SubElement(visual_geometry, "box", size=str(floorEx)+" "+ str(floorEy)+" "+str(floorEz))
collision = etree.SubElement(link, "collision")
collision_origin = etree.SubElement(collision, "origin", xyz=str(floorEx/2.0)+" "+ str(floorEy/2.0)+" "+str(-floorEz/2.0))
collision_geometry = etree.SubElement(collision, "geometry")
collision_box = etree.SubElement(collision_geometry, "box", size=str(floorEx)+" "+ str(floorEy)+" "+str(floorEz))

#-- Create Walls
for iX in range(nX):
    #print "iX:",iX
    for iY in range(nY):
        #print "* iY:",iY

        #-- Skip box if map indicates a 0
        if inFile[iX][iY] == 0:
            continue

        #-- Add E___ to each to force begin at 0,0,0 (centered by default)
        x = Ex/2.0 + iX*meterPerPixel
        y = Ey/2.0 + iY*meterPerPixel
        z = Ez/2.0 # Ez # Add this to raise to floor level (centered by default)

        #-- Create box
        link = etree.SubElement(robot, "link", name="box_"+str(iX)+"_"+str(iY))
        visual = etree.SubElement(link, "visual")
        visual_origin = etree.SubElement(visual, "origin", xyz=str(x)+" "+ str(y)+" "+str(z))
        visual_geometry = etree.SubElement(visual, "geometry")
        visual_box = etree.SubElement(visual_geometry, "box", size=str(Ex)+" "+ str(Ey)+" "+str(Ez))
        collision = etree.SubElement(link, "collision")
        collision_origin = etree.SubElement(collision, "origin", xyz=str(x)+" "+ str(y)+" "+str(z))
        collision_geometry = etree.SubElement(collision, "geometry")
        collision_box = etree.SubElement(collision_geometry, "box", size=str(Ex)+" "+ str(Ey)+" "+str(Ez))

myStr = etree.tostring(robot, pretty_print=True)

outFile = open('map.urdf', 'w')
outFile.write(myStr)
outFile.close()
