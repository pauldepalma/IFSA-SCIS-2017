
from Utils import *

def main():

    util = Utils()

    dirDict = util.getDict()

    keyLst = dirDict.keys()

    for family in keyLst:
        print family
        sessionLst = dirDict[family]
        for session in sessionLst:
            print ' ' + session

main()

