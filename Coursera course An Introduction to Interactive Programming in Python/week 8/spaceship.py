# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
rock_group = set([])
missile_group = set([])
explosion_group = set()

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
flame_ship_info = ImageInfo([135, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):        
        if self.thrust == False:
            canvas.draw_image(ship_image, ship_info.get_center(), ship_info.get_size(), self.pos, ship_info.get_size(), self.angle)
        else:
            canvas.draw_image(ship_image, flame_ship_info.get_center(), ship_info.get_size(), self.pos, ship_info.get_size(), self.angle)            
            
    def update(self):           
        self.angle += self.angle_vel         
        if self.thrust == True:                 
            self.vel[0] += 0.1 * angle_to_vector(self.angle)[0]
            self.vel[1] += 0.1 * angle_to_vector(self.angle)[1]
        else:    
            # multiply a number < 1 to add friction
            self.vel[0] *= 0.9
            self.vel[1] *= 0.9
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
    def decrease_angle_vel(self):
        self.angle_vel -= 0.07
        
    def increase_angle_vel(self):
        self.angle_vel += 0.07
        
    def thrusters_on(self, thrust):
        self.thrust = thrust   
        if self.thrust == True:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            
    def shoot(self):
        global a_missile, missile_group        
        missile_pos = [self.pos[0], self.pos[1]]
        missile_vel = [1, 1]
        missile_vel[0] = self.vel[0] + 10 * angle_to_vector(self.angle)[0]
        missile_vel[1] = self.vel[1] + 10 * angle_to_vector(self.angle)[1]
        missile_pos[0] = self.pos[0] + self.radius * angle_to_vector(self.angle)[0]
        missile_pos[1] = self.pos[1] + self.radius * angle_to_vector(self.angle)[1]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, self.angle_vel, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        if self.animated:
            center = [64,64]
            self.age = (time%24)//1
            center[0] = 64 + self.image_size[0]*self.age
            canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)        
        
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        if self.age >= self.lifespan:            
            return True        
        
    def collide(self, other_object):
            if dist(self.pos, other_object.pos) <= self.radius + other_object.radius:
                return True

def group_collide(group_rock, other_object):   
    count = 0
    for i in set(group_rock):
        if i.collide(other_object):
            group_rock.remove(i)
            count += 1
            explosion_group.add(Sprite(i.pos, [0, 0], 0, 0, explosion_image,
                                       explosion_info, explosion_sound))
    return count

def group_group_collide(group_missile, group_rock):  
    count = 0
    for a in set(group_missile):
        count = group_collide(group_rock, a)
        if count >0:
            group_missile.remove(a)        
    return count
    
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrease_angle_vel()
    if key == simplegui.KEY_MAP['right']:
        my_ship.increase_angle_vel()
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrusters_on(True)
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increase_angle_vel() 
    if key == simplegui.KEY_MAP['right']:
        my_ship.decrease_angle_vel() 
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrusters_on(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        timer.start()
        lives = 3
        score = 0
        
def draw(canvas):
    global time, started, rock_group, lives, score, missile_group, rock_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Lives", [50,60], 20, "white")
    canvas.draw_text("Score", [680,60], 20, "white")
   
    if group_collide(rock_group, my_ship) and lives > 0:
        lives -= 1

    elif lives == 0:
        rock_group = set([])
        started = False        
        timer.stop()
        
    canvas.draw_text(str(lives), [50,80], 20, "white")       
    score += group_group_collide(missile_group, rock_group)
    canvas.draw_text(str(score), [680,80], 20, "white")
    
    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(missile_group, canvas)    
    
    # update ship and sprites
    my_ship.update()    
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())  
        soundtrack.rewind()

    elif started:
        process_sprite_group(rock_group, canvas)
        soundtrack.play()
        process_sprite_group(explosion_group, canvas)       
        
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock, pos, ang_vel, vel, rock_group, started, my_ship, score    
    pos = [WIDTH / 3, HEIGHT / 3]
    pos[0] = random.randrange(0, WIDTH)
    pos[1] = random.randrange(0, HEIGHT) 
    ang_vel = 0
    ang_vel = random.random() * 0.1 * random.choice([-1,1])
    vel = [1, 1]
    n = score // 10 + 1
    vel[0] = random.random() *n* random.choice([-1,1])
    vel[1] = random.random() *n* random.choice([-1,1])
    a_rock = Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info)
    if dist(a_rock.pos, my_ship.pos) <= a_rock.radius + my_ship.radius:
        a_rock.pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    if len(rock_group) < 12:
        rock_group.add(a_rock)   

def process_sprite_group(group, canvas):
    for sprite in set(group):
        sprite.draw(canvas)
        if sprite.update():
            group.remove(sprite)    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.1, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH, 2 * HEIGHT], [0,0], 0, 0, missile_image, missile_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
frame.start()
