#Converts .tsv information to aerial photo index
# -*- coding: cp1252 -*-

import os
import sys

#SET INPUT AND OUTPUT FILES
inFile=open(input('Input location of the master spreadsheet (.tsv) and hit enter: ')) #Name of file located in the directory of this script that stores the information
#Note that the file entered must be a .csv for this script to work
outfn='index.html' #Desired name of output file
if os.path.exists(outfn): #Check if file exists
    print 'It appears that '+ outfn +' already exists!' 
    os.remove(outfn) #Remove the file if it exists
    print outfn +' has now been removed!'
else:
    print outfn +' does not already exist!' #This will be written if the file does not exist
outFile=open(outfn, 'w') #Create a new output File (.html)

#READ TSV FILE
allcontent=inFile.readlines() #Read csv and group contents line by line
content=allcontent[3:] #Remove the first line from the content as it does not provide useful information

#GATHER UNIQUE YEARS FROM inFile
years=[] #Create an empty array where years from the spreadsheet (.csv, inFile) will be stored
for line in content:
    item=line.split('\t') #split lines of inFile into 'item' at each comma (,)
    year=item[4]
    year=year[:4]
    years.append(year) #add the first column [0] to the empty array named years
uniqueYears=sorted(set(years)) #Get unique years, and sort them numerically

#HEADER SECTION
head='<html> \n <head> \n <title>McMaster Aerial Photographic Index</title> \n <meta charset="utf-8" /> \n <meta name="viewport" content="width=device-width, initial-scale=1.0"> \n <link rel="stylesheet" href="http://leafletjs.com/dist/leaflet.css" /> \n <link rel="stylesheet" type="text/css" href="css/own_style.css">\n<script src="http://code.jquery.com/jquery-1.11.1.min.js"></script>\n<script src="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js"></script>\n <script src="js/Autolinker.min.js"></script>\n</head> \n \n'
outFile.write(head) #write the html header to the outFile

#ORTHO AERIAL IMAGES YEARS
from datetime import date #get the date so that we can check entries up to today's date
inF=open('data\exp_AirOrthoAttributeGraph.js') #information from shapefile ALWAYS stored in data folder. If the name changes of the file, PLEASE change it here from exp_AirOrthoAttributeGraph.js to the new name!
contents=inF.readlines() #read all lines within the file
line=contents[5] #read the first line with content
item=line.split(',') #split line into sub-sections at each comma
orthoYears=[] #empty array that the years will be appended to
for i in xrange (3, len(item)): #iterates through the different sub segments starting at number three
    yr=item[i] 
    integer=yr[2:6]
    if integer=="geom": #it is known that 'geom' follows the last attribute table entry for the shapefile, therefore when this is read we have gone through all the years. This value was found by looking at the inFile (in this case exp_AirOrthoAttributeGraph.js)
        break #finish interating if the condition in the line above is met
    integer=int(integer)
    for x in xrange (1999, date.today().year+1):
        if x==integer:
            orthoYears.append(integer) #add the year to the array if it is equal to a year in the range in the for loop

#BODY HTML (ADDING THE MAP)
htmlbody='<body> \n <div id="map" style="width: 90%; height: 90%"></div> \n \n' #width and height can be changed to desired percentage of the frame/browser
outFile.write(htmlbody) #write the body html to the outFile
    #ADD TIMESLIDER TO BODY
leng=len(uniqueYears) -1
timeslider=' <fieldset> \n <legend>Time Slider</legend> \n <label for=year>'+str(uniqueYears[0])+'</label> \n<input type="range" min="'+str(uniqueYears[0])+'" max="'+str(orthoYears[-1])+'" value="'+str(uniqueYears[0])+'" id="year" step="1" list="hamyear" onchange="showValue(this.value); layer(this.value)" style="width: 75%;"> \n<datalist id=hamyear> \n'
outFile.write(timeslider)
for x in xrange(0, len(uniqueYears)): 
    option='<option>'+str(uniqueYears[x]) +'</option> \n' #add each year in spreadsheet between their own timeslide <option> tags
    outFile.write(option)
for x in xrange (0, len(orthoYears)):
    option='<option>'+str(orthoYears[x]) +'</option> \n' #add each year in spreadsheet between their own timeslide <option> tags
    outFile.write(option)
timesliderclose='</datalist> \n <label for=year>'+str(orthoYears[-1])+'</label> <strong>Selected Year:</strong> <span id="range">'+str(uniqueYears[0])+'</span> \n </fieldset>\n</body>\n'
outFile.write(timesliderclose) #Write end html of timeslider to outFile

#BEGIN SCRIPTS
scripts='<script src="data/exp_AirOrthoAttributeGraph.js"></script> \n <script> \n \n'
outFile.write(scripts) #write html to draw scripts

