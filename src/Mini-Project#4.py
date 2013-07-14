# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    # random initial velocity
    ball_vel[0] = random.randrange(120, 240) / 60
    ball_vel[1] = random.randrange(60, 180) / -60
    
    if right == False:
        ball_vel[0] = - ball_vel[0] 

# define event handlers

def restart_handler():
    new_game()

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    global ball_pos, ball_vel #these are lists
    
    # restart global variables
    ball_pos = [0, 0]
    ball_vel = [0, 0]
 
    paddle1_pos = (HEIGHT / 2) - (PAD_HEIGHT / 2)
    paddle2_pos = paddle1_pos
    
    paddle1_vel = 0
    paddle2_vel = 0
    
    score1 = 0
    score2 = 0
    
    ball_init(True)
    
# increase velocity by 10%
def increase_ball_vel():
    global ball_vel
            
    ball_vel[0] += (ball_vel[0] * 10) / 100 
    ball_vel[1] += (ball_vel[1] * 10) / 100 

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
     
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= 0 and paddle1_pos + paddle1_vel + PAD_HEIGHT <= HEIGHT:
        paddle1_pos += paddle1_vel 
    
    if paddle2_pos + paddle2_vel >= 0 and paddle2_pos + paddle2_vel + PAD_HEIGHT <= HEIGHT:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    c.draw_polygon([[0, paddle1_pos], [PAD_WIDTH, paddle1_pos], [PAD_WIDTH, paddle1_pos + PAD_HEIGHT], [0, paddle1_pos + PAD_HEIGHT]], 1, "White", "White")
    c.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos], [WIDTH, paddle2_pos], [WIDTH, paddle2_pos + PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT]], 1, "White", "White")
     
    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # collide and reflect the ball
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH + 1:
        if ball_pos[1] < paddle1_pos or ball_pos[1]  > paddle1_pos + PAD_HEIGHT:
            # left paddle lose
            ball_init(True)
            score2 += 1
        else:
            # reflect and increase velocity
            ball_vel[0] = - ball_vel[0] 
            increase_ball_vel()
            
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH - 1:
        if ball_pos[1] < paddle2_pos or ball_pos[1] > paddle2_pos + PAD_HEIGHT:
            # right paddle lose
            ball_init(False)
            score1 += 1
        else:
            # reflect and increase velocity
            ball_vel[0] = - ball_vel[0] 
            increase_ball_vel()
            
    elif ball_pos[1] <= BALL_RADIUS + 1:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] + BALL_RADIUS >= HEIGHT - 1:
        ball_vel[1] = - ball_vel[1]
            
    # draw ball and scores
    c.draw_text(str(score1), (WIDTH / 2 - 160, 55), 40, "White")
    c.draw_text(str(score2), (WIDTH / 2 + 135, 55), 40, "White")
    
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -5
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 5
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -5
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 5  
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0  

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart Game", restart_handler, 150)

#start game
new_game()

# start frame
frame.start()