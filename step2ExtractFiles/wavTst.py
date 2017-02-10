from Const import *
import wave


def main():

    #fn = wave.open(Const.LOC_INP + 'HE47/2010_03/e20100330_105907_003606.wav','r')
    fn = wave.open('handel.wav','r')
    rate = fn.getframerate()
    pos = fn.tell()
    print pos
    print rate
    pos = pos + 3 * rate
    fn.setpos(pos)
    print fn.tell()
    

main()
