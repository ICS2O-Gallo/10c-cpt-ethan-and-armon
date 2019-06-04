import random
import arcade
import math


WIDTH = 1366
HEIGHT = 710
SCALE = HEIGHT/WIDTH/1.1
RIGHTCAP = WIDTH*0.85

MOTOR_SPEED = 0.3
MOTOR_SPEED_CAP = 10
MOTOR_ANGLE = 1
MOTOR_JUMP = 3
MOTOR_FALL = -4


# Conditional varioobles:
Accelerate = False
Decelerate = False
Jumping = False
Falling = False
Second = 0

class Dust(object):
    # DDDDDDDOST

    def __init__(self):
        # Create a random spawning point
        self.x = random.randrange(WIDTH, 1.5*WIDTH)
        self.y = random.randrange(HEIGHT)

        # set dust width to be able to delete it off screen
        self.dust_radius = 8

        self.speed = random.randrange(10, 17)
        self.fall = random.uniform(-0.5, -0.1)

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.dust_radius, arcade.color.EARTH_YELLOW)

    def update(self):
        self.x -= self.speed
        self.y += self.fall
        if self.x < -self.dust_radius or self.y < -self.dust_radius:
            self.__init__()


""" initiate the stuffses """
dust_list = []
for particle in range(30):
    particle = Dust()
    dust_list.append(particle)


# create the motorcycle parts:

part_list = arcade.SpriteList()

# create the tires:
tire_behind = arcade.Sprite("images/motorcycle_wheel.png", SCALE)
tire_front = arcade.Sprite("images/motorcycle_wheel.png", SCALE)
part_list.append(tire_behind); part_list.append(tire_front)

# create the body

body = arcade.Sprite("images/motorcycle_drawing_new.png", SCALE)
body.center_x = WIDTH/8; body.center_y = HEIGHT/8
part_list.append(body)
""" make the fanctions """


def jump(part):
    global Falling, Jumping

    if Jumping:

        if part.center_y >= HEIGHT/5:
            part.change_angle = MOTOR_ANGLE/2
            part.change_y = MOTOR_JUMP * 2
        else:
            part.change_angle = MOTOR_ANGLE
            part.change_y = MOTOR_JUMP * 4

        if part.center_y >= HEIGHT/4:
            Jumping = False
            Falling = True

    if Falling:
        Jumping = False
        if part.center_y >= HEIGHT/5:
            part.change_angle = -MOTOR_ANGLE/2
            part.change_y += (MOTOR_FALL/10)
        else:
            part.change_angle = -MOTOR_ANGLE
            part.change_y = MOTOR_FALL * 4

        if part.center_y <= HEIGHT/8:
            part.change_angle = 4
            part.change_y = 0
            if part.angle >= 0:
                part.change_angle = 0
                Falling = False



def game_over():
    exit(1)


def draw_ground():
    arcade.draw_lrtb_rectangle_filled(0, WIDTH, HEIGHT/6, 0, arcade.color.LIGHT_BROWN)

# motorcycle movement:

def update_motorcycle():
    part = part_list[2]
    part.change_x -= 0.05


    if Accelerate:
        part.change_x += MOTOR_SPEED
    if Decelerate:
        part.change_x -= 2*MOTOR_SPEED  # we brake quacker
    else:
        if part.change_x < -2:
            part.change_x += 0.2
            if part.change_x > -2 and Accelerate == False:
                part.change_x = -2

    # make sure not goin too darnerino fasterino

    if part.change_x > MOTOR_SPEED_CAP:
        part.change_x = MOTOR_SPEED_CAP
    if part.change_x < -MOTOR_SPEED_CAP:
        part.change_x = -MOTOR_SPEED_CAP

    # Jomp!

    jump(part)

    # check if off the loft side of the screen:
    global Second
    if part.center_x < 0:
        if Second >= 120:
            game_over()
            Second = 0
        Second += 1

    # check if near the roite side of the screen
    if part.center_x > RIGHTCAP:
        part.change_x -= 2.5*MOTOR_SPEED

    # manage dost (in motorcycle function, WWHHHHATTTTT?????)
    for particle in dust_list:
        if Accelerate:
            particle.speed += MOTOR_SPEED/1.5
        if Decelerate:
            particle.speed -= MOTOR_SPEED
        if particle.speed >= 30:
            particle.speed -= MOTOR_SPEED*2
        if particle.speed < 10:
            particle.speed += MOTOR_SPEED*4


    # very camplicated math thing that I made to make sure tires are at the right spot.
    # won't wurk if the screeen resolution is different so DON'T CHANGE IT JESUS CHRIST
    set_wheels(part_list[0], part_list[1], part_list[2])
    # TESTING:



    # update the part:
    for part in part_list:
        part.update()


def set_wheels(wheel1, wheel2, body):
    """complicated math to do stoff"""
    wheel1.center_x = body.center_x + 94.55337264*(math.cos(math.radians(body.angle + 205.977886)))
    wheel1.center_y = body.center_y + 94.55337264*(math.sin(math.radians(body.angle + 205.977886)))
    print(body.center_x - wheel1.center_x)
    print(body.center_y - wheel1.center_y)

    # front tire

    wheel2.center_x = body.center_x + 72.90638023*(math.cos(math.radians(body.angle + 325.3835437)))
    wheel2.center_y = body.center_y + 72.90638023*(math.sin(math.radians(body.angle + 325.3835437)))
    print(body.angle)

""" Run the actual game """


def setup():
    arcade.open_window(WIDTH, HEIGHT, "Road to Eternity")
    arcade.set_background_color(arcade.color.ARYLIDE_YELLOW)
    arcade.schedule(update, 1/60)


    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_press = on_mouse_press

    arcade.run()


def update(delta_time):

    for particle in dust_list:
        particle.update()

    update_motorcycle()


def on_draw():
    arcade.start_render()

    # Draw far dost:
    for particle in dust_list:
        if particle.speed >= -2:
            particle.draw()

    # Draw The Ground (OH REALLY?)
    draw_ground()

    for part in part_list:
        part.draw()

    # Draw close Dost
    for particle in dust_list:
        if particle.speed < -2:
            particle.draw()


def on_key_press(key, modifiers):
    global Accelerate, Decelerate, Jumping

    if key == arcade.key.UP:
        if Falling == False:
            Jumping = True
    else:
        if key == arcade.key.RIGHT:
            Accelerate = True
        if key == arcade.key.LEFT:
            Decelerate = True


def on_key_release(key, modifiers):
    global Accelerate, Decelerate

    if key == arcade.key.RIGHT:
        Accelerate = False
    if key == arcade.key.LEFT:
        Decelerate = False


def on_mouse_press(x, y, button, modifiers):
    pass


def on_mouse_release(x, y, button, modifiers):
    pass


if __name__ == '__main__':
    setup()




"""Elevate
def jump(part):
    global Falling, Jumping
    if Jumping:
        if part.center_y >= HEIGHT/4:
            part.change_angle = MOTOR_ANGLE/2
            part.change_y = MOTOR_JUMP * 2
        else:
            part.change_angle = MOTOR_ANGLE
            part.change_y = MOTOR_JUMP * 4
        if part.center_y >= HEIGHT/3:
            Jumping = False
            Falling = True
    if Falling:
        if part.center_y >= HEIGHT/4:
            part.change_angle = -MOTOR_ANGLE/2
            part.change_y -= (MOTOR_FALL/10)
        else:
            part.change_angle = -MOTOR_ANGLE
            part.change_y = MOTOR_FALL * 4
        if part.center_y <= HEIGHT/8:
            part.change_angle = 0
            part.change_y = 0
            Falling = False
"""
