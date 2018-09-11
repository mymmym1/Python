import simplegui
p = [10, 20]
v = [3, 0.7]


def keydown(key):
    global p
    if key == simplegui.KEY_MAP["up"]:
        p = [p[0]+v[0],p[1]+v[1]]

def draw(canvas):
    canvas.draw_line([50,50], [180,50], 4, "white")
    canvas.draw_line([180,50], [180,140], 4, "white")
    canvas.draw_line([180,140], [50,140], 4, "white")
    canvas.draw_line([50, 140], [50,50], 4, "white")
    canvas.draw_circle(p, 2, 2, "red", "red")

frame = simplegui.create_frame("overlap", 300, 300)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.start()