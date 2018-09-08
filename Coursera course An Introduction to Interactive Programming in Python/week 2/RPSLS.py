# GUI-based version of RPSLS

###################################################
# Student should add code where relevant to the following.

import simplegui
import random

# Functions that compute RPSLS
def word_to_number(word):
    if word == "rock":
        return 1
    elif word == "paper":
        return 2
    elif word == "scissors":
        return 3
    elif word == "lizard":
        return 4
    elif word == "Spock":
        return 5
    else:        
        return 0
        
def number_to_word(number):
    if number == 1:
        return "rock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "scissors"
    elif number == 4:
        return "lizard"
    elif number == 5:
        return "Spock"
    else:
        print "Error: wrong number"
    
def RPSLS(word):
    player_number = word_to_number(word)
    print
    if player_number == 0:
        return "Error: Bad input"
    else:
        print "Player chose " + word      
        
        computer_number = random.randrange(1,6)
        computer_choice = number_to_word(computer_number)
        print "Computer chose " + computer_choice    
    
        dif = (player_number - computer_number) % 5
        if dif == 1 or dif == 2:
            return "Player wins!"
        elif dif == 0:
            return "Player and computer tie!"
        else:
            return "Computer wins!"
    
# Handler for input field
def get_guess(guess):
    print RPSLS(guess)

# Create frame and assign callbacks to event handlers
frame = simplegui.create_frame("GUI-based RPSLS", 200, 200)
frame.add_input("Enter guess for RPSLS", get_guess, 200)


# Start the frame animation
frame.start()


###################################################
# Test

get_guess("Spock")
get_guess("dynamite")
get_guess("paper")
get_guess("lazer")

###################################################
# Sample expected output from test
# Note that computer's choices may vary from this sample.

#Player chose Spock
#Computer chose paper
#Computer wins!
#
#Error: Bad input "dynamite" to rpsls
#
#Player chose paper
#Computer chose scissors
#Computer wins!
#
#Error: Bad input "lazer" to rpsls
#
