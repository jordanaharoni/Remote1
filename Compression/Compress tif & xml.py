import os
import shutil

sPath=os.path.abspath(__file__) #get path of this file (script)
bName=os.path.basename(__file__) #get basename of this file (script)
lbName=len(bName)
sPath=sPath[:-lbName] #get directory of the location of this file (script)
x=0 #this value will count file sizes
fzip=[] #this array will contain all files to be moved to a folder
for files in os.listdir(sPath):
    if files[-3:] == 'tif' or files[-3:] == 'xml': #only sort through tif and xml files to sort into folders with size restrictions
        fzip.append(files) #add the name of the files to fzip array
        y=os.path.getsize(files) #gets file size
        x=x+y #adds file sizes of files in the array
        zipName=fzip[0]
        zipName=zipName[:-4] #get name of the first file in the array and remove the extension. This name will be used as the storage folder
        try:
            os.makedirs(zipName) #made the out directory the current Dir to create folders
        except OSError:
            if os.path.exists(zipName): #no not create if it already exists
                pass
            else:
                raise
        shutil.copy(files, zipName) #copy current file to the folder
        if x >2.00e9 and x<2.14e9: # if the cumulative file size is between 2.1 and 2.3GB 
            x=0 #once the file size is met clear the file size tally
            fzip=[] #clear the array for the create of the next folder
    else:
        continue
for item in os.listdir(sPath): #Selects all folders in the directory
    if item[-3:]!='tif' and item[-3:]!='xml' and item[-3:]!='zip' and item[-2:]!='py':
        print item #this prints the folder we are going through to give us an idea of how much progress we've made
        shutil.make_archive(item, 'zip', item) #zips each folder to the location desired


