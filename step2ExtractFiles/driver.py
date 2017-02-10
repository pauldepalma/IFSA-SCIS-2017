import sys
from ExtractConv import *
import time

def main():

    print time.strftime("%a,%d %b %Y %H:%M:%S",time.localtime())
    print '********************'
    print 'Start File Extraction'
    print '********************'
    print ''
    start = time.time()
    
    ext = ExtractConv()
    ext.extractFiles()

    print ''
    print '********************'
    print 'Finish File Extraction'
    print '********************'
    print time.strftime("%a,%d %b %Y %H:%M:%S",time.localtime())
    howLong = (time.time()- start)
    print "Running Time = " + str(howLong)
    print "Step2 Complete"
    print ''
    return 1
main()