#CREATE MARKERS FROM SPREADSHEET
#WRITING DIFFERENT MARKER COLOURS
markercolours=['blue', 'orange', 'green', 'purple', 'yellow', 'red', 'pink', 'gray', 'maroon', 'brown', 'lightblue', 'lightgreen'] #Note that all of these colours correspond to an image of the marker hosted on our MDG wordpress blog
shadowURL='\'http://en.unesco.org/sites/all/libraries/leaflet/images/marker-shadow.png\''
for colour in markercolours:
    markerURL='\'https://mdgmcmaster.files.wordpress.com/2015/05/'+str(colour)+'.png?w=25\''
    varIcon='var '+str(colour)+'Icon=L.icon({iconUrl: '+str(markerURL)+', shadowUrl: '+str(shadowURL)+', iconAnchor: [12.5,41], popupAnchor: [0,-40]});\n \n'
    outFile.write(varIcon) #creates an icon associated with each colour from the markercolours array and writes it to the outFile
markercolours=['blue', 'orange', 'green', 'purple', 'yellow', 'red', 'pink', 'gray', 'maroon', 'brown', 'lightblue', 'lightgreen', 'blue', 'orange', 'green', 'purple', 'yellow', 'red', 'pink', 'gray', 'maroon', 'brown', 'lightblue', 'lightgreen', 'blue', 'orange', 'green', 'purple', 'yellow', 'red', 'pink', 'gray', 'maroon', 'brown', 'lightblue', 'lightgreen', 'blue', 'orange', 'green', 'purple', 'yellow', 'red',  'pink', 'gray', 'maroon', 'brown', 'lightblue', 'lightgreen']
flightLine=[] #Create an empty array where all flight lines of the same year will be stored
yearlayers=[] #Create an empty array where all the different year layer groups will be mentioned
yfl=[]
for x in xrange(0, len(uniqueYears)): #iterates through each year
    z=1 #numbers each different markers for labeling their variable name in the javascript of outFile
    markerarray=[] #Create empty array for all markers of the same year
    yflightline=[]
    for line in content:
        item=line.split('\t') #similar to above, split each line into items at each comma
        year=item[4] #year is in the first column
        year=year[:4]
        flightline=item[1] #flightline is in the second column
        if uniqueYears[x]==year: #if the year is equal to the first value in the cell (year) then append the flightline in the column beside it to the flightLine array
            flightLine.append(item[5]) 
        flightLine=sorted(set(flightLine)) #sort the flightlines for the year
    for line in content:
        item=line.split('\t')
        year=item[4] #Here we define each colum as a different variable for use in the marker
        year=year[:4]
        ID=item[2]
        flightline=item[5]
        photo=item[6]
        scale=item[7]
        latitude=item[8]
        longitude=item[9]
        img=item[10]
        imglink=item[11]
        flightline=flightline.translate(None,"-")
        flightline=flightline.translate(None,"?")
        flightline=flightline.translate(None,"/")
        photo=photo.translate(None," ")
        photo=photo.translate(None,"[")
        photo=photo.translate(None,"]")
        if img=="":
            imgsrc="" #If there is no value in the image column (img="") then don't do anything
        else:
            imgsrc='<a href="'+str(imglink)+'" target="_blank"><img src="'+str(img)+'" height="200" width="200"></a> <br>' #If image field is not empty then add the image
        if uniqueYears[x]==year:
            yfl.append(flightline)
    yfl=sorted(set(yfl))
    for line in content:
        item=line.split('\t')
        for z in xrange (0, len(item)-1):
            interest=item[z]
            if interest.startswith('"') and interest.endswith('"'):
                item[z]=interest[1:-1]
        year=item[4] #Here we define each colum as a different variable for use in the marker
        year=year[:4]
        ID=item[3]
        flightline=item[5]
        photo=item[6]
        scale=item[7]
        latitude=item[8]
        longitude=item[9]
        img=item[10]
        dArchive=item[11]
        flightline=flightline.translate(None,"-")
        photo=photo.translate(None," ")
        photo=photo.translate(None,"[")
        photo=photo.translate(None,"]")
        photo=photo.translate(None,"/")
        flightline=flightline.translate(None,"/")
        flightline=flightline.translate(None,"\'")
        if dArchive!="":
            dalink='<a href="'+str(dArchive)+'" target="_blank">View Metadata in the Digital Archive</a>'
        else:
            dalink=""
        if img=="":
            imgsrc="" #If there is no value in the image column (img="") then don't do anything
        else:
            imgsrc='<a href="'+str(dArchive)+'" target="_blank"><img src="'+str(img)+'" height="200" width="200"></a> <br>' #If image field is not empty then add the image
    
        for y in xrange (0, len(yfl)):
            if flightline==yfl[y] and uniqueYears[x]==year:
                markers='var '+str(ID)+str(uniqueYears[x])+str(flightline)+str(photo)+'=L.marker(['+str(latitude)+','+str(longitude)+'], {icon: '+str(markercolours[y])+'Icon}).bindPopup(\''+str(imgsrc)+' <strong>Flight Line</strong> '+str(flightline)+'<br> <strong>Photo</strong> '+str(photo)+'<br> <strong>Scale</strong> '+str(scale)+'<br> '+str(dalink)+'\'); \n'
                outFile.write(markers)
                #1919 photo # have a space and off chaarcters that don't work well with javascript
                markerarray.append(str(str(ID)+uniqueYears[x])+str(flightline)+str(photo)) #write name of the marker above to the marker array
            markerarray=sorted(set(markerarray)) #sort the marker array
            markerarrayNQ=str(markerarray).translate(None,"'") #remove quotations from the marker array so that it can be read in javascript (ex. ['a', 'b'] becomes [a, b]
            layerGroup='var Hamilton'+str(uniqueYears[x])+'=L.layerGroup('+str(markerarrayNQ)+'); \n \n' #group all markers by year in a layer group read by javascript 
            if flightline==yfl[y] and uniqueYears[x]==year:     
                yearlayers.append('Hamilton'+str(uniqueYears[x])) #adding each layerGroup created (from each year) to the massive array of all layers (yearlayers)
    outFile.write(layerGroup)
    yfl=[]

