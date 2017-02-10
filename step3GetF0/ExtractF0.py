
import subprocess
from subprocess import Popen, PIPE, STDOUT
import sys
from Const3 import *
import imp
import os
import time
from Talkin1 import *
from Reaper import *

CO = imp.load_source('Const.py', Const3.STEP1 + 'Const.py')

class ExtractF0:
    """
    Uses Dave Talkin's get_f0 to extract mean f0 for each of the conversations.
    Const3.py contains a constant (GETF0DIR) that gives the location the f0
    extractor.  Other f0 extractors could be used by changing this parameter
    and taking care with the output of course

    Input:
        File containing dictionary describing file system
    Output:
        Up to eight files stored in csv format
            FHH-a (female adult talking to HH child)
            FHH-na (female adult, HH child, but not adjacent)
            FTD-a (female adult, talking to traditionally developing child)
            FTD-na (female adult, TD child, but not adjacent)
            Analogues for male adults
        Log and error files whose location is described in Const3.py
    """
    
    def __init__(self):
        """
        Retrieve stored dictionary
        Delete previous F0 repositories if they exist.
        Create 8 lists, one for each of the output files described above
        """
    
        #get stored dictionary describing file system
        fin = open(CO.Const.LOC_UTIL + CO.Const.DICTFILE, 'r')
        self.dirDict = eval(fin.read())
        fin.close()
       
        self.pathIn = CO.Const.LOC_INP
        self.pathOut = CO.Const.LOC_OUT
        self.pathRepos = Const3.F0REPOS

        #Delete f0 repository if its exists
        errCode = os.system('ls ' + self.pathRepos)
        if errCode == 0: #directory exists
            os.system('rm -r ' + self.pathRepos)
            print 'files holding previously saved f0 files deleted'
        else:
            print 'first execution: no previously saved f0 files'

        #make new directory for repos
        errCode = os.system('mkdir ' + Const3.F0REPOS)
        if errCode > 0:
            print 'problem creating ' + Const3.F0REPOS
            sys.exit()
        
        #log files
        self.logFile = open(Const3.F0LOG, 'w')
        self.errFile = open(Const3.F0ERR, 'w')

        self.numCons = 0
        self.numSessions = 0
        self.numFams = 0
        self.numFamsProc = 0
        
    def countConv(self):
        """
        Count the total conversations. 
        A conversation is what was extracted from the wav files in step 2.  It is
        an exchange between an adult and a child.  There are many of these
        very short conversations per wav file.
        """
        for family in self.dirDict.keys():
            self.numFams = self.numFams + 1
            months = self.dirDict[family]
            for month in months:
                arg = 'ls ' + self.pathOut + family + '/' + month + '/' + '*.' + 'mat'
                matFile = str(subprocess.check_output(arg, shell=True))
                matFile = matFile.rstrip()
                matLst = self.lstIze(matFile)
                self.numCons = self.numCons + len(matLst)
                self.numSessions = self.numSessions + 1
        fams = 'Processing ' + str(self.numFams) + ' ' + 'Families'
        sess = 'Processing ' + str(self.numSessions) + ' ' + 'Recording Sessions'
        convs = 'Processing ' + str(self.numCons) + ' ' + 'Conversations In Total'
        self.logFile.write(fams + '\n')
        self.logFile.write(convs + '\n')
        print(fams)
        print sess
        print (convs)
        
        
    def accumF0(self,extractor):
        """
        Iterate through the dictionary, making a list of all conversations
        per family by month.
        Extract mean f0 for each conversation
    
        See class CreateMatrix.recordAdj(self,prev,cur,post)
        We've distinguished between pre-adjacent, post-adjacent, and pre  and
        post adjacent.  For the present, however, all of these are collapsed into
        adjacent.  This gives four categories for adult speakers
        
        allF0 is a list of list holding f0 data.  Columns hold the following values:
        Adjacent
        0 : male, TD family
        1 : male, HH family
        3 : female, TD family
        4 : female, TD family
        Non-Adjacent
        0 : male, TD family
        1 : male, HH family
        3 : female, TD family
        4 : female, TD family
        """
        for family in self.dirDict.keys():
            #The following list is to be written to disk after each family is processed
            allF0 = [[] for i in range(8)]
            months = self.dirDict[family]
            print 'Processing Family: ' + family
            print 'Number of Sessions: ' + str(len(months))
            numMonthsProc = 0
            for month in months:
                #make a list of all conversations for each family by month
                arg = 'ls ' + self.pathOut + family + '/' + month + '/' + '*.' + 'mat'
                matFile = str(subprocess.check_output(arg, shell=True))
                matFile = matFile.rstrip()
                matLst = self.lstIze(matFile)
                fam = 'Processing Session from Family ' + family + ' recorded: ' + month
                numConvs = 'f0 from ' + str(len(matLst)) + ' Conversations to Process...' + '\n'
                self.logFile.write(fam)
                self.logFile.write(numConvs)
                print fam
                print numConvs
                #process the conversations--i.e., extract f0
                allF0 = self.processMatrix(matLst,extractor,allF0)
                numMonthsProc = numMonthsProc + 1
                print str(len(months) - numMonthsProc) + ' sessions to go for family ' + family + '\n'
            self.numFamsProc = self.numFamsProc + 1
            self.saveData(allF0) #save data for a family to disk.
            print 'Finished Family '  + family
            print str(self.numFams - self.numFamsProc) + ' of ' + str(self.numFams) + ' families to go\n'
        self.logFile.close()
                       
    def lstIze(self,matFile):
        """
        Return a list created from a matrix file

        Parameters:
            matFile: holds tokenized information gotten from .its files
        """
        fin = open(matFile, 'r')
        matStr = fin.read()
        matStr = matStr.rstrip()
        matLst = matStr.split('\n')
        fin.close()
        return matLst

    def processMatrix(self,matLst,extractor,allF0):
        """
        Iterate through the listized version of the matrix, extracting
        f0 for each conversation
        Writes status for each conversation to a log file.


        Parameters:
            matList: tokenized and listized version of information extracted from
            .its files
        """
        ctr = 0
        for conv in matLst:  #conv is an individual conversation, i.e., 1 line in the .mat file
            conv = conv.split() #string file line to list

            if (extractor == Const3.EXT):
                extF0 = Talkin1(self.errFile)
            else:
                if (extractor == Const3.EXT1):
                    extF0 = Reaper(self.errFile)
                else:
                    print ("unknown F0 Extractor")
                    sys.exit()
            #contains family, recording code, mean f0
            ctr = ctr + 1
            #skip a certain number of recordings to speed things up
            skip = int(Const3.SKIP)
            if (ctr % skip == 0):
                f0_lst = extF0.processConv(conv)
                allF0 = self.addToGlobal(allF0, f0_lst, conv[5], conv[8], conv[1]) #f0 values, adult, pre/post/non, TD/HH
                self.logFile.write(conv[10] + ' OK' + '\n')
        return allF0

    def addToGlobal(self,allF0, f0_lst, sex, adjacency, status):
        """
        Add data for an individual conversation to the global lists created in the constructor.
        There are eight such lists all described in the constructor.  Their indices are as
        follows:
    
        Adjacent
        0 : male, TD family
        1 : male, HH family
        2 : female, TD family
        3 : female, HH family
        Non-Adjacent
        4 : male, TD family
        5 : male, HH family
        6 : female, TD family
        7 : female, HH family

        Parameters:
            f0_lst: output of the extractro plus identifying data
            sex: gender of child
            adjacency: does the adult speak before the child (pre-adj) or after (post-adj)
            status: hearing status
        """

        if adjacency == CO.Const.PRE_ADJ or adjacency == CO.Const.POST_ADJ:
            if sex == 'MAN' and status == 'TD':
                allF0[0].append(f0_lst)
                #allF0[0] = allF0[0] + f0_lst
            if sex == 'MAN' and status == 'HH':
                allF0[1].append(f0_lst)
                #allF0[1] = allF0[1] + f0_lst
            if sex == 'FAN' and status == 'TD':
                allF0[2].append(f0_lst)
                #allF0[2] = allF0[2] + f0_lst
            if sex == 'FAN' and status == 'HH':
                allF0[3].append(f0_lst)
                #allF0[2] = allF0[2] + f0_lst

        if adjacency == CO.Const.NON_ADJ:
            if sex == 'MAN' and status == 'TD':
                allF0[4].append(f0_lst)
                #allF0[4] = allF0[4] + f0_lst
            if sex == 'MAN' and status == 'HH':
                allF0[5].append(f0_lst)
                #allF0[5] = allF0[5] + f0_lst
            if sex == 'FAN' and status == 'TD':
                allF0[6].append(f0_lst)
                #allF0[6] = allF0[6] + f0_lst
            if sex == 'FAN' and status == 'HH':
                allF0[7].append(f0_lst)
                #allF0[7] = allF0[7] + f0_lst
        return allF0
        
    def saveData(self, allF0):
        """
        Write lists of f0 data to csv files.
        """
        for i in range(8):
            if len(allF0[i]) > 0:
                #print Const3.F0REPOS + Const3.F0_FILES[i]
                out = open(Const3.F0REPOS + Const3.F0_FILES[i], 'a')
                self.writeFile(allF0[i], out)
                out.close()
        print "Data for a family saved to f0 repositories"
    
    def writeFile(self,inLst, outFile):
        """
        Write item in the list to the appropriate file

        Parameters:processConv
            inLst: list containing f0 data
            outFile: csv file containing f0 data
        """
        last = len(inLst) - 1
        for i in range(len(inLst)):
            if (i < last):
                data = inLst[i] #tuple holding family id and f0
                fam_id = data[0] #family identifier
                recording_id = data[1]  #name of recording
                f0 = data[2] #f0 cmnputation
                out_str = str(fam_id) + ',' + str(recording_id) + ',' + str(f0) + '\n'
                outFile.write(out_str)
            
        
        
        
       
                    
                        
                        
                        
        
            
        
        

    
