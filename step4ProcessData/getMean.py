
from Const4 import *



class Results:
    def __init__(self):


        #Delete results repository if its exists
        errCode = os.system('ls ' + Const4.RESULTS)
        if errCode == 0: #directory exists
            os.system('rm -r ' + Const4.RESULTS)
            print 'files holding previously saved f0 files deleted'

        #make new directory for results
        errCode = os.system('mkdir ' + Const4.RESULTS)
        if errCode > 0:
            print 'problem creating ' + Const4.RESULTS
            sys.exit()


        
    def getMean(self,fname):
        fin = open(Const4.RESULTS + fname, 'r')
        fLst = fin.readlines()
        print fLst[0]
        
        
        
   
