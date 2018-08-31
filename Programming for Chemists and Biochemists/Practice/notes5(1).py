#!/usr/bin/env python

namelist=['Frank','Jim','Steve']
gradelist=[[95,6,80.4,76.3],[75,6,90.4,66.3],[65.6,70.4,66.3]]

if len(namelist)==len(gradelist):
  for i in range(len(namelist)):
     grades=gradelist[i]
     sum=0
     for grade in grades:
        sum+=grade
        avg=sum/len(gradelist)
     print "%s's GPA is %1f"%(namelist[i],avg)

else:
    print "the number of names is different than the number of grades"
