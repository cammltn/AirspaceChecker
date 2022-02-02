# Camille Milton
# Geog 666
# 11 June 2021


# Import Python Modules

import os
from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import pandas as pd
from datetime import date
import zipfile
import arcpy



# Create web scraper for FAA data

url = 'https://www.faa.gov/air_traffic/flight_info/aeronav/Aero_Data/NASR_Subscription/'
base_url = 'https://www.faa.gov/air_traffic/flight_info/aeronav/Aero_Data/'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
page_html = uReq(req).read().decode('utf-8', 'ignore')
page_soup = soup(page_html, "html.parser")
link = page_soup.findAll("article",{"class","content"})[0].findAll('ul')[1].li.a['href'].replace("./../","")
Current = base_url + link
req1 = Request(Current, headers={'User-Agent': 'Mozilla/5.0'})
page_html1 = uReq(req1).read().decode('utf-8', 'ignore')
page_soup1 = soup(page_html1, "html.parser")
zip_link = page_soup1.findAll("article",{"class","content"})[0].findAll('ul')[2].li.a['href']
r = requests.get(zip_link) # create HTTP response object
with open('C:\Users\milto\Desktop\Lab1/ipg100105.zip','wb') as f:
    f.write(r.content)



###############################
# Unzip downloaded file

with zipfile.ZipFile('C:\Users\milto\Desktop\Lab1/ipg100105.zip' , 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)

###############################
# Open extracted file using arcpy

# Allow files to be overwritten
arcpy.env.overwriteOutput = True

# Set workspace
arcpy.env.workspace = r 'C:\Users\milto\Desktop\Lab1' 

###############################



# File path of shapefiles

Class_Airspace = "C:\Users\milto\Desktop\Lab1/ipg100105\Additional_Data\Shape_Files\Class_Airspace.shp"
locations_shp = "C:\Users\milto\Desktop\Lab1/ipg100105\Additional_Data\Shape_Files\Locations.shp"

# Create feature layer 
arcpy.MakeFeatureLayer_management(Class_Airspace, "Class_Airspace", "LOWER_VAL = '0'") # Surface layer zones

arcpy.MakeFeatureLayer_management(Class_Airspace, "locations_lyrs") # Make locations layer

# Layer geometries
airspaces = []
with arcpy.da.UpdateCursor("locations_lyr", ["SHAPE@". "Aircheck"]) as cursor:
    for row in cursor:
        Class_Airspace.append(row[0])

# Identify areas with clearance for drones (above 400ft)
with arcpy.da.UpdateCursor("locations_lyr", ["SHAPE@", "Aircheck"]) as cursor:
    for row in cursor:
        row[1] = 'Pass'
        for airspace in airspaces:
            if row[0].within(airspace):
                row[1] = 'Fail'
                cursor.updateRow(row)



###############################

# Create CSV
arcpy.TableToTable_conversion("locations_lyr", "C:\Users\milto\Desktop\Lab1", +"ClassAirspace.csv"

