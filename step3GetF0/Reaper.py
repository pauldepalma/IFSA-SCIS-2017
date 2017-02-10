
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

class Reaper:
    """
    Invokes Google's speech extractor, Reaper, written by Dave Talkin
    Available at: https://github.com/google/REAPER
    
    Input:
    
    Output:
        
    """
    
    def __init__(self,errFile):
        """
        
        """
        self.errFile = errFile
    
    def processConv(self,conv):
        """
        Uses Google's Reaper f0 extractor.
        Extract f0 for each conversation file. We are interested only CD speech,
        i.e., speech from males/females who are either pre/post adjacent.
        Each line in the .mat file is a list, components of which are used in the f0 computation
        The indices are the positions in the list.  pgm is the f0 extraction program.

        
        """
        #wave file is the 10th entry on conv

        cmd = Const3.REAPER + ' -i ' + conv[10] + ' -f ' + 'tmpF0.txt' + ' -a'
        #the Python way to execute a file
        out_cde = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        #redirect stderr to a log file
        if out_cde.stdout.read() != '':
            cde = out_cde.stdout.read()
            msg = conv[10] + ' ' + cde + '\n'
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

            

    def file_to_list(self, f0File, family, recording_code):
        """
        Return list created from the output of the f0 extractor plus other codes

        Parameters:
            f0File: output of f0 extractor
            family: family code
            recording_code: name of the conversation file
        """
        fin = open(f0File)
        file_lst = fin.readlines()
        fin.close()
        file_lst = [line.rstrip() for line in file_lst]
        file_lst = [line.split('\t') for line in file_lst]
        f0 = []
        #bypass header information unvoiced segments
        for i in range(7,len(file_lst)):
            line = file_lst[i]
            line = line[0]
            line = line.split()
            if line[1] == '1':
                f0.append(float(line[2]))
        if len(f0) > 0:
            f0_mean = np.nanmean(f0)
        else:
            f0_mean = np.nan
        f0_lst = [family, recording_code, f0_mean]
        return f0_lst                       
              
            
        
        

    
