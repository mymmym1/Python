#!/usr/bin/env python
#Yimin


import sys, math


f1=open(sys.argv[1] , 'r')
l1=f1.readlines()
f1.close()

f2=open(sys.argv[2] , 'r')
l2=f2.readlines()
f2.close()



list1=[]
list2=[]

for n in l1:
        if n[:4]=="ATOM":
                xcor1=float(n[30:38])
                ycor1=float(n[38:46])
                zcor1=float(n[46:54])
                list1.append([xcor,ycor,zcor])

for n in l2:
        if n[:4]=="ATOM":
                xcor2=float(n[30:38])
                ycor2=float(n[38:46])
                zcor2=float(n[46:54])
                list2.append([xcor2,ycor2,zcor2])

sumx=0
sumy=0
sumz=0

n=len(list1)
m=len(list2)
if n==m:
   for i in range(n):
        vx=list1[i][0]
        vy=list1[i][1]
        vz=list1[i][2]
        
        wx=list2[i][0]
        wy=list2[i][1]
        wz=list2[i][2]

        sumx+=(vx-wx)**2
        sumy+=(vy-wy)**2
        sumz+=(vz-wz)**2


    sumsq=sumx+sumy+sumz
    avg=sumsq/n

RMSD=math.sqrt(avg)

print "The RMSD is" , RMSD
print "Done"
