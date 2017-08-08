'''
Yosemite Campsite Finder
Copyright 2017 github.com/mrchowmein
Script is meant to facilitate campsite searching.

'''

from bs4 import BeautifulSoup
import re
import requests
import datetime


print("Yosemite Campsite Finder will list available campsites for a 2 week range." + "\n")

campGround = {
    "Upper Pines" : "70925",
    "Lower Pines" : "70928",
    "North Pines": "70927",
    "Hodgdon Meadow" : "70929",
    "Bridalveil Creek Group and Horse Camp" : "70931",
    "Crane Flat" : "70930",
    "Tuolumne Meadows" : "70926",
    "Wawona" : "70924"
}

campGroundString = ""

for key in campGround:
    campGroundString += key + ", "

date = input("Enter start date (MM/DD/YYYY): ")
print("Available Campgrounds: "+ campGroundString[:-2])

#check if user entered campground exist
r = "incorrect"
while r == "incorrect":
    campselect = input("Enter campground name: ")
    r = campGround.get(campselect.title(), "incorrect" )
    if r == "incorrect":
        print("\n" + "Error: Incorrect Name")


prefix = "https://www.recreation.gov/campsiteCalendar.do?page=matrix&calarvdate="
post = "&contractCode=NRSO&parkId="
url = prefix + date + post + campGround[campselect.title()]
page  = requests.get(url)

#prints url to book site
print("\n" + "Booking URL: " + url)

soup = BeautifulSoup(page.content, 'html.parser')

#add siteID to dict
siteDict = {}
siteData =  soup.find_all('td', class_="sn")
siteData = map(str, siteData)

for entry in siteData:
    siteID = re.search("siteId=(.+?)&amp", entry).group(1)
    siteNumber = re.search("title=\"(.+?)\"", entry).group(1)
    siteDict[siteID] = siteNumber

#available sites
availData =  soup.find_all('td', class_="status a")
availDataSat =  soup.find_all('td', class_="status a sat")
availDataSun =  soup.find_all('td', class_="status a sun")

availData = availData + availDataSat + availDataSun

print("Available Sites: " + str(len(availData)))
availData = map(str, availData)



#saves query sites and dates to list
querylist = []

for entry in availData:
    siteID = re.search("siteId=(.+?)&amp", entry).group(1)
    dateAvail = re.search("arvdate=(.+?)&amp", entry).group(1)
    dateAvail = datetime.datetime.strptime(dateAvail, '%m/%d/%Y').strftime('%m/%d/%Y')
    siteNumber = siteDict[siteID]
    querylist.append("Site# " + siteNumber + " Date Available: " + dateAvail)

#print available sites and dates
querylist.sort()
for element in querylist:
    print(element)
