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
markerYears=sorted(set(years)) #Get unique years, and sort them numerically
markerYears=map(int,markerYears)
#HEADER SECTION
head='<html> \n <head> \n <title>McMaster Aerial Photographic Index</title>\n<meta charset="utf-8" />\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" />\n<link rel="stylesheet" type="text/css" href="css/own_style.css">\n<link href="http://loopj.github.io/jquery-simple-slider/css/simple-slider.css" rel="stylesheet" type="text/css" />\n<link rel="stylesheet" href="css/API.css">\n<link rel="stylesheet" href="https://ismyrnow.github.io/Leaflet.groupedlayercontrol/src/leaflet.groupedlayercontrol.css">\n<script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>\n<script src="data/FIP_bounds.js"></script>\n<script src="http://code.jquery.com/jquery-1.11.1.min.js"></script>\n<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>\n<script src="https://ismyrnow.github.io/Leaflet.groupedlayercontrol/src/leaflet.groupedlayercontrol.js"></script>\n<script src="js/simple-slider.js"></script>\n<script src="js/control-layers.js"></script>\n<script src="https://api.mapbox.com/mapbox.js/plugins/leaflet-markercluster/v0.4.0/leaflet.markercluster.js"></script>\n<link href="https://api.mapbox.com/mapbox.js/plugins/leaflet-markercluster/v0.4.0/MarkerCluster.css" rel="stylesheet" />\n<link href="https://api.mapbox.com/mapbox.js/plugins/leaflet-markercluster/v0.4.0/MarkerCluster.Default.css" rel="stylesheet" />\n<link rel="stylesheet" href="http://eclipse1979.github.io/leaflet.slider/dist/leaflet-slider.css">\n<script src="http://eclipse1979.github.io/leaflet.slider/dist/leaflet-slider.js"></script>\n</head> \n \n'
outFile.write(head) #write the html header to the outFile

#ORTHO AERIAL IMAGES YEARS
years2=[] #empty array that the years will be appended to
for x in [1999,2002,2005,2007,2010,2014]: ####ADD TO THIS LIST IF MORE LAYERS ARE AVAILABLE on the tile.mcmaster.ca server
      years2.append(x) #add the year to the array if it is equal to a year in the range in the for loop
orthoYears=sorted(set(years2))

#FIP IMAGES YEARS
years3=[] #empty array that the years will be appended to
for x in [1898]: ####ADD TO THIS LIST IF MORE LAYERS ARE AVAILABLE on the tile.mcmaster.ca server
      years3.append(x) #add the year to the array if it is equal to a year in the range in the for loop
FIPYears=sorted(set(years3))
	  
#BODY HTML (ADDING THE MAP)
htmlbody='<body> \n <div id="map" style="width: 100%; height: 90%"></div> \n \n' #width and height can be changed to desired percentage of the frame/browser
outFile.write(htmlbody) #write the body html to the outFile
    #ADD TIMESLIDER TO BODY
