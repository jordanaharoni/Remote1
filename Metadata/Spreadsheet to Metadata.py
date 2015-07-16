import os
inFile=open(input('Input location of the Master Spreadsheet (.tsv) within quotations and press enter: '))

#READ CSV FILE AND GATHER UNIQUE YEARS
allcontent=inFile.readlines() #Read csv and group contents line by line
content=allcontent[2:2752] #Remove the first line from the content
    #GATHER UNIQUE YEARS FROM SPREADSHEET AND ADD THEM TO AN ARRAY
years=[] #creates an empty array where all of the years from the spreadsheet will be stored
for line in content:
    item=line.split('\t') #split the items in each line by the tabs (\t) between them
    year=item[17] #year value is in column 20 (or 19 if we begin count at 0)
    years.append(year)
years=sorted(set(years))
print years
    #DEFINE FILE NAMES FROM THE SPREADSHEET AND ADD THEM TO AN ARRAY
outFiles=[] #creates an empty array where the name of all files will be stored
for line in content:
    item=line.split('\t') #split the items in each line by the tabs (\t) between them
    IDlocation=item[3] #location of set is in column 4 (or 3 if we begin count at 0)
    year=item[17]
    outfn='Metadata '+str(IDlocation)+' Airphotos '+str(year)+'.txt' #structure of filename
    outFiles.append(outfn) #add structure of out Files to an array, which we will pull from later
outFiles=sorted(set(outFiles))

#CREATING MASTER METADATA FILE
mName='Air Photo Metadata Master.txt'
if os.path.exists(mName): #Check if file exists
    os.remove(mName) #Remove the file if it exists
mMaster=open(mName, 'wb') #Create a new output File (.txt)
home=os.getcwd()
    #CREATING HEADERS FOR NEW FILES
mtitle='Identifier\tTitle\tSubtitle\tCorporate Name/Author\tPersonal Name/Author\tType of resource\tGenre\tDate\tSearchable Date\tPublisher\tPlace of publication\tLanguage\tForm\tExtent/Scale\tPhysical description note\tNote\tSubject(geographic)\tSubject(geographic)\tSubject(geographic)\tContinent\tCountry\tProvince/state\tRegion\tCounty\tCity\tCity section\tArea\tCoordinates\r\n'
sTitle='identifier\ttitle\tsubtitle\tcorporateauthor\tpersonalauthor\ttypeofresource\tgenreloc\tdateCreated\tsearchDate\tpublisher\tpublicationplace\tlanguage\tphysicalform\tphysicalextent\tphysicalnote\tnote\tsubjectgeographic\tsubjectgeographic\tsubjectgeographic\tcontinent\tcountry\tprovince\tregion\tcounty\tcity\tcitySection\tarea\tcoordinates\r\n'
mMaster.write(mtitle) #Writes title line into mMaster file
mMaster.write(sTitle) #Write sub title line into mMaster file

#CREATING FOLDER FOR INDIVIDUAL METADATA FILES
newDir="Metadata by Set" #Name of folder that will contain individual metadata files
try:
    os.makedirs(newDir) #Creates the folder (directory)
except OSError:
    if os.path.exists(newDir):
        pass
    else:
        raise
os.chdir(newDir) #Changes this new folder to the current directory/folder we are in
    #CREATING METADATA FILE IN FOLDER FOR EACH SET FROM SPREADSHEET
