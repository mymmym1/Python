# Compute and print powerball numbers.

###################################################
# Powerball function
# Student should enter function on the next lines.
import random
def powerball():
    print "Today's numbers are "+str(random.randrange(1,60))+",",
    print str(random.randrange(1,60))+",",
    print str(random.randrange(1,60))+",",
    print str(random.randrange(1,60))+",",
    print "and " + str(random.randrange(1,60))+".",
    print "The Powerball number is " + str(random.randrange(1,36)) + "."
    
    
###################################################
# Tests
# Student should not change this code.
    
powerball()
powerball()
powerball()
