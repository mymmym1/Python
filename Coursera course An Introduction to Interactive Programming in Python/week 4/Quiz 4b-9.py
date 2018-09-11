import simplegui
a = 5

def keydown(key):
    global a
    if key == simplegui.KEY_MAP["space"]:
        a = a*2
        print a
def keyup(key):
    global a
    if key == simplegui.KEY_MAP["space"]:
        a -= 3
        print a
def draw(canvas):
    #text = str(a)    
    canvas.draw_text(str(a), [120,160], 24, "white")

frame = simplegui.create_frame("what", 300, 300)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.start()