uniqueYears=sorted(set(markerYears)|set(orthoYears)|set(FIPYears))
leng=len(uniqueYears) -1
timeslider='<fieldset class="align-center"> \n <legend>Time Slider</legend> \n<input type="text" id="slide" data-slider="true" data-slider-values='+",".join(str(i) for i in markerYears)+' data-slider-snap="true" value=1919> \n '
outFile.write(timeslider)
timesliderclose='<label class="align-left" for=year>'+str(markerYears[0])+'</label><label class="align-right" for=year>'+str(markerYears[-1])+'</label> \n <script> \n $("[data-slider]") \n .each(function () { \n var input = $(this); \n $("<span>") \n .addClass("output") \n .attr("id", "newId") \n .insertAfter($(this)); \n }) \n .bind("slider:ready slider:changed", function (event, data) { \n $(this) \n .nextAll(".output") \n .html(data.value.toFixed(0)); \n }); \n $(document).ready(function()\n{$("body").on("click",":radio",function(evt) {radio(evt.target.layerId);});\n}); \n</script> \n</fieldset>\n</body>\n'
outFile.write(timesliderclose) #Write functions for displaying the value of the timeslider and for obtaining the layer that has been clicked in the layer control window

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
FIPbounds=[] #Create an empty array where all the different FIP bounds will be mentioned
yfl=[]
id={}
for x in xrange(0, len(markerYears)): #iterates through each year
	z=1 #numbers each different markers for labeling their variable name in the javascript of outFile
	markerarray=[] #Create empty array for all markers of the same year
	layerarray=[] #Create empty array for all layers of the same year
	yflightline=[]
	for line in content:
		item=line.split('\t') #similar to above, split each line into items at each comma
		year=item[17] #year is in the first column
		year=year[:4]
		flightline=item[1] #flightline is in the second column
		if str(markerYears[x])==year: #if the year is equal to the first value in the cell (year) then append the flightline in the column beside it to the flightLine array
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
		if str(markerYears[x])==year:
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
			if flightline==yfl[y] and str(markerYears[x])==year:
				markers='var '+str(ID)+str(markerYears[x])+str(cflightline)+str(cphoto)+str(iTitle)+'=L.marker(['+str(latitude)+','+str(longitude)+'], {icon: '+str(markercolours[y])+'Icon, time: "'+str(dateother)+'"}).bindPopup(\''+str(imgsrc)+'<strong>Set Name</strong> '+str(ID)+' '+str(dateother)+' <br><strong>Photo Date</strong> '+str(item[4])+' <br><strong>Flight Line</strong> '+str(flightline)+'<br> <strong>Photo</strong> '+str(iphoto)+'<br> <strong>Scale</strong> '+str(scale)+'<br> '+str(dalink)+'\'); \n'
				outFile.write(markers)
				markerarray.append(str(str(ID)+str(markerYears[x]))+str(cflightline)+str(cphoto)+str(iTitle)) #write name of the marker above to the marker array
			else: pass
	if markerYears[x] in markerYears:
		layerarray.append('Markers'+str(markerYears[x]))
	markerarray=sorted(set(markerarray)) #sort the marker array
	markerarrayNQ=str(markerarray).translate(None,"'") #remove quotations from the marker array so that it can be read in javascript (ex. ['a', 'b'] becomes [a, b]
	markerGroup='var Markers'+str(markerYears[x])+'=L.markerClusterGroup({disableClusteringAtZoom:13}).addLayers('+str(markerarrayNQ)+'); \n \n' #group all markers by year in a marker cluster group read by javascript
	layerarray=sorted(set(layerarray)) #sort the layer array
	layerarrayNQ=str(layerarray).translate(None,"'") #remove quotations from the marker array so that it can be read in javascript (ex. ['a', 'b'] becomes [a, b]
	layerGroup='var Hamilton'+str(markerYears[x])+'=L.featureGroup('+str(layerarrayNQ)+'); \n \n' #group all layers by  by year
	yearlayers.append('Hamilton'+str(markerYears[x])) #adding each layerGroup created (from each year) to the massive array of all layers (yearlayers)
	id[str(markerYears[x])]='Hamilton'+str(markerYears[x])
	outFile.write(markerGroup)
	outFile.write(layerGroup)
	yfl = []

orthoarray=[]
FIParray=[]
for x in xrange(0, len(uniqueYears)): #iterates through each year
	if uniqueYears[x] in orthoYears:
		layer = "var Hamilton_"+str(uniqueYears[x])+" = L.tileLayer('http://tiles.mcmaster.ca/Hamilton_"+str(uniqueYears[x])+"/{z}/{x}/{y}.png', {format: 'image/png',tms: true,noWrap: true,maxZoom: 19});\n"
		outFile.write(layer) #write Ortho Layer variable in java to the outFile
		orthoarray.append('\"Hamilton '+str(uniqueYears[x])+'\": Hamilton_'+str(uniqueYears[x]))
	if uniqueYears[x] in FIPYears:
		layer = "var FIP_"+str(uniqueYears[x])+" = L.tileLayer('http://tiles.mcmaster.ca/FIP_"+str(uniqueYears[x])+"/{z}/{x}/{y}.png', {format: 'image/png',tms: true,noWrap: true,maxZoom: 19});\n"
		outFile.write(layer) #write FIP layer variable in java to the outFile
		bound = "var bound_"+str(uniqueYears[x])+" =L.geoJson(B_"+str(uniqueYears[x])+",{style:{'fillOpacity':0,'opacity':0}});\n" 
		outFile.write(bound) # write FIP bound variable in java to the outFile 
		FIP = "var FIP"+str(uniqueYears[x])+" =L.featureGroup([FIP_"+str(uniqueYears[x])+", bound_"+str(uniqueYears[x])+"]);\n"
		outFile.write(FIP)
		FIPbounds.append('bound_'+str(uniqueYears[x])) # This set of bounds is to be used for dynamic zooming to the level of the FIPs
		FIParray.append('\"Hamilton '+str(uniqueYears[x])+'\": FIP'+str(uniqueYears[x]))
	
