import subprocess
import sys
import xlrd
import os
import re
from Const import *

class CleanUp:
    """
    A. Validate Data:
        1. Folders must be in format CCDD, where C is an alphabetic character
        and D is a digit.
        2. Sub-folders must be in format YYYY_MM
        3. Sub-folders must (at least) contain a .wav and a .its file
        4. Write all exceptions to an error file.

    B. Create dictionary based on the Lena directory structure
        1. Write this dictionary to a text file.
        2. Read and reconstruct the dictionary
        3. Example
            Suppose just under the top level LENA directory, we have
            directories PX78, AM28, AM29
            Suppose these directories have the following subdirectories:
            PX78 has 2010_12
            AM28 has 2010_12, 2011_01, 2011_02
            AM29 has 2010_12, 2011_01, 2011_02
            Then invoking makeDirsDict produces this dictionary:
            {'PX78': ['2010_04'],
             'AM28': ['2010_12', '2011_01', '2011_02'],
             'AM29: ['2010_12', '2011_01', '2011_02']}

    Input
        directory structure defined in file Const.LOC_INP
    Output
        1. Const.EXCEPTION containts names of folders in LENA system with
        formatting errors.
        2. dictionary described above.
        3. file version of dictionary stored in Const.LOC_OUT
        
    """
    def __init__(self):
        """
        Delete existing system
        Pass over directories in the LENA structure with invalid data
        Create dictionary of valid directories in the LENA directory structure
        """

        #Starting fresh, create new system
        self.fileSystemDict = {}
        self.familyDescDict = {}
        
        self.startFresh()
        print 'Previously Built Files Deleted'
        print 'lenaUtils folder created'

        fout = open(Const.EXCEPTION, 'w')
        dirsDict, self.familyDescDict = self.cleanFolderNames(fout)
        print 'Invalid Folder Names Passed Over '
        fout.write('\n')
        
        dirsDict = self.cleanSubFolderNames(dirsDict,fout)
        print 'Invalid Sub-folder Names Passed Over'
        fout.write('\n')
        
        self.fileSystemDict = self.cleanSubFolderContents(dirsDict,fout)
        print 'Sub-Folders With Invalid Its/Wav file names passed over'
        fout.write('\n')
        fout.close()

        #eliminate family names with all invalid data
        keys = self.fileSystemDict.keys()
        for item in keys:
            if self.fileSystemDict[item] == []:
                del self.fileSystemDict[item]
        
        print 'Dictionary of Valid File System Created'

    def getFileSystemDict(self):
        """
        Return class-wide copy of the file system dictionary
        """
        return self.fileSystemDict

    def getFamilyDescDict(self):
        """
        Return the class-wide copy of the family description dictionary.
        This dict holds family hearing status
        """
        return self.familyDescDict
        
    def startFresh(self):
        """
        Delete existing system
        """
        
        print 'Remove previously built lenaUtils and lenaMatrices'

        #Matrices are stored in a folder lenaMatrices defined in Const.LOC_OUT
        #Delete ../lenaMatrices if it exists
        print "Here are the families used in the last run of the system"
        errCode = os.system('ls ' + Const.LOC_OUT)
        if errCode == 0: #directory exists
            os.system('rm -r ' + Const.LOC_OUT)
            print 'matrices deleted'

        #Delete lenaUtils if its exists
        errCode = os.system('ls ' + Const.LOC_UTIL)
        if errCode == 0: #directory exists
            os.system('rm -r ' + Const.LOC_UTIL)
            print('lenaUtils deleted')
            
        #make new directory for utilities and error files
        errCode = os.system('mkdir ' + Const.LOC_UTIL)
        if errCode > 0:
            print 'problem creating ' + Const.LOC_UTIL + ' in CleanUp'
            sys.exit()

    def cleanFolderNames(self,fout):
        """
        Take the first step in creating a dictionary of the LENA.  See above.
        Write exceptions to error file, Const.EXCEPTIONS
        Return dictionary of file system described in point B of CleanUp,above
        Return dicionary description of families (family:hearingstatus)
        
        Parameters:
            fout: pointer to the exception file
        """
        #make a list of directories
        dirs = os.listdir(Const.LOC_INP)
        
        #keep only those with four characters of any kind (e.g., AM28)
        dirs1 = [item for item in dirs if len(item) == 4]
        
        #keep only those in the correct format
        dirs2 = re.findall(r"[A-Z]{2}[0-9]{2}"," ".join(dirs1))

        #pair up families with family descriptor (HH, TD)
        descDict = self.makeFamilyDescDict()

        #keep only those who appear in SubjectDatabase14.xlsx
        dirs3 = [family for family in dirs2 if family in descDict]         
        
        #turn the list into a dictionary with folder as key
        dirsDict = {folder:'' for folder in dirs3}


        #write invalid data to error file
        errLst = [item for item in dirs if item not in dirsDict]

        fout.write("NON-STANDARD STUFF IN TOP-LEVEL FOLDER\n")
        fout.write("OR FAMILY NAME NOT IN SubjectDatabase14.slsx\n") 
        for item in errLst:
            fout.write(item + '\n')
        return dirsDict, descDict
   
    def makeFamilyDescDict(self):
        """
        Read excel file holding family hearing status (Const.XLSX_FILE) using
        xlrd package
        Creates a dictionary using family as key and family descriptor as value
        For instance:
        AM28:HH
        PH78:TD
        """
        descDict = {}
        wb = xlrd.open_workbook(Const.XLSX_FILE)
        sh = wb.sheet_by_name(Const.SHEET)
        cur_row = 1
        while cur_row < sh.nrows:
            row = sh.row(cur_row)
            #myrow = ''
            #family id appears in the 9th col. of the spreadsheet
            val1 = str(sh.cell_value(cur_row,9))
            #HH value appears in the 41st col of the spreadsheet
            val2 = str(sh.cell_value(cur_row,41))
            val2 = val2.split('.')
            val2 = val2[0] #0/1 on the SS becomes '0.0' and '1.0'. But only
                           #the first character is necessary
            descDict[val1] = val2
            cur_row += 1

        #eliminate empty entry in dictionary
        keys = descDict.keys()
        for item in keys:
            if item == '':
                del descDict[item]
        return descDict


    def cleanSubFolderNames(self,dirsDict,fout):
        """
        Take second step in making a dictionary of all all valid folders.
        These have the format: CCDD, where C is an upper case letter, D is a digit.
        Write exceptions to error file

        Parameters:
            dirsDict: dictionary description of the LENA file system
            fout: pointer to exception file
        """
        
        folderLst = dirsDict.keys()
        
        dict = {folder:os.listdir(Const.LOC_INP + folder) for folder in folderLst}
        dict1 = {}
        fout.write('NON-STANDARD SUB-FOLDERS\n')
        for folder in folderLst:
            dict1[folder] = self.getGoodSubFolders(dict[folder],folder,fout)

        return dict1

    def getGoodSubFolders(self,folderLst,parent,fout):
        """
        Return list of subfolders in the proper format
        Write names of bad folders to error file

        Parameters:
            folderList: list of recording sessions linked to a particular family
            parent: family name
            fout: pointer to exception file
        """
        
        #must have 7 characters (2011_01)
        lst = [item for item in folderLst if len(item) == 7]
        
        #must be in this format
        lst1 = re.findall(r"[0-9]{4}_[0-9]{2}"," ".join(lst))
    
        #get the names of bad subfolders
        #write invalid data to error file
        errLst = [item for item in folderLst if item not in lst1]

        if len(errLst) > 0:
            errStr = parent + ' ' + " ".join(errLst)  
            fout.write(errStr + '\n')
        return lst1

    def cleanSubFolderContents(self,dirsDict,fout):
        """
        Return completed dictionary
        Write names of subfolders with invalid contents to error file

        Parameters:
            dirsDict: dictionary description of the LENA file system
            fout: pointer to exception file
        """
        folders = dirsDict.keys() #folder: e.g., AM28
        fout.write('SUBFOLDER CONTENTS ERROR\n')
        fout.write ('BOTH ITS AND WAV NOT PRESENT OR NAME OF ITS != NAME OF WAV\n')
        for folder in folders: #subfolder list: [2010_06, 2010_05]
            subFolderLst = [] #new subfolder list
            for subFolder in dirsDict[folder]: #subfolder: e.g., 2010_06 
                if (self.checkForFiles(folder,subFolder)):
                    subFolderLst.append(subFolder)
                else:
                    fout.write(str(folder) + ' ' + str(subFolder) + '\n')
            dirsDict[folder] = subFolderLst
        return dirsDict
            
                          
    def checkForFiles(self,folder,subFolder):
        """
        Return true if folder/subfolder contains both .its and .wav files
        Return false otherwise

        Parameters:
            folder: family name
            subFolder: recording session
        """
        localPath = Const.LOC_INP + folder + '/' + subFolder + '/'
        wavCt = 0
        itsCt = 0
        wavFile = ''
        itsFile = ''
        files = os.listdir(localPath)
        for file in files:
            if '.' in file:
                components = file.split('.')
                if components[1] == 'wav':
                    wavFile = components[0]
                    wavCt = wavCt + 1
                if components[1] == 'its':
                    itsFile = components[0]
                    itsCt = itsCt + 1
        if (wavCt == 1 and itsCt == 1 and wavFile == itsFile):
            return True
        else:
            return False
    
    def dictToMat(self):
        """
        Write dictionary of file system to Const.LOC_UTIL/Const.DICT_TO_MAT_FILE
        This file can be read in to a dictionary as needed in other classes
        """
        fout = open(Const.LOC_UTIL + Const.DICT_TO_MAT_FILE, 'w')
        for key in dirsDict.keys():
            mmLst = dirsDict[key]
            for mm in mmLst:
                fout.write(key + ' ' + mm + '\n')
        fout.close()
        print 'Matrix version of dictionary file system created'
        
        
 
   
