import sys
from Analyze import *
import time

def main():
    
    print time.strftime("%a,%d %b %Y %H:%M:%S",time.localtime())
    print '********************'
    print 'Start Analysis'
    print '********************'
    print ''
    start = time.time()
    
    A = Analyze()
    A.retrieveFiles()
    
    print ''
    print '********************'
    print 'Finish Analysis'
    print '********************'
    print time.strftime("%a,%d %b %Y %H:%M:%S",time.localtime())
    howLong = (time.time()- start)
    print "Running Time = " + str(howLong)
    print "Step 5 Complete"
    return 1
    
main()
