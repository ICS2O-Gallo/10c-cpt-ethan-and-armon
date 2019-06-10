import random
import arcade
import math
import numpy

""" the holy greyl of intentional spelling mistakes """
WIDTH = 1366
HEIGHT = 710
SCALE = HEIGHT/WIDTH/1.1
RIGHTCAP = WIDTH*0.85

MOTOR_X = WIDTH/8
MOTOR_Y = HEIGHT/8
MOTOR_SPEED = 1
MOTOR_SPEED_CAP = 10
MOTOR_ANGLE = 1
MOTOR_JUMPCAP = HEIGHT/4
MOTOR_JUMPCAP_SLOW = HEIGHT/5
MOTOR_JUMP = 12
MOTOR_FALL = -5

OBSTACLE_SPEED = -10

GROUND = HEIGHT/6

# Conditional varioobles:
accelerate = False
decelerate = False
jumping = False
falling = False
carole_is_dying = False
second = 0
# cheats and fun stuff
carole_is_flying = False
ddup = True # death do us part (as in carole and teh motorcycle)


# timer for seconds since stort:
timer = 0


# list of possoble images for obstacles (add more maybe?):
obstacle_images = [
'images/barrel.png',
'images/box.png',
]


class Dust(object):
    # DDDDDDDOST

    def __init__(self):
        # Create a random spooning point
        self.x = random.randrange(WIDTH, 1.5*WIDTH)
        self.y = random.randrange(HEIGHT)

        # set dust width to be able to delete it off screen
        self.dust_radius = 8

        self.speed = random.randint(10, 17)
        self.fall = random.uniform(-0.5, -0.1)

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.dust_radius, arcade.color.EARTH_YELLOW)

    def update(self):
        if accelerate:
            self.speed += MOTOR_SPEED/1.5
        if decelerate:
            self.speed -= MOTOR_SPEED
        if self.speed >= 30:
            self.speed -= MOTOR_SPEED*2
        if self.speed < 10:
            self.speed += MOTOR_SPEED*4
        self.x -= self.speed
        self.y += self.fall
        if self.x < -self.dust_radius or self.y < -self.dust_radius:
            self.__init__()


""" initiate the stuffses """

dust_list = []
for particle in range(30):
    particle = Dust()
    dust_list.append(particle)

# create obstacle lirt:
obstacle_list = arcade.SpriteList()

# create the motarcycle parts:
part_list = arcade.SpriteList()

# create the toires:
tire_behind = arcade.Sprite('images/wheel.png', SCALE)
tire_front = arcade.Sprite('images/wheel.png', SCALE)
part_list.append(tire_behind); part_list.append(tire_front)

# create the boody
body = arcade.Sprite('images/motorcycle.png', SCALE)
body.center_x = MOTOR_X; body.center_y = MOTOR_Y
part_list.append(body)

# create carole (yes. that is his name)
carole = arcade.Sprite('images/carole.png', SCALE/2)
part_list.append(carole)

""" moke the FUNctions """

def fly_carole_fly():
    carole = part_list[3]
    body = part_list[2]
    carole.change_x += 0.1
    if jumping and 0 <= carole.change_y:
        carole.change_y += 3.6
    if falling:
        carole.change_y -= 1
    if carole.center_y <= body.center_y - 18:
        global carole_is_flying

        carole.change_x = 0
        carole.change_y = 0
        carole.center_y = body.center_y + 10
        catch = arcade.check_for_collision(carole, part_list[2])
        if catch:
            if carole.center_x <= body.center_x - 50 or carole.center_x >= body.center_x + 50:
                game_over()

        else:
            game_over()

        carole_is_flying = False






""" make the fanctions """

def game_over():
    global carole_is_dying

    carole = part_list[3]

    if ddup:
        carole.change_angle = 20
        carole.change_x = -20
        carole.center_y = GROUND
        carole_is_dying = True
        carole.update()
        if carole.center_x < -WIDTH:
            exit(1)
    else:
        print("We can never be torn apart. and now this message will repeat a thousand times to show the strength of"
              " our love")


# colision function:
def check_carole_collision():
    carole = part_list[3]

    hit = arcade.check_for_collision_with_list(carole, obstacle_list)
    if len(hit) > 0:
        game_over()


# crete obstacles:
def create_obstacle():
    type = obstacle_images[random.randint(0, 1)]
    obstacle = arcade.Sprite(type, SCALE*5/3)
    obstacle.center_x = WIDTH + 66
    if type == obstacle_images[0]:
        obstacle.center_y = GROUND - 65
    elif type == obstacle_images[1]:
        obstacle.center_y = GROUND - 80
    obstacle_list.append(obstacle)


# reset obstucles:
def reset_obstacle(obstacle):
    obstacle.kill()


