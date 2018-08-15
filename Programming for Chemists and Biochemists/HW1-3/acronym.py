#! /usr/bin/env python

s=raw_input("Please input a phrase you want to convert into an acronym: ")
l=s.split()
a=""
for n in l:
    a=a+n[0]
a=a.upper()

print a
