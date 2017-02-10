import sys
import os
from Const5 import *
import numpy as np
import imp

C = imp.load_source('Const4.py', Const5.STEP4 + 'Const4.py')


class Analyze:
    def __init__(self):
        """
        Produces a 5-tuple:
        session id, mean non-adj f0, non-adj std, mean adj f0, adj std
        The tuple is produced only if the particular speaker has both adjacent and
        non-adjacent speech.  
        
        Input:
        Files storing mean f0 values from step 4

        Output:
        Up to four csv files with lines in the following format:
        session_id,mean_non-adjacent_f0,mean_adjacent f0
        For example, FHH.csv might have this line:
        MM28_20100921_121146_003985,191.5,244.0

        In the example:
            FHH indicates that the speaker is female, the child is hard-of-hearing
            MM28 is the family name
            20100921_121146_003985 is the name if the .wav/.its file (minux 'e' prefix)
            191.5 is the mean non-adjacent f0 value for the speaker
            244.0 is the mean adjacent f0 value for the speaker

        These files are named FHH.csv, FTD.csv, MHH.csv, MTD.csv and stored in 
        Const.ANALYSIS
        """

        #Delete analysis repository if its exists
        errCode = os.system('ls ' + Const5.ANALYSIS)
        if errCode == 0: #directory exists
            os.system('rm -r ' + Const5.ANALYSIS)
            print 'files holding previously saved analysis files deleted'

        #make new directory for analysis files
        errCode = os.system('mkdir ' + Const5.ANALYSIS)
        if errCode > 0:
            print 'problem creating ' + Const5.ANALYSIS
            sys.exit()
        
    def retrieveFiles(self):
        """
        Retrieve list of output files from Step 4.  Iterate over them
        """
        if os.path.exists(C.Const4.RESULTS):
            fileLst = os.listdir(C.Const4.RESULTS)
            self.constructDataPoints(fileLst)
        else:
            print  C.Const4.RESULTS + ' not created'
            print 'Make sure mean/std computation worked'
            sys.exit()

    def constructDataPoints(self,tplLst):
        """
        Driver function for the entire class
        tplLst is a list of .csv files
        tupleLst is a list of tuples, each containing file names of the adjacent and
        non-adjacent f0 values for a particular speaker and family type.
        Example tupleLst:
        [('FHH-a_mean_std.csv', 'FHH-na_mean_std.csv'), ('FTD-a_mean_std.csv', 
          'FTD-na_mean_std.csv'), ('MTD-a_mean_std.csv', 'MTD-na_mean_std.csv')]
        """
        tupleLst = self.makeTuples(tplLst)
        #since the graph will have points of the form (na,a), exchange the order of the
        #items in the tuple.  Sort put them (a,na)
        for tpl in tupleLst:
            tplNew = (tpl[1],tpl[0])
            self.mkPointFiles(tplNew)
        print "data point files constructed at: " + Const5.ANALYSIS

    def makeTuples(self,fileLst):
        """
        Creates a list of tuples, where each tuple contains the names of the 
        non-adjacent and adjacent
        mean f0 files from step 4
        Example:
        [('FHH-a_mean_std.csv', 'FHH-na_mean_std.csv'), ('FTD-a_mean_std.csv',
        'FTD-na_mean_std.csv'), ('MTD-a_mean_std.csv', 'MTD-na_mean_std.csv')]

        If the files from step 4 contains a non-adjacent without a corresponding 
        adjacent or vice-versa,
        it's passed over.  This could lead to an odd number of files.
        """
        
        fileLst.sort()
        tupleLst = []
        j = 1
        i = 0
        while (j < len(fileLst)):
            adj = fileLst[i].split('-')
            nonadj = fileLst[j].split('-')
            if adj[0] == nonadj[0]:
                tpl = (fileLst[i],fileLst[j])
                tupleLst.append(tpl)
                j = j + 2
                i = i + 2
            else:
                i = i + 1
                j = j + 1
        return tupleLst
    

    def mkPointFiles(self,tpl):
        """
        For each file pair in the list of tuples (see makeTuples, above), creates 
        the output file described in the constructor documentation, above.  These
        files, in turn, can be used to create Mark's graphs where the (in theory)
        the adjacent f0s cluster above x=y, and the non-adjacent f0s cluster below
        x=y. 
        """
        #spkr_type is FHH_a, FHH_na etc 
        spkr_type = tpl[0].split('-')

        #turn files into lists
        cln_na, cln_a = self.makeLists(tpl) 

        """ 
        To construct a graph we need both x (non-adjacent) and y (adjacent) values.
        It's possible that some recording sessions have one or the other but not both.
        By putting the data in a dictionary, session id can be searched on to make sure
        we have both x and y values.  
        """ 
        na_dict, a_dict = self.makeDicts(cln_na,cln_a)

        pts = []
        #found is true for every key in na_dict that is also in a_dict
        na_keys = na_dict.keys()
        for key in na_keys:
          found = a_dict.get(key,False)
          if found:
            na_values = na_dict[key]
            a_values = a_dict[key]
            tpl = (key, na_values[0],na_values[1],a_values[0],a_values[1]) 
            pts.append(tpl) 
        
        self.writePoints(spkr_type, pts)

    def makeLists(self,tpl): 
        """
        transforms files in tpl to lists
        """
        fl_na = C.Const4.RESULTS + tpl[0]
        fl_a = C.Const4.RESULTS + tpl[1]
        
        fin_a = open(fl_a, 'r')
        fin_aLst = fin_a.readlines()
        cln_a = self.cleanLines(fin_aLst)
        fin_a.close()
        
        fin_na = open(fl_na, 'r')
        fin_naLst = fin_na.readlines()
        cln_na = self.cleanLines(fin_naLst)
        fin_na.close()

        return cln_na, cln_a


    def cleanLines(self,lines):
        """
        tokenizes each input mean f0 file
        clnLines contains session id, mean f0, std
        """
        clnLines = [line.rstrip() for line in lines]
        clnLines = [line.split(',') for line in clnLines]
        clnLines = [[line[0],line[1],line[2]] for line in clnLines]
        return clnLines

    
    def makeDicts(self, cln_na,cln_a):
        """
        turns two lists into two dictionaries
        input:
        [session_id,meanF0,std]
        output:
        {session_id:(meanF0,std)}
        """

        a_dict = {cln_a[i][0]:(cln_a[i][1],cln_a[i][2]) for i in range(len(cln_a))}
        na_dict = {cln_na[i][0]:(cln_na[i][1],cln_na[i][2]) for i in range(len(cln_na))}  
        return na_dict, a_dict  

    def writePoints(self,spkr_type,points):
        """
        save points to files like FHH_a.csv, FHH_na.csv, etc
        """
 
        fout = open(Const5.ANALYSIS + spkr_type[0] + '.csv', 'w')
        for tpl in points:
            #session id, mean non-adj f0, non-adj std, mean adj f0, adj std
            fout.write(tpl[0] + ',' + tpl[1] + ',' + tpl[2] + ',' + tpl[3] + ',' 
            + tpl[4] + '\n')
        fout.close()
