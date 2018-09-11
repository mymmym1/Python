import simplegui

p = [350,350]
v = [0.5,3]
t = 1
acceleration = 0.5
v = [v[0]+t*acceleration, v[1]+t*acceleration]  
velocity = [6,0.5]

def draw(canvas):    
    global p,v    
    p = [p[0]+t*v[0], p[1]+t*v[1]]
    canvas.draw_circle(p, 4, 4, "red", "red")

def tick():
    global v, velocity
    v = [v[0]+velocity[0], v[1]+velocity[1]]

frame = simplegui.create_frame("shape", 700, 700)
timer = simplegui.create_timer(100, tick)
frame.set_draw_handler(draw)
frame.start()
timer.start()
