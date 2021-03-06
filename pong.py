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
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [1, -1] # pixels per update (1/60 seconds)
paddle1_pos = (HEIGHT/2)
paddle2_pos = (HEIGHT/2)
paddle1_vel = 0
paddle2_vel = 0



# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists

    # start ball position in middle of canvas
    ball_pos = [WIDTH / 2, HEIGHT / 2]

    # randomly assign velocity based on direction
    if direction == RIGHT :
        ball_vel = [random.randrange(2, 5), - random.randrange(1, 4)]
    else:
        ball_vel = [- random.randrange(2, 5), - random.randrange(1, 4)]



# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    # reset score
    score1 = 0
    score2 = 0

    # spawn ball
    spawn_ball(RIGHT)



def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "Green")

    # collide and reflect off of top and bottom of canvas
    # top
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    # bottom
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]

    # update paddle's vertical position, keep paddle on the screen
    # paddle 1 top and bottom restraint
    if paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT and\
    paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    # paddle 2 top and bottom restraint
    if paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT and\
    paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel

    # draw paddles
    # paddle1 -- left paddle
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT],
                         [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT],
                         [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT],
                         [0, paddle1_pos + HALF_PAD_HEIGHT]],
                         1, 'White', 'White')
    # paddle2 -- right paddle
    canvas.draw_polygon([[(WIDTH - PAD_WIDTH), paddle2_pos - HALF_PAD_HEIGHT],
                         [WIDTH, paddle2_pos - HALF_PAD_HEIGHT],
                         [WIDTH, paddle2_pos + HALF_PAD_HEIGHT],
                         [(WIDTH - PAD_WIDTH), paddle2_pos + HALF_PAD_HEIGHT]],
                         1, 'White', 'White')

    # determine whether paddle and ball collide
    # paddle1 -- left paddle
    if (ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and\
    ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT) and\
    (ball_pos[0] - BALL_RADIUS) <= PAD_WIDTH:
        ball_vel[0] = - (ball_vel[0] * 1.10)
    elif ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        score2 += 1
        spawn_ball(RIGHT)
    # paddle2 -- right paddle
    if (ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and\
    ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT) and\
    (ball_pos[0] + BALL_RADIUS) >= WIDTH - PAD_WIDTH:
        ball_vel[0] = - (ball_vel[0] * 1.10)
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        score1 += 1
        spawn_ball(LEFT)

    # draw scores
    # left paddle -- player1 score
    canvas.draw_text(str(score1), [200, 50], 50, "White")
    # right paddle -- player2 score
    canvas.draw_text(str(score2), [375, 50], 50, "White")



def button_handler():
    new_game()



def keydown(key):
    global paddle1_vel, paddle2_vel

    paddle_speed = 4
    # paddle1
    if key==simplegui.KEY_MAP["W"]:
        paddle1_vel -= paddle_speed
    elif key==simplegui.KEY_MAP["S"]:
        paddle1_vel += paddle_speed

    # paddle2
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= paddle_speed
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += paddle_speed



def keyup(key):
    global paddle1_vel, paddle2_vel

    paddle_speed = 4
    # paddle1
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel += paddle_speed
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel -= paddle_speed

    # paddle2
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel += paddle_speed
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel -= paddle_speed



# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("New Game", button_handler, 100)



# start frame
new_game()
frame.start()
