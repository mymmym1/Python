#!/usr/bin/env python

namelist=[]
gradelist=[]

while True:
      name=raw_input("Please enter a name or enter end to stop: ")
      if name=='end':
             break
      gradestring=raw_input("Please enter a list of grades seperated by commas: ")
      grades=[]
      for n in gradestring.split(','):
             grades.append(int(n))
      namelist.append(name)
      gradelist.append(grades)

      if len(namelist)==len(gradelist):
              for i in range(len(namelist)):
                       grades=gradelist[i]
                       sum=0
                       for grade in grades:
                                sum+=grade
                       avg=sum/len(grades)
                       print "%s's GPA is %.1f"%(namelist[i],avg)

