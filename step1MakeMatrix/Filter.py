
import subprocess
import sys
import imp
import os
from Const import *

class Filter:
    """
    Permits the user to examine only a part of the LENA files.  The filters
    are limited to age range and gender
    Extracts only the age and gender of children we want to work with.
    These become a new dictionary.

    Input: file system dictionary, age and gender-related parameters
    Output: file representing the file system dictionary but filterd as
    as described above.
    """
    
    def __init__(self,dirsDict, lowAge,hiAge,gender):
        """
        Filter the LENA file structure by age and gender

        Parameters:
            lowAge: starting age in months
            hiAge: ending age in months
            gender: child gender
        """

        self.path = Const.LOC_OUT

        matLst = []
        for family in dirsDict.keys():
            toRemove = []
            months = dirsDict[family]
            for month in months:
                arg = 'ls ' + self.path + family + '/' + month + '/' + '*.' + 'mat'
                matFile = str(subprocess.check_output(arg, shell=True))
                matFile = matFile.rstrip()
                matLst = self.lstIze(matFile)
                if self.removeEpisode(matLst,lowAge,hiAge,gender):
                    toRemove.append(month)
            for month in toRemove:
                dirsDict[family].remove(month)
        
        newDict = {key:dirsDict[key] for key in dirsDict if dirsDict[key] != []}
        print "Dictionary of matrices has been filtered for age and gender"    
        self.writeDict(newDict)
       

    
    def lstIze(self,matFile):
        fin = open(matFile, 'r')
        matStr = fin.read()
        matStr = matStr.rstrip()
        matLst = matStr.split('\n')
        fin.close()
        return matLst

        
    def removeEpisode(self, matLst,lowAge,hiAge,gender):
        """
        Return true if data for this conversation passes the filter, false
        otherwise.

        Parameters:
            matLst: tokenized version of the .its file.  It contains the gender
                    and age of the child
            lowAge: Lowest age wanted in months
            hiAge: Highest age wanted in months
            gender: gender of child (M or F or MF)
        """
        conv = matLst[0].split()
        if conv[4] == gender or gender == 'MF':
            age = int(conv[3])
            if age >= int(lowAge) and age <= int(hiAge):
                return False
        return True

    def writeDict(self, dirsDict):
        """
        Write the dictionary from memory to a file

        Parameters:
            dirsDict: dictionary in RAM
        """

        #remove family ids without valid months from dirsDict        
        newDict = {key:dirsDict[key] for key in dirsDict if dirsDict[key] != []}
    
        #errCode = os.system('mkdir ' + Const.LOC_UTIL)
        
        arg = Const.LOC_UTIL + Const.DICTFILE
        fout = open(arg, 'w')
        fout.write(str(dirsDict))
        fout.close()
        print 'File structure dictionary written to a file'

    
