import subprocess
import sys
from Const import *
from CleanUp import *
import sys
import re
from Const import *
class CreateMatrix:
    """
    Create matrices from the speaker information extracted from .its files
    These matrices will contain all of the information needed to do f0
    extraction. Each recording session is represented by a matrix.  Each
    line within the matrix represents a a conversation, where a conversation
    is a speech interaction involving an adult and a child.  Ultimately, each
    conversation will be extracted from the corresponding .wav file
    Matrices will have these implicit column labels:
        Family
        HearingStatus
        ITSFileID
        AgeOfChild
        SexofChild
        Speaker
        StartTime
        StopTime
        AdjacencyStatus
        sourceWavFileID,
        targFileID
    Where:
        Family is family identifier AM28, BH35, etc
        HearingStatus is TD or HH
        ITS file id is the name of the its file where all information comes
            from, e.g., 20100818_110654_003541
        AgeOfChild in months
        SexOfChild is M or F
        Speaker: FAN/MAN/CHN
        StartTime/StopTime are the start and stop times of a particular
            conversation
        Adjacency is true if an adult directly precedes or follows a child (CHN)
            An adult (FAN/MAN) is either adacent or non-adjacent (NONA)
            An adjacent adult is pre-adjacent (PREA) or post-adjacent (PSTA)
            A child is CHLD
        sourceWavFileID is the full path plus file name to the wave file
            containing data described in each matrix
        targFileID is the sub wav file containing the conversation described
            for each row of the matrix

    Each recording session is represented by a matrix.  Each line within the
    represents a a conversation, where a conversation is a speech interaction
    involving an adult and a child.

    Input
        Dictionary representing LENA file structure
    Output
        Create and save matrix files described above.
    """
    def __init__(self,dirDictIn):
        """
        Create a global dictionary from the parameter
        Parameter:
            Dictionary describing mirror file structure
        """
        self.dirDict = dirDictIn
        print 'CreateMatrix object created'

    def makeMatrices(self):
        """
        Make the matrices described above
        """
        print 'Creating Matrix Files in Mirror File System ...'
        dirDictKeys = self.dirDict.keys()
        for family in dirDictKeys:
            famValues = self.dirDict[family]
            for month in famValues:
                arg0 = 'ls ' + Const.LOC_OUT + family + '/' + month + '/' + '*.' + 'its' + Const.ITSTYPE
                #this is the tokenized file created from the ITS file
                
                spkrFile = str(subprocess.check_output(arg0, shell=True))
                spkrFile = spkrFile.rstrip()
                srcPath = Const.LOC_INP + family + '/' + month + '/'
                srcPath = srcPath.rstrip()
                targPath = Const.LOC_OUT + family + '/' + month + '/'
                targPath = targPath.rstrip()

                #a matrix of speaker info from each its file.
                #At this point it does not include adjacency info
                matrixLst = self.makeEachMatrix(spkrFile)

                #add adjacency information
                matrixLst = self.determineAdj(matrixLst)

                #add wav file name for each speaker
                #this is a wav file extracted from the main wav file
                #for this recording session. It holds sounds from the
                #start time to stop time for each speaker.
                matrixLst = self.addWavFileInfo(matrixLst,srcPath,targPath,spkrFile)
                self.writeMatrixFile(matrixLst,spkrFile)
            
                #delete temporary files
                tokFileLst = arg0.split('ls ')
                errCode = os.system('rm ' + tokFileLst[1])
                if errCode > 0:
                    print 'Problem removing temporary token files'
                    sys.exit()
        print 'Matrix files created in mirror file system'     
        print 'Temporary token files removed'

    def removeIts(self):
        """
        Delete all .its files from the mirror file system
        """
        dirDictKeys = self.dirDict.keys()
        for family in dirDictKeys:
            famValues = self.dirDict[family]
            for month in famValues:
                arg0 = 'ls ' + Const.LOC_OUT + family + '/' + month + '/' + '*.' + 'its'
                itsFile = str(subprocess.check_output(arg0, shell=True))
                itsFile = itsFile.rstrip()
                errCode = os.system('rm ' + itsFile)
                if errCode > 0:
                    print 'Problem removing its files'
                    sys.exit()
        print "its files removed from mirror file system"
        print "Matrix Files with Speaker Parameters Stored in Mirror File System"
                
    def addWavFileInfo(self,matrixLst,srcPath,targPath,spkrFile):
        """
        Add .wav file info for each speaker.
        Parameters:
            matrixLst: matrix created from .its file
            srcPath: path to where .wav file is found in LENA system
            targPath: path to where .wav file piece extracted from .wav file
                found in mirror system
            spkrFile: name of the token file representation of the .its file. 
        """
        spkrFileLst = spkrFile.split('/')
        spkrFile = spkrFileLst[-1]
        spkrFileLst = spkrFile.split('.its.tok')
        spkrFile = spkrFileLst[0]
        for i in range(len(matrixLst)):
            sourceFile = srcPath + spkrFile + '.wav '
            targFile = targPath + spkrFile + '_' + str(i) + '.wav'
            matrixLst[i].append(sourceFile)
            matrixLst[i].append(targFile)
        return matrixLst

        
    def writeMatrixFile(self,finalMatLst,spkrFile):
        """
        Create a file from the internal list of lines
        Parameters:
            finalMatLst: matrix of lines representing an .its file
            spkrFile: tokenized verions of the .its files
        """
        #listized version of path to and name of token file
        matFileLst = spkrFile.split('.')
        #create the name of matrix file representing a conversation from the token file
        matFile = matFileLst[0] + Const.MAT
        fout = open(matFile,'w')
        for item in finalMatLst:
            newItem = ' '.join(item)
            fout.write(newItem + '\n')
        fout.close()

    def makeEachMatrix(self,spkrFile):
        """
        Return list of conversation data for each recording session.  Each line in the
            list represents a conversation 
        Parameters:
            spkrFile: tokeninzed file representing .its file for each recording session
            
        """
        outLineLst= []
        cnt = 0
        fin = open(spkrFile,'r')
        finLst = fin.readlines()
        prefix = self.getFirstThreeLines(finLst) #containing file id, family id, hearing status, age of child, gender of child
        prefix = prefix.rstrip()
        for i in range(3,len(finLst),1):
            line = finLst[i]
            outLine = self.ConstructLine(line,prefix)
            outLineLst.append(outLine)
        return outLineLst

    def getFirstThreeLines(self,finLst):
        """
        Return a string containing identification data from the first three
        lines of the token file--file id, family id, hearing status, age and gender of child
        Parameters:
            finList: listized version of the tokenized representation of the .its file

        """
        #identifier information is found in the first three lines
        outLine = ''
        for i in range(3):
            idInfo = finLst[i].split()
            if i == 0:
                outLine = outLine + idInfo[0] + ' ' + idInfo[1] + ' '
            if i == 1:
                lst = idInfo[1].split('"')
                outLine = outLine + lst[1]
            if i == 2:
                outLine = outLine + ' ' + finLst[i]
        return outLine


    def ConstructLine(self,line,prefix):
        """
        Return a string with all data representing a single conversation.  This will become a line in the matrix file representing
            a single recording session.  The technique is to start at the fourth line and search the entire tokenized file.  Lines
            in the tokenized file contain speaker information.  The task here is to get it in a more useable format.
        Parameters:
            line: line with speaker information from tokenized file
            prefix: session identification information from tokenized version of its file
        """

        #speaker is CHN, FAN, MAN
        spkr = re.search(Const.SPKR,line)

        startTime = re.search('startTime="PT[0-9]+.[0-9]+S"',line)
        startTime = re.search('[0-9]+.[0-9]+',startTime.group(0))
        
        endTime = re.search('endTime="PT[0-9]+.[0-9]+S"',line)
        endTime = re.search('[0-9]+.[0-9]+',endTime.group(0))

        outLine = prefix + ' ' + spkr.group(0) + ' ' + startTime.group(0) + ' ' + endTime.group(0)
        return outLine

    
    def determineAdj(self,matrix):
        """
        Return matrix of conversation data extracted from the .its file for single session with
            adjacency information having been aded. Adjacency is true if an adult directly precedes or follows a CHILD
            An adult (FAN/MAN) is either adacent or non-adjacent.  A CHILD is n/a.  The idea--in all cases except the
            special cases of the first and last lines--is to pass three lines to a function.  That function will determine
            the adjacency status of the speaker in the current line.  There are multiple possibilities, all documented in
            the functions recordAdj, recordAdjFirst, recordAdjLast. 
        Parameters:
            matrix: list of strings, each string representing one conversation.  The list is the tokenized representation of the .its file
        """
        newMatrix = []
       
        for i in range(len(matrix)):
            if i == 0:
                cur = matrix[i].split()
                post = matrix[i+1].split()
                cur = self.recordAdjFirst(cur,post) #deal with first line
            else:
              if i == len(matrix) - 1:
                prev = matrix[i-1].split()
                cur = matrix[i].split()
                cur = self.recordAdjLast(prev,cur) #deal with last line
              else:
                prev = matrix[i-1].split()
                cur = matrix[i].split()
                post = matrix[i+1].split()
                cur = self.recordAdj(prev,cur,post) #deal with all other lines
            newMatrix.append(cur)
        return newMatrix
            

    def recordAdj(self,prevLn,curLn,postLn):
        """
        Return current line from the matrix with adjacency status appended
        Parameters:
            prevLn: the previous line in the matrix
            curLn: the current line in the matrix
            postLn: the next line in the matrix
        """
        
        #speaker is at index 5
        prev = prevLn[5]
        cur = curLn[5]
        post =  postLn[5]
        if cur in Const.CHILD:
            curLn.append(Const.NOT_APPL)
            return curLn

        if prev in Const.ADULT and post in Const.ADULT:
            curLn.append(Const.NON_ADJ)
            return curLn

        if prev in Const.ADULT and post in Const.CHILD:
            curLn.append(Const.PRE_ADJ)
            return curLn

        if prev in Const.CHILD and post in Const.ADULT:
            curLn.append(Const.POST_ADJ)
            return curLn

        if prev in Const.CHILD and post in Const.CHILD:
            curLn.append(Const.BOTH)
            return curLn
            
    def recordAdjFirst(self,curLn,postLn):
        """
        Return current line from the matrix with adjacency status appended. Deals with special case
            of the first line in the matrix which has no previous line (i.e., no previous speaker)
        Parameters:
            curLn: the current line in the matrix
            postLn: the next line in the matrix
        """

        #speaker is at index 5
        cur = curLn[5]
        post = postLn[5]

        if cur in Const.CHILD:
            curLn.append(Const.NOT_APPL)
            return curLn

        if  post in Const.ADULT:
            curLn.append(Const.NON_ADJ)
            return curLn

        if post in Const.CHILD:
            curLn.append(Const.PRE_ADJ)
            return curLn

    #special case of last speaker who has no following speaker
    def recordAdjLast(self,prevLn,curLn):
        """
        Return current line from the matrix with adjacency status appended. Deals with special case
            of the last line in the matrix which has no post line (i.e., no following speaker)
        Parameters:
            prevLn: the previous line in the matrix
            curLn: the current line in the matrix
        """

        #speaker is at index 5 
        prev = prevLn[5]
        cur = curLn[5]

        if cur in Const.CHILD:
            curLn.append(Const.NOT_APPL)
            return curLn

        if prev in Const.ADULT:
            curLn.append(Const.NON_ADJ)
            return curLn

        if prev in Const.CHILD:
            curLn.append(Const.POST_ADJ)
            return curLn


       
