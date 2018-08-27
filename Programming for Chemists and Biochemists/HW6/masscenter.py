#!/usr/bin/env python
#Yimin

import sys 

#Usage: centerpdb.py infile outfile
infile=sys.argv[1]
outfile=sys.argv[2]

masses={
        ' H':1.0079,
        ' C':12.011,
        ' O':15.9994,
        ' S':32.06,
        ' P':30.97376,
        ' N':14.00674}

#open infile and read into linelist
def readpdb(filename):
    f1=open(infile, 'r')
    linelist=f1.readlines()
    f1.close()
 
    n=len(linelist)
    line=[]
    atomlist=[]

    for i in range(n): 
        line=linelist[i]
        if line[0:4]!="ATOM":    
           continue            #discard lines not start with ATOM

        #parse each line     
        rtype = line[0:6]
        atomnumber = int(line[6:11])
        atomtype = line[12:16]
        altLoc = line[16:17]
        resName = line[17:20]
        chainID = line[21:22]
        resSeq = int(line[22:26])
        iCode = line[26:27]
        x = float(line[30:38])
        y = float(line[38:46])
        z = float(line[46:54])
        occupancy = float(line[54:60])
        tempFactor = float(line[60:66])
        element = line[76:78]
        charge = line[78:80]
 
        #difine dictionary & record data
        atom={'rtype':rtype,
              'atomnumber':atomnumber,
              'atomtype':atomtype,
              'altLoc':altLoc,
              'resName':resName,
              'chainID':chainID,
              'resSeq':resSeq,
              'iCode':iCode,
              'x':x,
              'y':y,
              'z':z,
              'occupancy':occupancy,
              'tempFactor':tempFactor,
              'element':element,
              'charge':charge}
        atomlist.append(atom)
   
    return atomlist



def geocenter(atomlist):
      xavg=0
      yavg=0
      zavg=0

      for atom in atomlist:
        #compute geometric center
          xavg+=atom['x']
          yavg+=atom['y']
          zavg+=atom['z']

      m=len(atomlist)

      xavg=xavg/m
      yavg=yavg/m
      zavg=zavg/m

        
      for atom in atomlist:
                atom['x']=atom['x']-xavg 
                atom['y']=atom['y']-yavg 
                atom['z']=atom['z']-zavg

      return {'geocenterx':xavg,'geocentery':yavg,'geocenterz':zavg}



def masscen(atomlist):
        masssum=0
        weightedx=0
        weightedy=0
        weightedz=0

        for atom in atomlist:
                masssum+=masses[atom['element']]
                weightedx+=atom['x']*masses[atom['element']]
                weightedy+=atom['y']*masses[atom['element']]
                weightedz+=atom['z']*masses[atom['element']]


        masscenterx=weightedx/masssum
        masscentery=weightedy/masssum
        masscenterz=weightedz/masssum

        return  {'masscenterx':masscenterx,'masscentery':masscentery,'masscenterz':masscenterz}


#write into outfile with pdb format using new x, y, z
def writepdb(filename, atomlist):
      f2=open(filename,'w')
      for atom in atomlist:
  
         f2.write("%-6s%5d %-4s%1s%-3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f           %1s%-2s\n" % (atom['rtype'],atom['atomnumber'],atom['atomtype'],atom['altLoc'],atom['resName'],atom['chainID'],atom['resSeq'],atom['iCode'],atom['x'],atom['y'],atom['z'],atom['occupancy'],atom['tempFactor'],atom['element'],atom['charge']))
        
      f2.close()


if __name__=="__main__":

        

        atomlist=readpdb(infile)

        geocenter(atomlist)

        centerofmass=masscen(atomlist)

        print "com dict", centerofmass

        writepdb(outfile, atomlist)
        


print "Done"

