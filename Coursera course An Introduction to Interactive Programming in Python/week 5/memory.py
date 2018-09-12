# implementation of card game - Memory

import simplegui
import random
numbers = range(8) * 2
random.shuffle(numbers)
#print numbers
exposed = []
for i in range(16):
    exposed.append(False)
first_number_idx = 0
second_number_idx = 1
count = 0
    
# helper function to initialize globals
def new_game():
    global state, count, exposed, numbers
    state = 0 
    count = 0
    label.set_text("Turns = " + str(count))    
    random.shuffle(numbers)    
    for i in range(16):
        exposed[i] = False
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, first_number_idx, second_number_idx, count
    for i in range(16):
        if i*50 <= pos[0] <= (i+1)*50:
            #print i    
            if state == 0 and exposed[i] == False:
                state = 1
                exposed[i] = True
                first_number_idx = i
                #print "state: " + str(state) + " first_number: " + str(numbers[i])
            elif state == 1 and exposed[i] == False:
                state = 2
                exposed[i] = True
                second_number_idx = i  
                #print "state: " + str(state) + " second_number: " + str(numbers[i])
                count += 1
                label.set_text("Turns = " + str(count))
            else:
                if exposed[i] == False:
                    state = 1
                    exposed[i] = True
                    third_number_idx = i
                    if numbers[first_number_idx] != numbers[second_number_idx]:
                        exposed[first_number_idx] = False
                        exposed[second_number_idx] = False
                        first_number_idx = third_number_idx
                    else: 
                        exposed[first_number_idx] = True
                        exposed[second_number_idx] = True
                        first_number_idx = third_number_idx
                #print "state: " + str(state) + " frist_number: " + str(numbers[i])
            
# cards are logically 50x100 pixels in size    
def draw(canvas):    
    for i in range(16):
        if exposed[i] == True:
            canvas.draw_text(str(numbers[i]), [2 + 50 * i, 80], 80, "White")
        else:
            canvas.draw_line([25+50*i,0], [25+50*i,100], 50, "Green")
            canvas.draw_line([0,0], [800,0], 1, "Red")
            canvas.draw_line([0,100], [800,100], 1, "Red")
            canvas.draw_line([0,0], [0,100], 1, "Red")
            canvas.draw_line([800,0], [800,100], 1, "Red")
            canvas.draw_line([50*i,0], [50*i, 100], 1, "Red")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(count))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric