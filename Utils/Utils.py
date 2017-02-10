from Const import *

class Utils:
    """
    Contains utilities that are helpful in debugging
    """
    def __init__(self):

      print "Utils Object Created"     
       
    def getDict(self):
        """
        Read file containing the dictionary the represents the file system.
        Return the dictionary to the calling program.
        """
        
        #open dictionary file created through Filter class
        fin = open(Const.LOC_UTIL + Const.DICTFILE, 'r')
        dirDict = eval(fin.read())
        fin.close()
        return dirDict
    


