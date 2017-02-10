import subprocess
import sys
import os
import re
from Const import *

'''
Creates a dictionary based on the Lena directory structure.
Writes this dictionary to a text file.
Reads and reconstructs the dictionary if necessary.
Suppose just under the top leval Lena directory, we have
directories PX78, AM28, AM29
Suppose these directories have the following subdirectories:
PX78 has 2010_12
AM28 has 2010_12, 2011_01, 2011_02
AM29 has 2010_12, 2011_01, 2011_02

Then invoking makeDirsDict produces this dictionary:
{'PX78': ['2010_04'],
 'AM28': ['2010_12', '2011_01', '2011_02'],
 'AM29: ['2010_12', '2011_01', '2011_02']}

Each top level directory is a key with subdirectory names as values.

The program passes over non-standard top level directores, i.e., those
that don't match the regular expression format: [A-Z]{2}[0-9]{2}
PX78 matches Data_General does not.  

Usage:
$python DirsDict <top level dir for its and wav files inp> <dict output file>
'''

class DirsDict:
    
    def __init__(self):
        print 'DirsDict object created'

        
        print 'Continuing will remove previously built lenaUtils and lenaMatrices'
        answ = raw_input('Do you want to continue (y/n)?')
        if answ != 'n' and answ != 'y':
            print 'answer must be y or n'
            print 'Exiting'
            sys.exit()
        if answ == 'n':
            print 'Exiting'
            sys.exit()

    #Delete ../lenaMatrices if it exists
        errCode = os.system('ls ' + Const.LOC_OUT)
        if errCode == 0: #directory exists
            os.system('rm -r ' + Const.LOC_OUT)
            print Const.LOC_OUT + ' deleted'

    #Delete ../lenaUtils if its exists
        errCode = os.system('ls ' + Const.LOC_UTIL)
        if errCode == 0: #directory exists
            os.system('rm -r ' + Const.LOC_UTIL)
            print Const.LOC_UTIL + ' deleted'
    
    #Delete .pyc files if they exist
        errCode = os.system('ls *.pyc')
        if errCode == 0: #files exist
            os.system('rm *.pyc')
            print '.pyc files deleted'

                      

    #make dictionary of directories using dictionary comprehension
    #Const.LOC_INP is the path to the directory holding its and wav files
    def makeDirsDict(self):
        #make a list of everything in the top level directory
        #keep only directories that have two upper case letters followed by two digits
        #There are non-standard files in the LENA directory, including directories like S1SJ that contain
        #only its files.  These are passed over.

        dirs = os.listdir(Const.LOC_INP)
	dirs1 = [item for item in dirs if len(item) == 4]
	
        dirs2 = re.findall(r"[A-Z]{2}[0-9]{2}"," ".join(dirs1))
        dirsDict = {folder:os.listdir(Const.LOC_INP + folder) for folder in dirs2}
 
        print 'File structure dictionary created'
        return dirsDict

        
    #write the dictionary to a file
    def writeDict(self, dirsDict):
        errCode = os.system('mkdir ' + Const.LOC_UTIL)
        if errCode > 0:
            print 'problem creating ' + Const.LOC_UTIL + 'in writeDict'
            sys.exit()

        arg = Const.LOC_UTIL + Const.DICTFILE
        fout = open(arg, 'w')
        fout.write(str(dirsDict))
        fout.close()
        print 'File structure dictionary written to a file'

        
    #read the file into a dictionary
    def readDict(self):
        fin = open(Const.LOC_UTIL + Const.DICTFILE, 'r')
        dirsDict = eval(fin.read())
        fin.close()
        print 'File structure dictionary read into a dictionary'
        return dirsDict

        
   
