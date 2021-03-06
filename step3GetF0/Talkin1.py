
import subprocess
from subprocess import Popen, PIPE, STDOUT
import sys
from Const3 import *
import imp
import os
import time
import numpy as np
#print Const3.STEP1

CO = imp.load_source('Const.py', Const3.STEP1 + 'Const.py')

class Talkin1:
    """
    Invokes Dave Talkin's speech extractor.  The details are described in:
    Talkin, D. (1995). Chap 14: A Robust Algorithm for Speech Tracking.  In
    Klein, W., Paliwal, K. (eds.), Speech Coding and Synthesis.  NY: Elsevier
    Science.

    https://github.com/dpwe/get_f0_snd
    
    Input:
    
    Output:
        
    """
    
    def __init__(self,errFile):
        """
        
        """
        self.errFile = errFile
    
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
            '''
            errCode = os.system('rm ' + 'tmpF0.txt')
            if errCode > 0:
                print 'Problem removing tmpF0.txt'
                sys.exit()
            '''
            return f0_lst

            

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

        f0 = [float(line[1]) for line in file_lst if (line[1] != '0.0')]
        if len(f0) > 0:
            f0_mean = np.nanmean(f0)
        else: #conversation was faulty.  Pass over
            f0_mean = np.nan
        f0_lst = [family, recording_code, f0_mean]
        return f0_lst
        


    
            
        
        
        
       
                    
                        
                        
                        
        
            
        
        

    
