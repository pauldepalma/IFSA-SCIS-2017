class Const3():

    #STEP1 = '/home/depalma/Documents/sabbatical14-15/paper4/step1MakeMatrix/'
    STEP1 = '/home/depalma/paper4/step1MakeMatrix/'
    #STEP1 = '/home/paul/Desktop/sabbatical14-15/paper4/step1MakeMatrix/'

    #names of F0 Extractor
    EXT = 'talkin1'
    EXT1 = 'reaper'

    #Dave Talkin's older get_f0 along with parameter files
    #GETF0DIR = '/home/depalma/Documents/sabbatical14-15/paper4/step3GetF0/talkinF0/'
    #GETF0DIR = '/home/paul/Desktop/sabbatical14-15/paper4/step3GetF0/talkinF0/'
    GETF0DIR = '/home/depalma/paper4/step3GetF0/talkinF0/'
    GETF0 = 'get_f0_snd -P '
    FEM = 'fparams.txt'
    MALE = 'mparams.txt'
    CHLD = 'cparams.txt'

    #Dave Talkin's newer F0 extracter, called reaper
    REAPER = '/home/paul/Desktop/sabbatical14-15/paper4/step3GetF0/googleF0/REAPER/build/reaper'
    REAPER_OUT = '/home/paul/Desktop/sabbatical14-15/paper4/step3GetF0'
    
    #path to f0 repository
    #F0REPOS = '/home/depalma/Documents/sabbatical14-15/paper4/f0Repos/'
    #F0REPOS = '/home/paul/Desktop/sabbatical14-15/paper4/f0Repos/'
    F0REPOS = '/home/depalma/paper4/f0Repos/'

    #Log file 
    #F0LOG = '/home/depalma/Documents/sabbatical14-15/paper4/step3GetF0/f0Log.txt'
    #F0LOG = '/home/paul/Desktop/sabbatical14-15/paper4/step3GetF0/f0Log.txt'
    F0LOG = '/home/depalma/paper4/step3GetF0/f0Log.txt'

    #F0ERR= '/home/depalma/Documents/sabbatical14-15/paper4/step3GetF0/errLog.txt'
    #F0ERR= '/home/paul/Desktop/sabbatical14-15/paper4/step3GetF0/errLog.txt'
    F0ERR= '/home/depalma/paper4/step3GetF0/errLog.txt'

    #F0 files for child-adjacent adults
    F0_FILES = ['MTD-a.csv', 'MHH-a.csv', 'FTD-a.csv', 'FHH-a.csv',
                'MTD-na.csv','MHH-na.csv','FTD-na.csv','FHH-na.csv']

    #decoded (initially constants were used]
    '''
    MTD = 'MTD-a.csv' #male-traditionally developing child
    MHH = 'MHH-a.csv'
    FTD = 'FTD-a.csv'
    FHH = 'FHH-a.csv' #female-hard-of-hearing child

    #F0 files for child-non-adjacent adults
    MTD-non = 'MTD-na.csv' #male-traditionally developing child
    MHH-non = 'MHH-na.csv'
    FTD-non = 'FTD-na.csv'
    FHH-non = 'FHH-na.
    '''

    #This is used in processMatrix to control how many conversations to process
    #1: process all
    #2: process every other
    #3: process every third
    #etc
    SKIP = '1'
    
    
