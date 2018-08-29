#!/usr/bin/env python

l=['Luke','Anakin','Palpatine']
for name in l:
    if name=='Luke':
       force='light'
    elif name=='Palpatine':
       force='dark'
    else:
       force='unknown'
    print "%s:%s"%(name, force)
print "Done!"
