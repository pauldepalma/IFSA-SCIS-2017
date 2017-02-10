import sys
import os
from Const4 import *
import numpy as np
import imp

C = imp.load_source('Const3.py', Const4.STEP3 + 'Const3.py')

class Results:
    def __init__(self):
        """
        Uses numpy to compute the mean and standard deviation for each type
        of adult and family:
        Female, adjacent, HH Family
        Female, non-adjacent, HH Family
        Female, adjacent, TD Family
        Female, non-adjacent, TD Family
        Male, adjacent, HH Family
        Male, non-adjacent, HH Family
        Male, adjacent, TD Family
        Male, non-adjacent, TD Family

        Input:
        Up to eight output files from Step 3.  These contain mean f0 values
        for each of the conversations defined in Step 2 and processed in
        Step 3

        Output:
        Up to eight output files, each containing id info, along with mean and
        standard deviation for, for example, Female, adjacent, HH Family. See
        getMeanStd for format.
        """
        

        #Delete results repository if its exists
        errCode = os.system('ls ' + Const4.RESULTS)
        if errCode == 0: #directory exists
            os.system('rm -r ' + Const4.RESULTS)
            print 'files holding previously saved results files deleted'

        #make new directory for results
        errCode = os.system('mkdir ' + Const4.RESULTS)
        if errCode > 0:
            print 'problem creating ' + Const4.RESULTS
            sys.exit()

        '''
        for each csv file in the results directory, produces a csv file with 
        three columns:
        1) session id (family + data + recording identifier)
        2) mean f0 for all entries for the same session id in the original i
           csv file
        3) std for the computation in column 2
        ex:
        KA05_20100325_093017_003524,227.2,58.1
        '''
    def getMeanStd(self):
        """
        Retrieve list of output files from Step 3.  Iterate over them
        """
        if os.path.exists(C.Const3.F0REPOS):
            fileLst = os.listdir(C.Const3.F0REPOS)
            for fname in fileLst:
                self.readFile(fname)
        else:
            print  C.Const3.F0REPOS + ' not created'
            print 'Make sure that f0 extraction ran to completion'
            sys.exit()

    def readFile(self,fname):
        """
        Read an output file from Step 3
        Invoke routines to compute mean and standard deviation

        Parameters:
            fname: name of an input file to process
        """
        fnameLst = fname.split('.')
        outp = Const4.RESULTS + fnameLst[0] + '_mean_std' + '.csv'
        inp = C.Const3.F0REPOS + fname
        fin = open(inp, 'r')
        fLst = fin.readlines()
        if len(fLst) > 0:
            fout = open(outp, 'w')
            self.compute(fLst,fout)
            fout.close()
        fin.close()

    def compute(self,fLst,fout):
        """
        Construct a list of f0 values for the input file undergoing processing
        Compute mean and standard deviation for the list
        Write values to output file

        Parameters:
            fLst: listized version of input file
            fout: internal name of output file
        """
        idPrev = ''
        subLst = []
        lineCt = 0
        #remove eol
        fLst = [line.rstrip() for line in fLst]
        #turn list of lines as strings to list of lines as lists
        fLst = [line.split(',') for line in fLst]
        #construct an id from the family name and session id and
        #transform string rep. of f0 to float
        fLst = [[line[0] + '_' + line[1],(float(line[2]))] for line in fLst]
        #be sure that f0 is a number
        fLst = [line for line in fLst if not np.isnan(line[1])]
        for line in fLst:
            lineCt = lineCt + 1
            idCur = line[0]
            f0 = line[1]
            '''
            Five Cases:
            1)  fLst contains a single conversation with a single f0 value
                Length of fLst == 1
            2)  Beginning of conversation and not case 1
                Current Line is the first line in an input file
                --add f0 to sublist
                --set idPrev to id of current line
            3)  Within a conversation
                Current Line id is the same as the last line
                --add f0 to the sublist
            4)  End of conversation but not end of fLst
                Current Line id is different from the last line
                --Compute mean and std
                --Write to output file
                --start a new sublist
                --add f0 of current line to new sublist
                --reset idPrev to the current id
            5)  End of fList
                --Compute mean and std
                --Write to output file   
            '''
            #Case 1
            if len(fLst) == 1:
                subLst.append(f0)
                mean = np.around(np.mean(subLst), decimals = 1)
                std = np.around(np.std(subLst), decimals = 1)
                fout.write(idCur + ',' + str(mean) + ',' + str(std) + '\n')
                break

            #Cases 2 & 3
            if idPrev == '' or idPrev == idCur:
                subLst.append(f0)
                idPrev = idCur
        
            #Cases 4 & 5
            if idPrev != idCur or lineCt == len(fLst):
                mean = np.around(np.mean(subLst), decimals = 1)
                std = np.around(np.std(subLst), decimals = 1)
                fout.write(idPrev + ',' + str(mean) + ',' + str(std) + '\n')
                subLst = []
                subLst.append(f0)
                idPrev = idCur
            
    def cleanLine(self,line):
        """
        Tokenize line from input file

        Parameters:
            line: line from input file
        """
        
        line = line.rstrip()
        lineLst = line.split(',')
        idCur = lineLst[0] + '_' + lineLst[1]
        f0 = float(lineLst[2])
        return idCur, f0

       
       
   
