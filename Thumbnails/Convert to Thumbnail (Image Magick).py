#THIS SCRIPT REQUIRES THE USER TO DOWNLOAD AND INSTALL IMAGEMAGICK PROGRAM
#Do not run this script until ImageMagick (http://www.imagemagick.org/script/binary-releases.php) is installed on your computer

#Creates thumbnails of original aerial image in duplicated folder structure in the locations of the executed script (this script: __file__)
#Note: the thumbnails & files will be created in the location of this script. Please adjust it before executing should you wish to change it.

import os
import subprocess #allows commandline functions to executed

inDir=input('Insert the directory path  of where the tifs are stored within single quotations (ex: \'C:/Digitization_Projects/AirPhotos\'). Copy it here and press enter: ')#modify this string to the location where the folders containing the airphotos is
inBase=inDir[3:] #removes the drive in the filename to replicate the folders in another location
scriptname=os.path.basename(__file__) #Get the path of this script
sclen=len(scriptname)
home=os.getcwd() #Set script folder location/directory as home
folderNames=[] #Create an empty array
for folder in os.listdir(inDir):
    folderNames.append(folder) #created a list of folders
for x in xrange (0, len(folderNames)): #iterate through each folder in the array folderNames
    outDir=str(inBase)+'/'+str(folderNames[x])
    try:
        os.makedirs(outDir) #make the out directory the current Dir to create folders
    except OSError:
        if os.path.exists(outDir):
            pass
        else:
            raise
    os.chdir(str(inDir)+'/'+str(folderNames[x])) #modify directory to each folder individually
    outDir=outDir.replace('/','\\')
    mogrify='mogrify -resize 200x -format jpg *tif -path '+str(home)+'\\'+str(outDir)+' *jpg'
    subprocess.call(mogrify) #runs mogrify variable above in command line windows
    os.chdir(home)
