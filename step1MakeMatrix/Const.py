class Const():
    NOTFOUND = -1
    
    #path to directory holding the its and wav input files
    #LOC_INP = '/home/depalma/Documents/sabbatical14-15/paper4/lenaSmall/'
    #LOC_INP = '/home/paul/Desktop/sabbatical14-15/paper4/lenaSmall/'
    #LOC_INP = '/home/depalma/paper4/lenaSmall/'
    LOC_INP = '/home/shares/lena/LENA/'
    #LOC_INP = '/home/paul/Desktop/sabbatical14-15/paper4/lenaSmallAlt/'

    #path to directory holding matrices that store start/stop times
    #LOC_OUT = '/home/depalma/Documents/sabbatical14-15/paper4/lenaMatrix/'
    #LOC_OUT = '/home/paul/Desktop/sabbatical14-15/paper4/lenaMatrix/'
    LOC_OUT = '/home/depalma/paper4/lenaMatrix/'
    
    #Directories holding intermediate files and error files
    #LOC_UTIL = '/home/depalma/Documents/sabbatical14-15/paper4/step1MakeMatrix/lenaUtils/'
    #LOC_UTIL = '/home/paul/Desktop/sabbatical14-15/paper4/step1MakeMatrix/lenaUtils/'
    LOC_UTIL = '/home/depalma/paper4/step1MakeMatrix/lenaUtils/'
    
    #name of the file holding dictionary used to recreate the lena
    #directory structure
    DICTFILE = 'dirsDict.txt'

        

    DICT_TO_MAT_FILE = 'dictMat.txt'
    
    #error file used to store system error messages
    ERRFILE = LOC_UTIL + 'sysErr.txt'

    #folders, sub-folders passed over
    EXCEPTION = LOC_UTIL + 'exceptions.txt'
    
    #tokenize its filetype
    ITSTYPE = '.tok'
    
    #matrix filetype
    MAT = '.mat'

    #excel file holding the family descriptor data (HH, TD, etc.)
    #XLSX_FILE = '/home/depalma/Documents/sabbatical14-15/paper4/lenaExcel/SubjectDatabase14.xlsx'
    #XLSX_FILE = '/home/paul/Desktop/sabbatical14-15/paper4/lenaExcel/SubjectDatabase14.xlsx'
    XLSX_FILE = '/home/depalma/paper4/lenaExcel/SubjectDatabase14.xlsx'


    #name of relevant sheet in XLSX_FILE
    SHEET = 'DemographicsRecording Dates'
    #SHEET = 'Sheet1'

    #legal speakers
    SPKR = 'CHN|MAN|FAN'

    #legal children
    CHILD = {'CHN'}

    #legal adults
    ADULT = {'FAN', 'MAN'}

    #Male/Female Adult Near
    MAN = 'MAN'
    FAN = 'FAN'
    

    #Adjency Constant
    PRE_ADJ = 'PREA'
    POST_ADJ = 'PSTA'
    BOTH = 'BOTH'
    NON_ADJ = 'NONA'
    NOT_APPL = 'CHlD'



    
