# Define an empty Tile class 
import simplegui
TILE_WIDTH = 50
TILE_HEIGHT = 100

#################################################
# Student adds code where appropriate

# definition of empty Tile class (use pass in the body)
class Tile:
    # initializer
    def __init__(self, num, exp, loc):
        self.number = num
        self.exposed = exp
        self.location = loc
    
    def get_number(self):
        return self.number
    
    def is_exposed(self):        
        return self.exposed
    
    def expose_tile(self):
        self.exposed = True        
    
    def hide_tile(self):
        self.exp = False
    
    def __str__(self):
        return "Number is " + str(self.number) + ", exposed is " + str(self.exposed)
    
    def draw_tile(self, canvas):
        loc = self.location
        if self.is_exposed():
            tex_location = [loc[0] + 0.2 * TILE_WIDTH, loc[1] - 0.3 * TILE_HEIGHT]
            canvas.draw_text(str(self.number), text_location, TILE_WIDTH, "White")
        else:
            tile_corners = (loc, [loc[0] + TILE_WIDTH, loc[1]], [loc[0] + TILE_WIDTH, loc[1] - TILE_HEIGHT], [loc[0], loc[1] - TILE_HEIGHT])
            canvas.draw_polygon(tile_corners, 1, "Red", "Green")
    
    def is_selected(self, pos):
        inside_hor = self.location[0] <= pos[0] < self.location[0] + TILE_WIDTH        
        inside_vert = self.location[1] - TILE_HEIGHT <= pos[1] <= self.location[1]
        # self.location[1] - TILE_HEIGHT = 0
        return inside_hor and inside_vert        
    
my_tile = Tile(3, True)      
your_tile = Tile(4, False)
tile_number = my_tile.get_number()
tile1 = Tile(3, True, [0, TILE_HEIGHT])
tile2 = Tile(5, False, [TILE_WIDTH, TILE_HEIGHT])
def draw(canvas):
    tile1.draw_tile(canvas)
    tile2.draw_tile(canvas)
def mouseclick(pos):
    if tile1.is_selected(pos):
        tile1.hide_tile()
    if tile2.is_selected(pos):
        tile2.expose_tile()
frame = simplegui.create_frame("Memory", 2 * TILE_WIDTH, TILE_HEIGHT)    
frame.set_draw_handler(draw) 
frame.set_mouseclick_handler(mouseclick)
frame.start()   
    
    
###################################################
# Testing code

print Tile


####################################################
# Output of testing code

# <class '__main__.Tile'>