yearlayers=sorted(set(yearlayers))
#ADD BASEMAPS
Basemaps='var grayscale   = L.tileLayer(\'https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png\', {id: \'examples.map-20v6611k\', attribution: \'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, \' +\'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, \' +\'Imagery © <a href="http://mapbox.com">Mapbox</a>\'}), \n OSMbase = L.tileLayer(\'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png\', {attribution: \'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, \' +\'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>\'}), \n streets  = L.tileLayer(\'https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png\', {id: \'examples.map-i875mjb7\',   attribution: \'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, \' +\'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, \' +\'Imagery © <a href="http://mapbox.com">Mapbox</a>\'}); \n \n'
outFile.write(Basemaps) #write java for basemaps to outFile

#CREATE MAP
Lmap='var map=L.map(\'map\', {center:[43.26,-79.89],zoom: 11,layers:[OSMbase,'+str(yearlayers[0])+']}); \n' #str() says that the lowest year will be turned on when the map starts up
outFile.write(Lmap) #write map to outFile
yearlayerz=str(yearlayers).translate(None,"'") #remove single quotations from all years in array yearlayers
outFile.write('var Years=L.layerGroup('+str(yearlayerz)+'); \n') #create a layer group containing all years as read by the java

#ADD ORTHOPHOTO FUNCTIONS
inF=open('data\exp_AirOrthoAttributeGraph.js') #information from shapefile ALWAYS stored in data folder. If the name changes of the file, PLEASE change it here from exp_AirOrthoAttributeGraph.js to the new name!
contents=inF.readlines() #read all lines within the file
line=contents[5] #read the first line with content
item=line.split(',') #split line into sub-sections at each comma

line=line.translate(None,",")
line=line.translate(None,"{")
line=line.translate(None,"}")
line=line.translate(None,'"')
line=line.translate(None,':')
item=line.split(' ')
orthoFunc='function pop_ORTHOTILES(feature, layer) {var popupContent = '
outFile.write(orthoFunc)
for n in xrange (7, len(item),2):
    ditem=item[n]
    if ditem=="":
        break
    else:
        if n!=7:
            outFile.write(' + ')
        field='\'<br><strong>'+str(ditem)+': </strong>\' + Autolinker.link(String(feature.properties[\''+str(ditem)+'\']))'
        outFile.write(field)
finish=';layer.bindPopup(popupContent);}\nfunction doStyleORTHOTILES(feature) {return {color: \'#000000\',fillColor: \'#b6b6b6\',weight: 1,dashArray: \'\',opacity: 0.35,fillOpacity: 0.35};} \nvar orthoAerial= new L.geoJson(exp_AirOrthoAttributeGraph,{onEachFeature: pop_ORTHOTILES,style: doStyleORTHOTILES});\n\n'
outFile.write(finish)
    