# obstocle thing:
def update_obstacles():
    if (numpy.random.choice(a=[0, 1], p=[0.98, 0.02])):
            create_obstacle()

    for obstacle in obstacle_list:
        obstacle.center_x += OBSTACLE_SPEED - timer/600
        if obstacle.center_x + 33 <= 0:
            reset_obstacle(obstacle)


def draw_ground():
    arcade.draw_lrtb_rectangle_filled(0, WIDTH, GROUND, 0, arcade.color.LIGHT_BROWN)


# next section is all about moturcycle movement:
def jump(body):
    global falling, jumping

    if jumping:

        if body.center_y >= MOTOR_JUMPCAP_SLOW:
            body.change_angle = MOTOR_ANGLE/2
            body.change_y = MOTOR_JUMP/2
        else:
            body.change_angle = MOTOR_ANGLE
            body.change_y = MOTOR_JUMP

        if body.center_y >= HEIGHT/4:
            jumping = False
            falling = True

    if falling:
        jumping = False
        if body.center_y >= MOTOR_JUMPCAP_SLOW:
            body.change_angle = -MOTOR_ANGLE/2
            body.change_y += (MOTOR_FALL/10)
        else:
            body.change_angle = -MOTOR_ANGLE
            body.change_y = MOTOR_FALL * 4

        if body.center_y <= MOTOR_Y:
            body.center_y = MOTOR_Y
            body.change_angle = 4
            body.change_y = 0
            if body.angle >= 0:
                body.change_angle = 0
                falling = False


def update_motorcycle():

    body = part_list[2]
    body.change_x -= 0.05

    if accelerate:
        body.change_x += MOTOR_SPEED
    if decelerate:
        body.change_x -= 2*MOTOR_SPEED# we brake quacker
    else:
        if body.change_x < -2:
            body.change_x += 0.2
            if body.change_x > -2 and accelerate == False:
                body.change_x = -2

    # make sure not guin too darned fasterino
    if body.change_x > MOTOR_SPEED_CAP:
        body.change_x = MOTOR_SPEED_CAP
    if body.change_x < -MOTOR_SPEED_CAP:
        body.change_x = -MOTOR_SPEED_CAP

    # Jomp!
    jump(body)

    # check if off the loft side of the screen
    global second
    if carole.center_x < 0:
        if second >= 120:
            game_over()
            second = 0
        second += 1
    else:
        second = 0

    # check if near the roite side of the screen
    if body.center_x > RIGHTCAP:
        body.change_x -= 2.5*MOTOR_SPEED

    # very camplicated math thing that I made to make sure tires are at the right spot.
    # won't wurk if the screen resolution is different so DON'T CHANGE IT JESUS CHRIST
    set_wheels(part_list[0], part_list[1], body)
    if carole_is_flying == False:
        set_carole(part_list[3], body)
    # TESTING:



    # update parts part:
    for part in part_list:
        part.update()


def set_wheels(wheel1, wheel2, body):
    """complicated math to do stoff"""

    # back tire
    wheel1.center_x = body.center_x + 62.64982043*(math.cos(math.radians(body.angle + 208.6104597)))
    wheel1.center_y = body.center_y + 62.64982043*(math.sin(math.radians(body.angle + 208.6104597)))

    # front tire
    wheel2.center_x = body.center_x + 94.86832981*(math.cos(math.radians(body.angle + 341.5650512)))
    wheel2.center_y = body.center_y + 94.86832981*(math.sin(math.radians(body.angle + 341.5650512)))

    # change how fast it moves
    if accelerate:
        tire_speed = -60
    elif decelerate:
        tire_speed = -20
    else:
        tire_speed = -40

    wheel1.change_angle = wheel2.change_angle = tire_speed


def set_carole(carole, body):

    if not carole_is_dying:
        carole.center_x = body.center_x
        carole.center_y = body.center_y + 10
        carole.angle = body.angle


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
    global timer

    for particle in dust_list:
        particle.update()

    if not carole_is_dying:
        if carole_is_flying:
            fly_carole_fly()
        update_obstacles()
        check_carole_collision()
        update_motorcycle()
    else:
        game_over()

    timer += 1


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

    for obstacle in obstacle_list:
        obstacle.draw()

    # Draw close Dost
    for particle in dust_list:
        if particle.speed < -2:
            particle.draw()


    # Draw the minu:
    #if menu == True:



def on_key_press(key, modifiers):
    global accelerate, decelerate, jumping, falling, carole_is_flying # actooal stuff
    global ddup # chets

    # cheat codes:
    if key == arcade.key.D:
        if ddup:
            ddup = False
        else:
            ddup = True


    if key == arcade.key.UP:
        if jumping == True:
            carole_is_flying = True
        if falling == False:
            jumping = True
    else:
        if key == arcade.key.RIGHT:
            accelerate = True
        if key == arcade.key.LEFT:
            decelerate = True


def on_key_release(key, modifiers):
    global accelerate, decelerate

    if key == arcade.key.RIGHT:
        accelerate = False
    if key == arcade.key.LEFT:
        decelerate = False


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
