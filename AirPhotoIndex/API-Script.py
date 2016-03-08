#Converts .tsv information to aerial photo index
# -*- coding: cp1252 -*-
import os
import sys

#SET INPUT AND OUTPUT FILES
inFile=open('Master Spreadsheet.tsv') #Name of file located in the directory of this script that stores the information
##input('Input location of the Master Spreadsheet (.tsv) within quotations and press enter: ')
#Note that the file entered must be a .tsv for this script to work
outfn='index.html' #Desired name of output file
if os.path.exists(outfn): #Check if file exists
    print 'It appears that '+ outfn +' already exists!' 
    os.remove(outfn) #Remove the file if it exists
    print outfn +' has now been removed!'
else:
    print outfn +' does not already exist!' #This will be written if the file does not exist
outFile=open(outfn, 'w') #Create a new output File (.html)

#READ CSV FILE
allcontent=inFile.readlines() #Read csv and group contents line by line
content=allcontent[3:] #Remove the first line from the content as it does not provide useful information

#GATHER UNIQUE YEARS FROM inFile
years=[] #Create an empty array where years from the spreadsheet (.csv, inFile) will be stored
for line in content:
    item=line.split('\t') #split lines of inFile into 'item' at each comma (,)
    year=item[17]
    if year[0]=='[':
        year=year[1:-1]
    year=year[:4]
    years.append(year) #add the first column [0] to the empty array named years
uniqueYears=sorted(set(years)) #Get unique years, and sort them numerically
uniqueYears=map(int,uniqueYears)
#HEADER SECTION
head='<html> \n <head> \n <title>McMaster Aerial Photographic Index</title> \n <meta charset="utf-8" /> \n <meta name="viewport" content="width=device-width, initial-scale=1.0"> \n <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" /> \n <link rel="stylesheet" type="text/css" href="css/own_style.css">\n<link href="http://loopj.github.io/jquery-simple-slider/css/simple-slider.css" rel="stylesheet" type="text/css" />\n<link rel="stylesheet" href="css/API.css">\n<script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>\n<script src="js/Autolinker.min.js"></script>\n<script src="http://code.jquery.com/jquery-1.11.1.min.js"></script>\n<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>\n<script src="js/simple-slider.js"></script>\n<script src="https://api.mapbox.com/mapbox.js/plugins/leaflet-markercluster/v0.4.0/leaflet.markercluster.js"></script>\n<link href="https://api.mapbox.com/mapbox.js/plugins/leaflet-markercluster/v0.4.0/MarkerCluster.css" rel="stylesheet" />\n<link href="https://api.mapbox.com/mapbox.js/plugins/leaflet-markercluster/v0.4.0/MarkerCluster.Default.css" rel="stylesheet" />\n</head> \n \n'
outFile.write(head) #write the html header to the outFile

#ORTHO AERIAL IMAGES YEARS
years2=[] #empty array that the years will be appended to
for x in [1999,2002,2005,2007,2010,2014]:
      years2.append(x) #add the year to the array if it is equal to a year in the range in the for loop
orthoYears=sorted(set(years2))
	  
#BODY HTML (ADDING THE MAP)
htmlbody='<body> \n <div id="map" style="width: 100%; height: 90%"></div> \n \n' #width and height can be changed to desired percentage of the frame/browser
outFile.write(htmlbody) #write the body html to the outFile
    #ADD TIMESLIDER TO BODY
