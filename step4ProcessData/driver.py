import sys
from Results import *
import time


def main():
    
    print time.strftime("%a,%d %b %Y %H:%M:%S",time.localtime())
    print '********************'
    print 'Start F0 Processing'
    print '********************'
    print ''
    start = time.time()
    
    R = Results()
    R.getMeanStd()
    
    print ''
    print '********************'
    print 'Finish F0 Processing'
    print '********************'
    print time.strftime("%a,%d %b %Y %H:%M:%S",time.localtime())
    howLong = (time.time()- start)
    print "Running Time = " + str(howLong)
    print "Step 4 Complete"
    return 1
    
main()