for y in xrange (0, len(outFiles)): #iterates through each value in the array outFiles created above
    if os.path.exists(outFiles[y]): #Check if file exists
        os.remove(outFiles[y]) #Remove the file if it exists
    outFile=open(outFiles[y], 'wb') #Create a new output File (.txt) for every value in the array
    #WRITE HEADER TITLE
    outFile.write(mtitle)
    outFile.write(sTitle)
    #FORMAT ITEMS & WRITE TO FILES
    for line in content:
        item=line.split('\t')
        #REMOVE ANY QUOTATIONS IN ALL ITEMS
        for z in xrange (0, len(item)-1):#iterates through all items in each row
            interest=item[z]
            if interest.startswith('"') and interest.endswith('"'): #if the item is surrounded by quotations they are removed in the following line
                item[z]=interest[1:-1]
        ryear=item[17]
        IDlocation=item[3]
        IDlocation=IDlocation.translate(None,"?") #remove any ? value from the years
        if IDlocation[0]=='[': #remove square brackets for creating an array of years (no special characters desired)
            IDlocation=IDlocation[1:-1]
        elif len(IDlocation)==5:
            IDlocation=IDlocation[:-1]
        fileName=outFiles[y]
        #WRITE RANGE YEAR SETS (EX. 1954-1955)
        if IDlocation==fileName[9:-24] and ryear==fileName[-13:-4]: #checks if file has year range, and the location name match
            year=item[4]
            sYear=year #only first four values of the year
            sYear=year.translate(None,"?") #remove any ? value from the years
            if sYear[0]=='[': #remove square brackets for creating an array of years (no special characters desired)
                sYear=sYear[1:-1]
            flightline=item[5]
            photo=item[6]
            scale=item[7]
            latitude=item[8]
            longitude=item[9]
            author1=item[13]
            author2=item[14]
            publisher=item[15]
            publisherloc=item[16]
            physicalDescription=item[18]
            dateother=item[17]
            note=item[19]
            subject1=item[20]
            subject2=item[21]
            subject3=item[22]
            continent=item[23]
            country=item[24]
            province=item[25]
            region=item[26]
            county=item[27]
            city=item[28]
            citysection=item[29]
            if flightline!='': #if the field is not empty ''
                eflightline='Flightline '+str(flightline) #formatting for title
                flightline='_'+str(flightline)
            else:
                eflightline=''
            if photo!='':
                ephoto='Photo '+str(photo) #formatting for title
            else:
                ephoto=''
            if flightline!='' or photo!='':
                sq1=' : ['
                sq2=']'
                join='-'
            else:
                sq1=''
                sq2=''
                join=''
            if flightline!='' and photo!='':
                Tjoin='-'
            else:
                Tjoin=''
            identifier='AirPhotos_'+str(IDlocation)+'_'+str(dateother)+str(flightline)+str(join)+str(photo)
            flightline=item[5]
            if item[0]!="": #format for if the air photo has a title on it (aka the very first column has content)
                title=str(item[0])+str(sq1)+str(eflightline)+str(Tjoin)+str(ephoto)+str(sq2)
            else:
                title='['+str(item[1])+', '+str(dateother)+']'+str(sq1)+str(eflightline)+str(Tjoin)+str(ephoto)+str(sq2)
            entry=str(identifier)+'\t'+str(title)+'\t\t'+str(author1)+'\t'+str(author2)+'\tcartographic\tAerial photographs\t'+str(year)+'\t'+str(sYear)+'\t'+str(publisher)+'\t'+str(publisherloc)+'\teng\tremote-sensing image\t'+str(scale)+'\t'+str(physicalDescription)+'\t'+str(note)+'\t'+str(subject1)+'\t'+str(subject2)+'\t'+str(subject3)+'\t'+str(continent)+'\t'+str(country)+'\t'+str(province)+'\t'+str(region)+'\t'+str(county)+'\t'+str(city)+'\t'+str(citysection)+'\t'+str(area)+'\tlatitude '+str(latitude)+' ; longitude '+str(longitude)+'\r\n'
            outFile.write(entry) #write entry variable to the respective file in the new folder/directory
            mMaster.write(entry) #write entry variable to the master metatdata sheet
        #WRITE SINGLE YEAR SETS (EX. 1955)
        elif ryear==fileName[-8:-4] and IDlocation==fileName[9:-19]: #checks if file year and the location name match (ex. Hamilton 1920)
            year=item[4]
            sYear=year #only first four values of the year
            sYear=year.translate(None,"?") #remove any ? value from the years
            if sYear[0]=='[': #remove square brackets for creating an array of years (no special characters desired)
                sYear=sYear[1:-1]
            flightline=item[5]
            photo=item[6]
            scale=item[7]
            latitude=item[8]
            longitude=item[9]
            author1=item[13]
            author2=item[14]
            publisher=item[15]
            publisherloc=item[16]
            physicalDescription=item[18]
            dateother=item[17]
            note=item[19]
            subject1=item[20]
            subject2=item[21]
            subject3=item[22]
            continent=item[23]
            country=item[24]
            province=item[25]
            region=item[26]
            county=item[27]
            city=item[28]
            citysection=item[29]
            area=item[30]
            if flightline!='': #if the field is not empty ''
                eflightline='Flightline '+str(flightline) #formatting for title
                flightline='_'+str(flightline)
            else:
                eflightline=''
            if photo!='':
                ephoto='Photo '+str(photo) #formatting for title
            else:
                ephoto=''
            if flightline!='' or photo!='':
                sq1=' : ['
                sq2=']'
                join='-'
            else:
                sq1=''
                sq2=''
                join=''
            if flightline!='' and photo!='':
                Tjoin='-'
            else:
                Tjoin=''
            identifier='AirPhotos_'+str(IDlocation)+'_'+str(dateother)+str(flightline)+str(join)+str(photo)
            flightline=item[5]
            if item[0]!="": #format for if the air photo has a title on it (aka the very first column has content)
                title=str(item[0])+str(sq1)+str(eflightline)+str(Tjoin)+str(ephoto)+str(sq2)
            else:
                title='['+str(item[1])+', '+str(dateother)+']'+str(sq1)+str(eflightline)+str(Tjoin)+str(ephoto)+str(sq2)
            entry=str(identifier)+'\t'+str(title)+'\t\t'+str(author1)+'\t'+str(author2)+'\tcartographic\tAerial photographs\t'+str(year)+'\t'+str(sYear)+'\t'+str(publisher)+'\t'+str(publisherloc)+'\teng\tremote-sensing image\t'+str(scale)+'\t'+str(physicalDescription)+'\t'+str(note)+'\t'+str(subject1)+'\t'+str(subject2)+'\t'+str(subject3)+'\t'+str(continent)+'\t'+str(country)+'\t'+str(province)+'\t'+str(region)+'\t'+str(county)+'\t'+str(city)+'\t'+str(citysection)+'\t'+str(area)+'\tlatitude '+str(latitude)+' ; longitude '+str(longitude)+'\r\n'
            outFile.write(entry) #write entry variable to the respective file in the new folder/directory
            mMaster.write(entry) #write entry variable to the master metatdata sheet
    outFile.close() #close outFile
inFile.close() #close inFile
mMaster.close() #close master metadata file