leng=len(uniqueYears) -1
timeslider='<fieldset class="align-center"> \n <legend>Time Slider</legend> \n<input type="text" data-slider="true" data-slider-values='+",".join(str(i) for i in uniqueYears)+','+",".join(str(i) for i in orthoYears)+' data-slider-snap="true"> \n '
outFile.write(timeslider)
timesliderclose='<label class="align-left" for=year>'+str(uniqueYears[0])+'</label><label class="align-right" for=year>'+str(orthoYears[-1])+'</label> \n <script> \n $("[data-slider]") \n .each(function () { \n var input = $(this); \n $("<span>") \n .addClass("output") \n .attr("id", "newId") \n .insertAfter($(this)); \n }) \n .bind("slider:ready slider:changed", function (event, data) { \n $(this) \n .nextAll(".output") \n .html(data.value.toFixed(0)); \n }); \n </script> \n</fieldset>\n</body>\n'
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
        year=item[17] #year is in the first column
        year=year[:4]
        flightline=item[1] #flightline is in the second column
        if str(uniqueYears[x])==year: #if the year is equal to the first value in the cell (year) then append the flightline in the column beside it to the flightLine array
            flightLine.append(item[5]) 
        flightLine=sorted(set(flightLine)) #sort the flightlines for the year
    for line in content:
        item=line.split('\t')
        year=item[17]
        if year[0]=='[':
            year=year[1:-1]
        year=year[:4]
        ID=item[2]
        flightline=item[5]
        photo=item[6]
        scale=item[7]
        latitude=item[8]
        longitude=item[9]
        img=item[10]
        imglink=item[11]
        cflightline=flightline.translate(None,"-")
        cflightline=cflightline.translate(None,"?")
        cflightline=cflightline.translate(None,"/")
        cphoto=photo.translate(None," ")
        cphoto=cphoto.translate(None,"[")
        cphoto=cphoto.translate(None,"]")
        if img=="":
            imgsrc="" #If there is no value in the image column (img="") then don't do anything
        else:
            imgsrc='<a href="'+str(imglink)+'" target="_blank"><img src="'+str(img)+'" height="200" width="200"></a> <br>' #If image field is not empty then add the image
        if str(uniqueYears[x])==year:
            yfl.append(flightline)
    yfl=sorted(set(yfl))
    for line in content:
        item=line.split('\t')
        for z in xrange (0, len(item)-1):
            interest=item[z]
            if interest.startswith('"') and interest.endswith('"'):
                item[z]=interest[1:-1]
        year=item[17]
        if year[0]=='[':
            year=year[1:-1]
        year=year[:4]
        dateother=item[17]
        ID=item[3]
        flightline=item[5]
        photo=item[6]
        scale=item[7]
        latitude=item[8]
        longitude=item[9]
        img=item[10]
        dArchive=item[11]
        cflightline=flightline.translate(None,"-")
        cphoto=photo.translate(None," ")
        cphoto=cphoto.translate(None,"[")
        cphoto=cphoto.translate(None,"]")
        cphoto=cphoto.translate(None,"/")
        cflightline=cflightline.translate(None,"/")
        cflightline=cflightline.translate(None,"\'")
        if flightline=='' and photo=='':
            iTitle=item[0]
            iphoto=item[0]
        else:
            iTitle=''
            iphoto=photo
        iTitle=iTitle.translate(None," ")
        iTitle=iTitle.translate(None,"-")
        iTitle=iTitle.translate(None," ")
        iTitle=iTitle.translate(None,"[")
        iTitle=iTitle.translate(None,"]")
        iTitle=iTitle.translate(None,"/")
        iTitle=iTitle.translate(None,",")
        if dArchive!="":
            dalink='<a href="'+str(dArchive)+'" target="_blank">View/Download the Full-sized Image</a>'
        else:
            dalink=""
        if img=="":
            imgsrc="" #If there is no value in the image column (img="") then don't do anything
        else:
            imgsrc='<a href="'+str(dArchive)+'" target="_blank"><img src="'+str(img)+'" height="200" width="200"></a> <br>' #If image field is not empty then add the image
    
        for y in xrange (0, len(yfl)):
            if flightline==yfl[y] and str(uniqueYears[x])==year:
                markers='var '+str(ID)+str(uniqueYears[x])+str(cflightline)+str(cphoto)+str(iTitle)+'=L.marker(['+str(latitude)+','+str(longitude)+'], {icon: '+str(markercolours[y])+'Icon, time: "'+str(dateother)+'"}).bindPopup(\''+str(imgsrc)+'<strong>Set Name</strong> '+str(ID)+' '+str(dateother)+' <br><strong>Photo Date</strong> '+str(item[4])+' <br><strong>Flight Line</strong> '+str(flightline)+'<br> <strong>Photo</strong> '+str(iphoto)+'<br> <strong>Scale</strong> '+str(scale)+'<br> '+str(dalink)+'\'); \n'
                outFile.write(markers)
                markerarray.append(str(str(ID)+str(uniqueYears[x]))+str(cflightline)+str(cphoto)+str(iTitle)) #write name of the marker above to the marker array
            markerarray=sorted(set(markerarray)) #sort the marker array
            markerarrayNQ=str(markerarray).translate(None,"'") #remove quotations from the marker array so that it can be read in javascript (ex. ['a', 'b'] becomes [a, b]
            layerGroup='var Hamilton'+str(uniqueYears[x])+'=L.markerClusterGroup({disableClusteringAtZoom:13}).addLayers('+str(markerarrayNQ)+'); \n \n' #group all markers by year in a layer group read by javascript
            if flightline==yfl[y] and str(uniqueYears[x])==year:     
                yearlayers.append('Hamilton'+str(uniqueYears[x])) #adding each layerGroup created (from each year) to the massive array of all layers (yearlayers)
    outFile.write(layerGroup)
    yfl=[]

yearlayers=sorted(set(yearlayers))
#ADD BASEMAPS
Basemaps="var mbAttr = 'Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, ' + \n '<a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, ' + \n 'Imagery © <a href=\"http://mapbox.com\">Mapbox</a>' \n var osmattr='Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, ' + \n '<a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>' \n var mbUrl2 = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoibmlja2x1eW1lcyIsImEiOiJjaWhzM2dsem4wMGs2dGZraGY1MzN3YmZ2In0.fDtuZ8EU3C5330xaVS4l6A' \n var grayscale =	L.tileLayer(mbUrl2,{id: 'mapbox.light', attribution: mbAttr}), \n OSMbase = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: osmattr}), \n streets =	L.tileLayer(mbUrl2,{id: 'mapbox.high-contrast', attribution: mbAttr}); \n \n"
outFile.write(Basemaps) #write java for basemaps to outFile

