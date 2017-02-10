
import subprocess
import sys
import wave
from Const2 import *
import imp
import os

CO = imp.load_source('Const.py', Const2.STEP1 + 'Const.py')


'''
Using the dictionary of the file system, reads the .mat file in each folder
of the mirror file system. Extracts all conversations from the main .wav file
found in the same directory using information found in the .mat file.  Writes
these conversations to the same directory using the naming conventions
found in .mat

Input: file containing dictionary that represents the file system
Output: file containing names of all conversation files and the conversation
files themselves.
'''

class ExtractConv:
    """
    This class extracts distinct conversations from each long recording session.
    A conversation here is any sequence in which an adult is followed by a child
    or vice-versa. The start and stop times are stored in the .its files.
    The extractions are handled using the Python wave package.  The extracted
    conversations are stored as .wav files in the same directory where
    the tokenized .its files--i.e., the matrix files--are stored.
    """
    
    def __init__(self):
        
        #get stored dictionary describing file system
        fin = open(CO.Const.LOC_UTIL + CO.Const.DICTFILE, 'r')
        self.dirDict = eval(fin.read())
        
        fin.close()
       
        self.pathIn = CO.Const.LOC_INP
        self.pathOut = CO.Const.LOC_OUT

        #Delete lenaWav if its exists
        errCode = os.system('ls ' + Const2.LENA_WAV)
        if errCode == 0: #directory exists
            os.system('rm -r ' + Const2.LENA_WAV)
            print 'Directory with wave file names from previous runs deleted'
        
        #make new directory for names of wavefiles
        errCode = os.system('mkdir ' + Const2.LENA_WAV)
        if errCode > 0:
            print 'problem creating ' + Const2.WAV_FILE + ' in ExtractConv'
            sys.exit()

        
        print 'Dictionary describing file system is available'

    def extractFiles(self):
        """
        Iterate through the dictionary description of the file system extracting
        conversations.
        """
        print 'Extracting Conversations .................'
        fout = open(Const2.LENA_WAV + '/' + Const2.WAV_FILE, 'w')
        for family in self.dirDict.keys():
            months = self.dirDict[family]
            for month in months:
                arg = 'ls ' + self.pathOut + family + '/' + month + '/' + '*.' + 'mat'
                matFile = str(subprocess.check_output(arg, shell=True))
                matFile = matFile.rstrip()
                matLst = self.lstIze(matFile)
                print 'Working on ' + family + ' ' + month
                self.processFiles(matLst,fout)
        fout.close()
        
    def lstIze(self,matFile):
        """
        Return a list version of the matrix file for a particular recording
        session.  Each entry in the list represents a distinct conversation.

        Parameters:
            matFile: is the tokenized version of the .its file. 
        """
        fin = open(matFile, 'r')
        matStr = fin.read()
        matStr = matStr.rstrip()
        matLst = matStr.split('\n')
        fin.close()
        return matLst

    def processFiles(self,matLst,fout):
        """
        For each convesation, represented in the matrix, invoke a function that
        extracts that chunk from the original wave file, and write the name
        of the resulting .wav file to an output file that stores the names of
        all conversation files. 

        Parameters:
            matList: listized version of the matrix file
            fout: pointer to a file that stores the names of all conversation
            files that have been created.  
        """
        
        for conv in matLst:  #conv is an individual conversation
            conv = conv.split() #string file line to list
            self.processConv(conv)
            fout.write(conv[10] + '\n') #file name is stored in pos. 10
    
    def processConv(self,conv):
        """
        Extract a segment from the session .wav file.  This is done using
        Python's wave package and parameters from each line in the listized
        version of the matrix file.

        Parameters:
            conv: a line from the matrix file that holds data associated with
            a conversation
        """
        
        start = float(conv[6]) #start time of conversation
        stop = float(conv[7])#stop time
    
        srcWav = conv[9].strip()    #original lena-recorded wave file
        trgWav = conv[10].strip()    #single conversation bounded by start & stop
        fin = wave.open(srcWav,'r')
        fout = wave.open(trgWav,'w')
        
        fout.setparams(fin.getparams()) #get characteristics of output file
        rate = float(fin.getframerate())
        width = fin.getsampwidth()

        #move start back and end forward a fixed number of frames
        bufAmt = int(float(Const2.BUFFER)/1000 * rate)

        start = int(rate * start)
        stop = int(rate * stop)

        #don't back up too far
        if (start - bufAmt >= 0):
            start = start - bufAmt
        #don't advance too far
        if (stop + bufAmt <= fin.getnframes()):
            stop = stop + bufAmt

        numFrames = stop - start

        fin.setpos(start)

        inFrame = fin.readframes(numFrames)
        fout.writeframes(inFrame)
        
        fin.close()
        fout.close()

    

    
