import os
import shutil
sPath=os.path.abspath(__file__) #get path of this file (script)
bName=os.path.basename(__file__) #get basename of this file (script)
lbName=len(bName)
sPath=sPath[:-lbName] #get directory of the location of this file (script)
f=0 #this value will count file sizes
fzip=[] #this array will contain all files to be moved to a folder
xml=[]
tif=[]
for files in os.listdir(sPath):
    if files[-3:] == 'tif':
        tif.append(files)
    elif files[-3:] == 'xml':
        xml.append(files)
folder=[]
for t in tif:
    for x in xml:
        if t[:-4]==x[:-4]:
            folder.append(t)
            folder.append(x)
            y=os.path.getsize(t)
            y=y+os.path.getsize(x)
            f=f+y
            folderName=folder[0]
            folderName=folderName[:-4]
            try:
                os.makedirs(folderName) #made the out directory the current Dir to create folders
            except OSError:
                if os.path.exists(folderName): #no not create if it already exists
                    pass
                else:
                    raise
            shutil.copy(t, folderName)
            shutil.copy(x, folderName)
            if f >2.00e9 and f<2.14e9: # if the cumulative file size is between 2.1 and 2.3GB 
                f=0 #once the file size is met clear the file size tally
                folder=[]
            else:
                continue
for item in os.listdir(sPath): #Selects all folders in the directory
    if item[-3:]!='tif' and item[-3:]!='xml' and item[-3:]!='zip' and item[-2:]!='py':
        print item #this prints the folder we are going through to give us an idea of how much progress we've made
        shutil.make_archive(item, 'zip', item) #zips each folder to the location desired
