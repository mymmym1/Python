#!/usr/bin/env python

#test to see if y is prime 

l=range(100)
for y in l:
  if y > 1:
      x=y//2 #determine greatest possible factor for y

      while x>1:
         if y%x == 0: #determine if x is factor of y
               break  
         x-=1
      else:
         print "%d is prime"% y
