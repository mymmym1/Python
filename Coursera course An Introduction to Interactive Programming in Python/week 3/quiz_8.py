import simplegui
# global state
n = 1
#iteration = 0
#max_iterations = 10

# helper functions
def init(start):
    global n
    n = start
    print "Input is", n
def get_next(current):
    if current % 2 == 0:
        current = current / 2
        return current
    else:
        current = current * 3 + 1
        return current

# timer callback
def update():
    global n
    n = get_next(n)
    if n == 1:
        timer.stop()
    print n

timer = simplegui.create_timer(1, update)
init(217)
timer.start()