##orthoFunc='function pop_ORTHOTILES(feature, layer) {var popupContent = \'<strong>Image Name: </strong>\' + Autolinker.link(String(feature.properties[\'IMAGE_NAME\'])) + \'<br><strong>Available Years</strong><br><strong>1999: </strong>\' + Autolinker.link(String(feature.properties[\'YEAR_1999\'])) + \'<br><strong>2002: </strong>\' + Autolinker.link(String(feature.properties[\'YEAR_2002\'])) + \'<br><strong>2005: </strong>\' + Autolinker.link(String(feature.properties[\'YEAR_2005\'])) + \'<br><strong>2007: </strong>\' + Autolinker.link(String(feature.properties[\'YEAR_2007\'])) + \'<br><strong>2009: </strong>\' + Autolinker.link(String(feature.properties[\'YEAR_2009\']));layer.bindPopup(popupContent);}\nfunction doStyleORTHOTILES(feature) {return {color: \'#000000\',fillColor: \'#b6b6b6\',weight: 3.5,dashArray: \'\',opacity: 0.35,fillOpacity: 0.35};} \nvar orthoAerial= new L.geoJson(exp_AirOrthoAttributeGraph,{onEachFeature: pop_ORTHOTILES,style: doStyleORTHOTILES});\n\n'
##outFile.write(orthoFunc)

#GROUP BASEMAP LAYERS
GBasemaps='var baseLayers = {"OSM": OSMbase,"Grayscale": grayscale,"Streets": streets}; \n \n'
outFile.write(GBasemaps) #write baseLayers variable in java to the outFile

#BASEMAP LAYER CONTROL
LCGBasemaps='L.control.layers(baseLayers).addTo(map); \n' #add baseLayers to the 'map' variable
outFile.write(LCGBasemaps)

#ADD SCALE TO MAP
mapScale='L.control.scale({options: {position: \'bottomleft\',maxWidth: 100,metric: true,imperial: false,updateWhenIdle: false}}).addTo(map); \n \n' #add a scale bar to the 'map' variable
outFile.write(mapScale)

#SHOW SELECTED YEAR
selectedyear='function showValue(newValue){document.getElementById("range").innerHTML=newValue;}; \n \n' #creates function that shows the year selected on the slider
outFile.write(selectedyear)

#ON AND OFF TIMESLIDER FUNCTIONALITY
onoff='function layer(value) \n  {if (value >='+str(uniqueYears[0])+', value <'+str(uniqueYears[1])+') {' 
outFile.write(onoff) #write beginning of function that will turn on and off layers using the html slider
#note that because the first and last slider are unique from the middle slider there are three written in order: first (1), middle (n-2), last (1)
for x in xrange(1, leng):
    removelayers='map.removeLayer(Hamilton'+str(uniqueYears[x])+'); '
    outFile.write(removelayers)
outFile.write('map.removeLayer(orthoAerial); ')
firstadd='Hamilton'+str(uniqueYears[0])+'.addTo(map);} \n'
outFile.write(firstadd)

for x in xrange(1, leng):
    eliff='else if (value >= '+str(uniqueYears[x])+',value < '+ str(uniqueYears[x+1])+') {'
    outFile.write(eliff)
    for y in xrange(0, leng+1):
        if uniqueYears[y]==uniqueYears[x]:
            continue
        removelayers='map.removeLayer(Hamilton'+str(uniqueYears[y])+'); '
        outFile.write(removelayers)
    outFile.write('map.removeLayer(orthoAerial); ')
    addlayer='Hamilton'+str(uniqueYears[x])+'.addTo(map);} \n'
    outFile.write(addlayer)

    #LAST VALUE IN RANGE
eliff='else if (value == '+str(uniqueYears[leng])+') {'
outFile.write(eliff)
for x in xrange(0, leng):
    removelayers='map.removeLayer(Hamilton'+str(uniqueYears[x])+'); '
    outFile.write(removelayers)
outFile.write('map.removeLayer(orthoAerial); ')
endadd='Hamilton'+str(uniqueYears[x+1])+'.addTo(map);} \n' 
outFile.write(endadd)

    #ADD ORTHO AERIAL IMAGES AND YEARS TO TIMESLIDER
eliff='else if (value > '+str(uniqueYears[-1])+',value <= '+str(orthoYears[-1])+') {'
outFile.write(eliff)
for x in xrange(0, leng+1):
    removelayers='map.removeLayer(Hamilton'+str(uniqueYears[x])+'); '
    outFile.write(removelayers)
add='orthoAerial.addTo(map);}}; \n'
outFile.write(add)

#CLOSE SCRIPT
closescript='</script> \n\n'
outFile.write(closescript) #closes script

#CLOSE HTML
Closehtml='\n \n </html>'
outFile.write(Closehtml) #closes html

#COMPLETED ALERT
print 'The map has been written to file' #once the script has completed the python sheel will say it has been write to the file
inFile.close() #close inFile
outFile.close() #close outFile
