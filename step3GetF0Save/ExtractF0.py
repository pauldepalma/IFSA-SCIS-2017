
import subprocess
from subprocess import Popen, PIPE, STDOUT
import sys
from Const3 import *
import imp
import os
import time
#print Const3.STEP1

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

        #keeps track of the number of families processed and the number to go
        self.numFams = 0
        self.numFamsProc = 0
        self.numCons = 0
        self.numSessions = 0
        self.ct = 0

        

        """
        See class CreateMatrix.recordAdj(self,prev,cur,post)
        We've distinguished between pre-adjacent, post-adjacent, and pre  and
        post adjacent.  For the present, however, all of these are collapsed into
        adjacent.  This gives four categories for adult speakers
        
        lists holding f0 data.  Columns hold the following values:
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
    
        self.allF0 = [[] for i in range(8)]
        
        #log files
        self.logFile = open(Const3.F0LOG, 'w')
        self.errFile = open(Const3.F0ERR, 'w')
        
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
        #seems to take about 9 to 10 minutes to extract f0 from all conversations in a recording session
        print 'Approximate Time Required: ' + str((10.0 * self.numSessions)/60.0) + ' hour(s)\n'
        
    def accumF0(self,extractor):
        """
        Iterate through the dictionary, making a list of all conversations
        per family by month.
        Extract mean f0 for each conversation
        """
        for family in self.dirDict.keys():
            months = self.dirDict[family]
            print 'Processing Family: ' + family
            print 'Number of Sessions: ' + str(len(months))
            for month in months:
                #make a list of all conversations for each family by month
                arg = 'ls ' + self.pathOut + family + '/' + month + '/' + '*.' + 'mat'
                matFile = str(subprocess.check_output(arg, shell=True))
                matFile = matFile.rstrip()
                matLst = self.lstIze(matFile)
                fam = 'Processing Family ' + family + ' recorded: ' + month
                numConvs = 'f0 from ' + str(len(matLst)) + ' Conversations to Process' + '\n'
                self.logFile.write(fam)
                self.logFile.write(numConvs)
                #process the conversations--i.e., extract f0
                self.processMatrix(matLst,extractor)
            self.numFamsProc = self.numFamsProc + 1
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

    def processMatrix(self,matLst,extractor):
        """
        Iterate through the listized version of the matrix, extracting
        f0 for each conversation
        Writes status for each conversation to a log file.

        Parameters:
            matList: tokenized and listized version of information extracted from
            .its files
        """
        num = 0
        for conv in matLst:  #conv is an individual conversation, i.e., 1 line in the .mat file
            conv = conv.split() #string file line to list

            if (extractor == Const3.EXT):
                self.processConv(conv)
            else:
                if (extractor == Const3.EXT1):
                    self.processConv1(conv)
                else:
                    print ("unknown F0 Extractor")
                    sys.exit()
            self.logFile.write(conv[10] + ' OK' + '\n')
            """
            if (num % 100 == 0):
                print str(num) + ' Conversations Processed'
            """
            num = num + 1
        self.logFile.write(str(num) + ' Conversations Processed' + 'saveData\n')


    
    def processConv(self,conv):
        """
        Uses Dave Talkin's original F0 Extractor.
        Extract f0 for each conversation file. We are interested only CD speech,
        i.e., speech from males/females who are either pre/post adjacent.
        Each line in the .mat file is a list, components of which are used in the f0 computation
        The indices are the positions in the list.  pgm is the f0 extraction program.

        Parameters:
            conv: an item from the listized version of the matrix file.  It is itself list,
            index to which are used in the extraction.
        """
        #open the f0 extractor
        pgm = Const3.GETF0DIR + Const3.GETF0

        #Use the proper parameter file for a man or a woman.  
        if conv[8] == CO.Const.POST_ADJ or conv[8] == CO.Const.PRE_ADJ or CO.Const.BOTH:
            if conv[5] == 'MAN':
                param = Const3.GETF0DIR + Const3.MALE
            else:
                if conv[5] == 'FAN':
                    param = Const3.GETF0DIR + Const3.FEM
                else:
                    param = 'NA'
        else:
            param = 'NA'
        wav = conv[10]
        if not(param == 'NA'):
            #execution string for f0 extraction.  Output is tmpF0.txt
            cmd = pgm + ' ' + param + ' ' + wav + ' ' + 'tmpF0.txt'
            #the Python way to execute a file
            out_cde = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            #redirect stderr to a log file
            if out_cde.stdout.read() != '':
                cde = out_cde.stdout.read()
                msg = wav + ' ' + cde + '\n'
                self.errFile.write(msg)
            #listize the output along with family and recording codes
            f0_lst = self.file_to_list('tmpF0.txt', conv[0], conv[2])

            #add this to the lists created in the constructor
            self.addToGlobal(f0_lst, conv[5], conv[8], conv[1]) #f0 values, adult, pre/post/non, TD/HH)

    def file_to_list(self,f0File, family, recording_code):
        """
        Return list created from the output of the f0 extractor plus other codes

        Parameters:
            f0File: output of f0 extractor
            family: family code
            recording_code: name of the conversation file
        """
        
        fin = open(f0File)
        file_lst = fin.readlines()
        #White space is unaccountably part of tmpF0.txt and causes failure. 
        #remove all trailing whitespace
        file_lst = [line.rstrip() for line in file_lst]
        #transform each line in the list into a list
        file_lst = [line.split('\t') for line in file_lst]

        #[1] is the index of f0 in f0File
        #store plus associated f0 in tuples within a list
        f0_lst = [(family,recording_code, line[1]) for line in file_lst if line[1] > '0.0']

        f0_lst = [(family,recording_code, line[1]) for line in file_lst if line[1] != '0.0']
        return f0_lst


    def addToGlobal(self,f0_lst, sex, adjacency, status):
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
        print len(f0_lst)   
        if adjacency == CO.Const.PRE_ADJ or adjacency == CO.Const.POST_ADJ:
            if sex == 'MAN' and status == 'TD':
                self.allF0[0] = self.allF0[0] + f0_lst
            if sex == 'MAN' and status == 'HH':
                self.allF0[1] = self.allF0[1] + f0_lst
            if sex == 'FAN' and status == 'TD':
                self.allF0[2] = self.allF0[2] + f0_lst
            if sex == 'FAN' and status == 'HH':
                self.allF0[3] = self.allF0[3] + f0_lst

        if adjacency == CO.Const.NON_ADJ:
            if sex == 'MAN' and status == 'TD':
                self.allF0[4] = self.allF0[4] + f0_lst
            if sex == 'MAN' and status == 'HH':
                self.allF0[5] = self.allF0[5] + f0_lst
            if sex == 'FAN' and status == 'TD':
                self.allF0[6] = self.allF0[6] + f0_lst
            if sex == 'FAN' and status == 'HH':
                self.allF0[7] = self.allF0[7] + f0_lst
        
    def saveData(self):
        """
        Write lists of f0 data to csv files.
        """
    
        errCode = os.system('ls ' + Const3.F0REPOS)
        if errCode == 0: #directory exists
            os.system('rm -r ' + Const3.F0REPOS)
            print 'Old F0 repositories deleted'

        #make new directory for repos
        errCode = os.system('mkdir ' + Const3.F0REPOS)
        if errCode > 0:
            print 'problem creating ' + Const3.F0REPOS
            sys.exit()

        for i in range(8):
            if len(self.allF0[i]) > 0:
                   out = open(Const3.F0REPOS + Const3.F0_FILES[i], 'w')
                   self.writeFile(self.allF0[i], out)
        print "Data saved to f0 repositories"
    
    def writeFile(self,inLst, outFile):
        """
        Write item in the list to the appropriate file

        Parameters:
            inLst: list containing f0 data
            outFile: csv file containing f0 data
        """
        last = len(inLst) - 1
        for i in range(len(inLst)):
            if (i < last):
                data = inLst[i] #tuple holding family id and f0
                fam_id = data[0] #family identifier
                recording_id = data[1]  #name of recording
                f0 = data[2] #f0 conputation
                outFile.write(fam_id + ',' + recording_id + ',' + f0 + '\n')
        outFile.close()
            
        
        
        
       
                    
                        
                        
                        
        
            
        
        

    
