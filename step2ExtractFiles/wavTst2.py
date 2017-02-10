import wave 
import struct
import sys

def main():

    ifile = wave.open("handel.wav")
    ofile = wave.open("output.wav", "w")
    ofile.setparams(ifile.getparams()) #get characteristics of input file
                                       #write them to output file

    sampwidth = ifile.getsampwidth()   #get sample width in bytes

    #h is hex, = says choose big or little endian as you wish
    fmts = (None, "=B", "=h", None, "=l")

    #out sample width is 2
    fmt = fmts[sampwidth]

    #I don't get this one
    dcs  = (None, 128, 0, None, 0)        
    dc = dcs[sampwidth]

    start = 0
    rate = ifile.getframerate()
    stop = rate * 3
    final = 0

    for i in range(stop):
        #read a frame
        iframe = ifile.readframes(1)

        #iframe is a hex string representing two digits.  We want to unpack it
        #to a tuple of two digits.  We want only the 0th
        iframe = struct.unpack(fmt, iframe)[0]  
        
        iframe -= dc #back up 0 (in our case)
        

        #why
        oframe = iframe / 2;

        oframe += dc
        oframe = struct.pack(fmt, oframe)
        ofile.writeframes(oframe)
        final = i

    print stop
    print i
    print rate
    ifile.close()
    ofile.close()
    

main()
