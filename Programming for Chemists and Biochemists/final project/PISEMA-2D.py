#!/usr/bin/env python
#Yimin


import sys, cmath
import numpy, scipy, matplotlib


from scikits.learn.em import GM, GMM, EM

import generic

infile=sys.argv[1]

ni = 32  #number of FID in this PISEMA experiments
dw1=15.0e-6 #dwell time 1 is 15.0us

if __name__=="__main__":

    fid = []
    fid0 = []

    f = open(infile, 'rb')
    fid0 = f.readlines()
    f.close()

    td = len(fid0) #time domain-number of raw data points; The larger td is, the higher spectrum resolution, but the longer acquisition time.

    fid1 = []
    fid2 = []
    for i in td:
        if i%2==0:
           fid1.append(fid0[i])
        else 
           fid2.append(fid0[i])
    
    for i in len(fid1):
        fid.append(complex(fid1[i],fid2[i]))

    fid = numpy.reshape(fid, td / (2 * ni), ni)

    [mrows0, ncols0] = numpy.size(fid)
    FIDMTX = numpy.zeros((mrows0, ncols0), float)
    for i in range(mrows0):
          for j in 1:24 :
                FIDMTX[i][j] = fid[i][j]

    [mrows, ncols] = numpy.size(FIDMTX)

    em  = EM()
    FIDMTX = em.train(FIDMTX, 400, dw1)#exponential-lb=100Hz (lb-line broadening factor)
   
    FIDMTX = numpy.zfill(FIDMTX, 2 * mrows0)#zero filling the data to doublesize
    
    spec = numpy.transpose(numpy.fft(FIDMTX))  #FT transform the first dimension
    spec = cmath.phase(spec, -150, 59.2 * 360) #phase the vector 
    spec = spec.real #remove the imaginary part
    spec = generic.bcorr_offset(spec, 350, 500)       #base line correction
 

    #2nd dimention data processing
    st1 = transpose(spec)   #transpose the matrix
    st1[1,:] = st1[1,:]*0.5   #first point attenuation

    dw2=44.6e-6   #dwell time on F1 is 44.6us

    em  = EM()
    st1 = em.train(st1, 200, dw2)     #exponential - lb = 200Hz
    st1 = generic.apodise(sqsin(pi/2),st1)  #sine bell squared apodization  
    st1 = numpy.zfill(st1, 256)     #zero fill the data to double size
    spec2 = numpy.transpose(numpy.fft(st1)))    #FT transform the second dimension
    spec2 = spec2.real

    delta = 1
    x = numpy.arange(1, 512, delta)
    y = numpy.arange(1, 256, delta)
    X, Y = numpy.meshgrid(x, y)

    matplotlib.pyplot.contour(X, Y, spec2, 10)
    grid(True)




