#!/usr/bin/env python
#Yimin


import sys, cmath
import numpy, scipy, matplotlib 

from scikits.learn.em import GM, GMM, EM  #Expectation-Maximization algorithm

import generic

infile=sys.argv[1]

ni = 1  #number of FID in this PISEMA experiments
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
    for m in range(td):
        if m%2==0:
           fid1.append(fid0[m])
        else 
           fid2.append(fid0[m])
    
    for n in range(td/2):
        fid.append(complex(fid1[n],fid2[n]))

    fid = numpy.reshape(fid, (td / (2 * ni), ni)) #convert row vector into column vector; we get row number: td/(2*ni), column number: ni

    [mrows0, ncols0] = numpy.size(fid)
    FIDMTX = numpy.zeros((mrows0, ncols0), float)
    for i in range(mrows0):
          for j in range(ncols0):
                FIDMTX[i][j] = fid[i][j]
    [mrows, ncols] = numpy.size(FIDMTX)


    em  = EM()
    FIDMTX = em.train(FIDMTX, 400, dw1)#  exponential-lb=100Hz (lb-line broadening factor);dw1 is threshold; 400 is maxiter  
                                       #  threshold: When the likelihood is increasing less than 'threshold', stop the algorithm
                                       #  max_iter: When the iteration number is larger than 'maxiter', stop the algorithm
                  
    FIDMTX = numpy.zfill(FIDMTX, 2 * mrows0)#zero filling the data to doublesize

    spec = numpy.transpose(numpy.fft(FIDMTX))  #FT transform the first dimension; transpose is exchange x axis and y axis
    spec = cmath.phase(spec, 78, 58.6 * 360) #phase the vector 
    spec = spec.real #remove the imaginary part
    spec = geneic.bcorr_offset(spec, 350, 500)       #baseline correction

    matplotlib.pyplot.plot(spec)
    grid(True)

