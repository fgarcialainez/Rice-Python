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

a_rock = None
a_missile = None

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
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

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
        if self.thrust:
            # Draw the ship with thrusts image when thrusts are on
            image_center_thrust = [self.image_center[0] + 90, self.image_center[1]]
            canvas.draw_image(self.image, image_center_thrust, self.image_size, self.pos, self.image_size, self.angle)
        else:
            # Draw the simple ship image when thrusts are off 
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)            

    def update(self):
        # Update the position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # Control that the Ship is always on the screen
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        
        # Update the angle 
        self.angle += self.angle_vel
        
        # Update the velocity if the thrusts are activated
        if self.thrust:
            direction_vector = angle_to_vector(self.angle)
            self.vel[0] += direction_vector[0] / 10
            self.vel[1] += direction_vector[1] / 10
            
        # Friction
        self.vel[0] *= 0.99
        self.vel[1] *= 0.99
        
    def rotate_clockwise(self, rotate):
        if rotate:
            self.angle_vel = 0.1
        else:
            if self.angle_vel == 0.1:
                self.angle_vel = 0
        
    def rotate_counter_clockwise(self, rotate):
        if rotate:
            self.angle_vel = -0.1
        else:
            if self.angle_vel == -0.1:
                self.angle_vel = 0
                
    def activate_thrust(self, activate):
        self.thrust = activate
        
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
    
    def shoot(self):
        global a_missile
        
        direction_vector = angle_to_vector(self.angle)  
        
        # Calculate initial positio of the missile
        missile_pos = [self.pos[0] + direction_vector[0] * 45, self.pos[1] + direction_vector[1] * 45]
        
        # Calculate velocity of the missile
        missile_vel = [self.vel[0] + direction_vector[0] * 6, self.vel[1] + direction_vector[1] * 6]
         
        # Create the new missile
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
    
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
    
    def update(self):
        # Update the position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # Control that the Sprite is always on the screen
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        
        # Update the angle 
        self.angle += self.angle_vel     

# Handlers
def key_up_handler(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.rotate_counter_clockwise(False)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.rotate_clockwise(False)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.activate_thrust(False)
    
def key_down_handler(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.rotate_counter_clockwise(True)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.rotate_clockwise(True)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.activate_thrust(True)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    
def draw(canvas):
    global time, a_rock, a_missile, lives
    
    # animate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw and update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    
    if a_rock != None:
        a_rock.draw(canvas)
        a_rock.update()  
    
    if a_missile != None:
        a_missile.draw(canvas)
        a_missile.update()
        
    # draw number of lives and score
    canvas.draw_text("Lives", (40, 40), 22, "White")
    canvas.draw_text(str(lives), (40, 67), 22, "White")
    
    canvas.draw_text("Score", (710, 40), 22, "White")
    canvas.draw_text(str(score), (710, 67), 22, "White")
            
# timer handler that spawns a rock    
def rock_spawner():
    spawn_rock()
    
def spawn_rock():
    global a_rock
    
    # Generate random position for the rock
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    
    # Generate random velocity for the rock (between -1 and 1)
    rock_vel = [(random.random() * 2) - 1, (random.random() * 2) - 1]
    
    # Generate random rotation angle velocity (between -0.1 and 0.1)
    ang_vel =  ((random.random() * 2) - 1) / 10   
    
    # Create the new rock
    a_rock = Sprite(rock_pos, rock_vel, 0, ang_vel, asteroid_image, asteroid_info)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)

frame.set_keydown_handler(key_down_handler)
frame.set_keyup_handler(key_up_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