#CREATE MAP
Lmap='var map=L.map(\'map\', {center:[43.26,-79.89],zoom: 11,layers:[OSMbase,'+str(yearlayers[0])+']}); \n' #str() says that the lowest year will be turned on when the map starts up
outFile.write(Lmap) #write map to outFile
yearlayerz=str(yearlayers).translate(None,"'") #remove single quotations from all years in array yearlayers
outFile.write('var Years=L.markerClusterGroup({disableClusteringAtZoom:13}).addLayers('+str(yearlayerz)+'); \n') #create a layer group containing all years as read by the java


#GROUP BASEMAP LAYERS
GBasemaps='var baseLayers = {"OSM": OSMbase,"Grayscale": grayscale,"Streets": streets}; \n \n'
outFile.write(GBasemaps) #write baseLayers variable in java to the outFile

#GROUP OrthoImagery LAYERS
for x in xrange(0,len(orthoYears)):
	layer = "var Hamilton_"+str(orthoYears[x])+" = L.tileLayer('http://tiles.mcmaster.ca/Hamilton_"+str(orthoYears[x])+"/{z}/{x}/{y}.png', {format: 'image/png',tms: true,noWrap: true,});\n"
	outFile.write(layer) #write ortholayer variable in java to the outFile

#BASEMAP LAYER CONTROL
LCGBasemaps='L.control.layers(baseLayers).addTo(map); \n' #add baseLayers to the 'map' variable
outFile.write(LCGBasemaps)

#ADD SCALE TO MAP
mapScale='L.control.scale({options: {position: \'bottomleft\',maxWidth: 100,metric: true,imperial: false,updateWhenIdle: false}}).addTo(map); \n \n' #add a scale bar to the 'map' variable
outFile.write(mapScale)

#ON AND OFF TIMESLIDER FUNCTIONALITY


def remChoose(x,years): #decide whether the remove function should be written for the points (uniqueYears) or orthophotos (orthoYears)
	if years==uniqueYears:
		return 'map.removeLayer(Hamilton'+str(x)+');'
	elif years==orthoYears:
		return 'map.removeLayer(Hamilton_'+str(x)+');'
	else: pass		
def addChoose(x,years): #decide whether the add function should be written for the points (uniqueYears) or orthophotos (orthoYears)
	if years==uniqueYears:
		return 'Hamilton'+str(x)+'.addTo(map);'
	elif years==orthoYears:
		return 'Hamilton_'+str(x)+'.addTo(map).bringToFront();'
	else: pass		
def Remove(x,years,layer): 
	if x in years:
		layer.append(remChoose(x,years))
	else: pass
def Add(x,years):
	if x in years:
		addlayer=addChoose(x,years)
		outFile.write(addlayer)
	else: pass
def removeRun(combyear,x,years):
	removelayers = []
	for y in xrange(0,len(combyear)):
		if combyear[y]==combyear[x]:
			continue
		Remove(combyear[y],years,removelayers)
	outFile.write(' '.join(removelayers))
	

onoff='function layer(value) \n  {if (value =='+str(uniqueYears[0])+') {' 
outFile.write(onoff) #write beginning of function that will turn on and off layers using the html slider
#note that because the first and last slider are unique from the middle slider there are three written in order: first (1), middle (n-2), last (1)
yearscomb = sorted(set(uniqueYears)|set(orthoYears))
removeRun(yearscomb,0,uniqueYears)
removeRun(yearscomb,0,orthoYears)   
Add(yearscomb[0],uniqueYears)
outFile.write('} \n')

yearscomb = sorted(set(uniqueYears)|set(orthoYears))		
for x in xrange(1, len(yearscomb)-1):
	eliff='else if (value == '+str(yearscomb[x])+') {'
	outFile.write(eliff)
	removeRun(yearscomb,x,uniqueYears)
	removeRun(yearscomb,x,orthoYears)
	Add(yearscomb[x],uniqueYears)
	Add(yearscomb[x],orthoYears)
	outFile.write('} \n')
		
eliff='else if (value == '+str(yearscomb[-1])+') {'
outFile.write(eliff)
removeRun(yearscomb,-1,uniqueYears)
removeRun(yearscomb,-1,orthoYears)
Add(yearscomb[-1],uniqueYears)
Add(yearscomb[-1],orthoYears)
outFile.write('}}; \n\n')

#TIMESLIDER FUNCTION
timesliderfunc = '$("body").mousemove(function() { \n layer(Number($("#newId").text())); \n });' 
outFile.write(timesliderfunc)

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

