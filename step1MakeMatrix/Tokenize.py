import subprocess
import sys
import xlrd #installed with sudo apt-get install python-xlrd
import csv
from Const import *
from CleanUp import *

class Tokenize:
    """
    1. Create a directory structure that mirrors the LENA structure
    2. Copy .its files to mirror file system
    3. Build a corresponding .tok file for each .its file
       a. First line contains file id
       b. Second line contains family id and hearing status
       c. Third line contains child age and sex info
       d. Subsequent lines contain speaker information (i.e., lines from the
          .its file beginning "<Segment spkr ...>.")
    4. The .tok file will be used by the CreateMatrix object to create
       a. a file with file id and family info (e.g. AM28 and TD)
       b. a file that can be transformed into a matlab matrix containing
          speaker info (FAN, MAN, etc), start/stop times, child adjacency info

    Input:
        Dictionary representing the LENA file structure.
    Output:
        Mirror directory structure
        .tok file for each .its file
        
    """
    def __init__(self,dirDictIn):
        self.dirDict = dirDictIn
        #print 'Tokenize object created'
       
    
    def makeDirStr(self):
        """
        Create mirror directory structure at Const.LOC_OUT
        """
        
        errCode = os.system('mkdir ' + Const.LOC_OUT)
        if errCode > 0:
            print 'Problem creating ' + Const.LOC_OUT + 'in makeDirStr'
            sys.exit()

        for family in self.dirDict.keys():
            arg = Const.LOC_OUT + family
            errCode = os.system('mkdir ' + arg)
            if errCode > 0:
                print 'Problem creating ' + arg + 'in makeDirStr'
                sys.exit()
                
            months = self.dirDict[family]
            for month in months:
                arg = Const.LOC_OUT + family + '/' + month
                errCode = os.system('mkdir ' + arg)
                if errCode > 0:
                    print 'Problem creating ' + arg
                    sys.exit()
        
    #copy its files from the server to the mirror directory structure on the local machine
    def copyItsFiles(self):
        """
        Copy .its files from LENA to mirror
        """
        for family in self.dirDict.keys():
            months = self.dirDict[family]
            for month in months:
                pathToMM = Const.LOC_INP + family + '/' + month 
                files = os.listdir(pathToMM)
                for file in files:
                    fileLst = file.split('.')
                    #copy only its files
                    if len(fileLst) == 2: #pass over folders in the subdir
                        if fileLst[1] == 'its':
                            itsFile = '.'.join(fileLst)
                            src = pathToMM + '/' + itsFile
                            dest = Const.LOC_OUT + family + '/' + month + '/'
                            errCode = os.system('cp ' + src + ' ' + dest)
                            if errCode > 0:
                                print 'Problem copying its files in copyItsFiles'
                                sys.exit()

    def extractSpkrInfo(self, descDict):
        """
        Traverse the mirror file system using the file system dictionary
        Tokenize each .its file
        Parameters
            descDict: dictionary describing the file system
        """
        for family in self.dirDict.keys():
            months = self.dirDict[family]
            for month in months:
                arg0 = 'ls ' + Const.LOC_OUT + family + '/' + month + '/' + '*.' + 'its'
                itsFileName = str(subprocess.check_output(arg0, shell=True))
                itsFileName = itsFileName.rstrip()
                self.tokenizeItsFile(itsFileName,family,descDict)
        print 'Speaker information extracted'

    def tokenizeItsFile(self,itsFileName, family, descDict):
        """
        Extract speaker information from .its file
        Write speaker information to a temporary file
        Parameters
            family: family key to dictionary
            descDict: dictionary containing file system description
        """
        itsFileNameTok = itsFileName + Const.ITSTYPE
        itsLst = self.lstIze(itsFileName)
        tokOut = open(itsFileNameTok, 'w')
        famDev = self.getFamilyDev(descDict, family) 
        
        #write family identifier information (HH or TD)
        famDesc = family + ' ' + self.getFamilyDev(descDict,family) + '\n' 
        tokOut.write(famDesc)
        self.writeId(itsLst,tokOut)
        self.writeAgeGender(itsLst,tokOut)
        self.writeSpeakers(itsLst,tokOut)
        tokOut.close()
        
    def getFamilyDev(self,descDict,family):
        """
        Return TD family type for code found in dictionary
        Parameters
            descDict: dictionary describing file system
            family: dictionary key
        """
        famDev = descDict[family]
        if famDev == '0':
            return 'TD'
        if famDev == '1':
            return 'HH'
        
                
    def lstIze(self,itsFileName):
        """
        Transform an .its file into a list, each line being an item in the list
        Parameters:
            Name and location of an .its file
        """
        fin = open(itsFileName, 'r')
        itsStr = fin.read()
        itsLst = itsStr.split('\n')
        return itsLst
        
    def writeId(self,itsLst, tokOut):
        """
        Write the file id found in the .its file to the temporary token file
        Parameters:
            itsLst: List version of an itsFile
            tokOut: name and location of the token file
        """
        for item in itsLst:
            found = item.find('<ITS fileName=')
            if found != Const.NOTFOUND:
                tokOut.write(item + '\n')
                break
        if found == Const.NOTFOUND:
            tokOut.write("No ID in ITS file\n")

    def writeSpeakers(self,itsLst,tokOut):
        """
        Look for and write speaker information (male adult near (MAN) etc.)
        Parameters:
            itsLst: List version of an itsFile
            tokOut: name and location of the token file
        """
        for item in itsLst:
            pos = item.find('<Segment spkr=')
            if pos > -1:
                strOut = self.tokenize(item)
                if strOut != "":
                    tokOut.write(strOut + '\n')

    def writeAgeGender(self,itsLst, tokOut):
        """
        Look for and write age and gender information 
        Parameters:
            itsLst: List version of an itsFile
            tokOut: name and location of the token file
        """
        for item in itsLst:
            found = item.find('<ChildInfo algorithmAge')
            if found != Const.NOTFOUND:
                age, gender = self.getAgeGender(item)
                out = age + ' ' + gender
                tokOut.write(out + '\n')
                break
        if found == Const.NOTFOUND:
            tokOut.write("No ID in ITS file\n")

    def getAgeGender(self,aline):
        """
        Return age and gender information using regex
        Parameters:
            aline: item in the list representing a line in the .its file
        """
        linLst = aline.split()
        #linLst looks like: <ChildInfo algorithmAge="P33M" gender="F"/>
        
        agePart = linLst[1]
        age = re.search('[0-9]+',agePart)
        genderPart = linLst[2]
        gender = re.search('F|M',genderPart)
        return age.group(0), gender.group()
        
                    
    def tokenize(self,aline):
        """
        Return speaker information if line contains it else return the empty
        string
        """
        linLst = aline.split()
        if linLst[1] == 'spkr="MAN"' or linLst[1] == 'spkr="FAN"' or linLst[1] == 'spkr="CHN"':
            return " ".join(linLst)
        else:
            return ""

