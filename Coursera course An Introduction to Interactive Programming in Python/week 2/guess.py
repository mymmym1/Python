# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math
count = 0
high = -1

# helper function to start and restart the game
#def new_game():
    # initialize global variables used in your code here
    # global secret_number
    # secret_number = random.randrange(0, 100)
   
    # define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game         
    global count
    global low
    global high
    global secret_number
    count = 0
    low = 0
    high = 100
    secret_number = random.randrange(low, high)    
        
def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global count
    global low
    global high
    global secret_number
    count = 0
    low = 0
    high = 1000
    secret_number = random.randrange(low, high)    
    
def input_guess(guess):
    # main game logic goes here	
    if high == -1:
        print "Error. Select range first."
    else:
        guess_number = int(float(guess))
        if guess_number >= high or guess_number < low:
            print "Guess out of range"
        else:            
            global count
            count += 1
            remain = int(math.ceil(math.log(high - low + 1) / math.log(2)) - count)
            print "Guess was " + str(int(float(guess)))
            if guess_number < secret_number:
                if remain == 0 and high == 100:
                    print "Your last guess is still wrong. Game restarted." 
                    count = 0            
                    range100()
                elif remain == 0 and high == 1000:
                    print "Your last guess is still wrong. Game restarted." 
                    count = 0            
                    range1000()
                else:
                    print "Higher"
                    print "Your remaining number of guess is " + str(remain) + "."
            elif guess_number > secret_number:
                if remain == 0 and high == 100:
                    print "Your last guess is still wrong. Game restarted." 
                    count = 0            
                    range100()
                elif remain == 0 and high == 1000:
                    print "Your last guess is still wrong. Game restarted." 
                    count = 0            
                    range1000()
                else:
                    print "Lower"
                    print "Your remaining number of guess is " + str(remain) + "."
            elif guess_number == secret_number:
                print "Correct. New game of the same range starts or select the other range."
                count = 0
                if high == 100:
                    range100()
                elif high == 1000:
                    range1000()
        
# create frame
frame = simplegui.create_frame("Guess Game", 200, 200)

# register event handlers for control elements and start frame
frame.add_input("Guess it", input_guess, 100)
frame.add_button("Number 0-99", range100, 100)
frame.add_button("Number 0-999", range1000, 100)
frame.start()

# call new_game 
# new_game()


# always remember to check your completed program against the grading rubric
