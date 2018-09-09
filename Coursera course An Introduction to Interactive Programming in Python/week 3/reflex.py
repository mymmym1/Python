# Reflex tester

###################################################
# Student should add code where relevant to the following.

import simplegui 

total_ticks = 0
#first_click = True
num = 0

# Timer handler
def tick():
    global total_ticks
    total_ticks += 1        
    
# Button handler
def click():
    global num
    global total_ticks
    num += 1    
    if num % 2 != 0:
        timer.start()        
    else:
        time = total_ticks * 10
        print "Your click speed is: " + str(time) + " ms."
        timer.stop()
        total_ticks = 0

# Create frame and timer
frame = simplegui.create_frame("Counter with buttons", 200, 200)
frame.add_button("Click me", click, 200)
timer = simplegui.create_timer(10, tick)

# Start timer
frame.start()
