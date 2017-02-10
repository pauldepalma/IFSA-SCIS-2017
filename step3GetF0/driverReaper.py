import sys
from ExtractF0 import *
import time


def main():
    print time.strftime("%a,%d %b %Y %H:%M:%S",time.localtime())
    print '********************'
    print 'Start F0 Extraction'
    print '********************'
    print ''
    start = time.time()
    
    f0 = ExtractF0()
    f0.countConv()
    f0.accumF0('reaper')
    
    print ''
    print '********************'
    print 'Finish F0 Extraction'
    print '********************'
    print time.strftime("%a,%d %b %Y %H:%M:%S",time.localtime())
    howLong = (time.time()- start)
    print "Running Time = " + str(howLong)
    print "Step 3 Complete"
    
main()
