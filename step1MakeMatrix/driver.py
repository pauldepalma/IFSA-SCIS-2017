import sys
from CleanUp import *
from Tokenize import *
from CreateMatrix import *
from Filter import *
import time


def main():


    print time.strftime("%a,%d %b %Y %H:%M:%S",time.localtime())
 
    print '********************'
    print 'Start Matrix Construction'
    print '********************'
    print ''
    start = time.time()

    #remove invalid data
    fileSystem = CleanUp()
   
    #create dictionaries used in matrix construction
    dirsDict = fileSystem.getFileSystemDict()
    familyDescDict = fileSystem.getFamilyDescDict()
    
    #extracts into a more useable format the data from its files
    tokenize = Tokenize(dirsDict)
    tokenize.makeDirStr()
    tokenize.copyItsFiles()
    
    tokenize.extractSpkrInfo(familyDescDict)

    #create matrices where each matrix is data extracted from a single its file
    makeMat = CreateMatrix(dirsDict)
    makeMat.makeMatrices()
    makeMat.removeIts()

    #filter by age and gender
    Filter(dirsDict,'0','1000','MF')
    
    print '********************'
    print 'Finish Matrix Construction'
    print '********************'
    print time.strftime("%a,%d %b %Y %H:%M:%S",time.localtime())
    howLong = (time.time()- start)
    print "Running Time = " + str(howLong)
    print "Step 1 Complete"
    print " "
    return 1
    #write matlib description of file system
    #fileSystem.dictToMat()
    
main()