yearlayers=sorted(set(yearlayers))
FIPbounds=sorted(set(FIPbounds))
orthoarray=sorted(set(orthoarray))
FIParray=sorted(set(FIParray))
#ADD BASEMAPS
Basemaps="var mbAttr = 'Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, ' +\n'<a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, ' +\n'Imagery © <a href=\"http://mapbox.com\">Mapbox</a>' \n var osmattr='Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, ' +\n'<a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>'\nvar mbUrl2 = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoibmlja2x1eW1lcyIsImEiOiJjaWhzM2dsem4wMGs2dGZraGY1MzN3YmZ2In0.fDtuZ8EU3C5330xaVS4l6A'\nvar grayscale = L.tileLayer(mbUrl2,{id: 'mapbox.light', attribution: mbAttr}),\nOSMbase = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: osmattr}),\nstreets =	L.tileLayer(mbUrl2,{id: 'mapbox.high-contrast', attribution: mbAttr});\n\n"
outFile.write(Basemaps) #write java for basemaps to outFile

#CREATE MAP
Lmap='var map=L.map(\'map\', {center:[43.26,-79.89],zoom: 11,layers:[OSMbase]}); \n\n' #str() says that the lowest year will be turned on when the map starts up
outFile.write(Lmap) #write map to outFile
FIPlayers=str(FIPbounds).translate(None,"'") #remove single quotations from all years in array FIPlayers
outFile.write('var FIP=L.featureGroup('+str(FIPlayers)+'); \n')
outFile.write("map.on('layeradd', function (e) {if (FIP.hasLayer(e.layer)){(map.fitBounds(e.layer.getBounds()))};})\n\n") #dynamic zooming to the extent of the FIPs
yearlayerz=str(yearlayers).translate(None,"'") #remove single quotations from all years in array yearlayers
outFile.write('var Years=L.layerGroup('+str(yearlayerz)+'); \n\n')
ids=str(id).translate(None,"'") #id array to allow for adding layers based on timeslider values
outFile.write('var id='+str(ids)+'; \n') 
orthoarrayz=str(orthoarray).translate(None,"'").translate(None,"]").translate(None,"[") #remove single quotations and square brackets from all years in array orthoarray
FIParrayz=str(FIParray).translate(None,"'").translate(None,"]").translate(None,"[") #remove single quotations and square brackets from all years in array FIParray
outFile.write('var baseLayers = {"OSM": OSMbase,"Grayscale": grayscale,"Streets": streets}; \n') 
outFile.write('var overlays = {"Ortho Imagery":{'+str(orthoarrayz)+'},\n"Fire Insurance Plans":{'+str(FIParrayz)+'}};\n\n') #baselayers and overlays to be used for the basemap layer control

#BASEMAP LAYER CONTROL
LCGBasemaps='var control = L.control.groupedLayers(baseLayers, overlays,{exclusiveGroups: ["Ortho Imagery","Fire Insurance Plans"],collapsed:false}).addTo(map); \n\n' #add layer control to the 'map' variable
outFile.write(LCGBasemaps)

#ADD SCALE TO MAP
mapScale='L.control.scale({options: {position: \'bottomleft\',maxWidth: 100,metric: true,imperial: false,updateWhenIdle: false}}).addTo(map); \n\n' #add a scale bar to the 'map' variable
outFile.write(mapScale)

##ADD OPACITY SLIDER
opacFunction='slider = L.control.slider(function(value) {'
outFile.write(opacFunction)
for x in xrange(0,len(orthoYears)):
	opacLayer='Hamilton_'+str(orthoYears[x])+'.setOpacity(value);'
	outFile.write(opacLayer)
for x in xrange(0,len(FIPYears)):
	opacLayer='FIP_'+str(FIPYears[x])+'.setOpacity(value);'
	outFile.write(opacLayer)
opacEnd='},\n{position: "topright",max: 1,value: 1,step:0.05,size: "200px",collapsed: false,id: "slider"}).addTo(map);\n\n'
outFile.write(opacEnd) #Add opacity slider to the map for the orthophotos and FIPs

## BASEMAP LAYER CONTROL CHANGE TIMESLIDER VALUE
sliderval='function radio(layerid)\n{obj = control._layers[layerid];\nfor(var key in id) {\n  if(id[key] === obj.layer) {$("#slide").simpleSlider("setValue", key);};\n};}\n\n'
outFile.write(sliderval) #Change the timeslider value based on overlay clicked in layer control

## TIMESLIDER SWITCHING BETWEEN YEARS
yearswitch='function layer(value) \n  {if (map.hasLayer(id[value])==false) {map.eachLayer(function(layer){if (Years.hasLayer(layer)==true) {map.removeLayer(layer)}}); id[value].addTo(map).bringToFront();}};\n\n'  
outFile.write(yearswitch) #Based on timeslider value, add layers to the map

#TIMESLIDER FUNCTION
timesliderfunc = '$("body").mousemove(function() { \n layer(Number($("#newId").text())); \n });\n\n' 
outFile.write(timesliderfunc) #Get value from timeslider to use in the previous function

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

