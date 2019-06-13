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
show_menu = True
accelerate = False
decelerate = False
jumping = False
falling = False
carole_is_dying = False
second = 0
# cheats and fun stuff
carole_is_flying = False
cheats_activated = False
ddup = True # death do us part (as in carole and teh motorcycle)


# timer for seconds since stort:
timer = 0
current_score = 0
high_score = 0

# keep track of mouse for other functions:
mouse_x = 0
mouse_y = 0
mouse_pressed = False
mouse_released = False



# list of possoble images for obstacles (add more maybe?):
obstacle_images = [
'images/barrel.png',
'images/box.png',
]

""" classes (not the schule kind, other kind, haha funny joke, wait, no it was terrible, this is going on for too long,
    how much more space is this gonna take? you're negatively impacting the program stop! seriously, you're gonna lose
    marks, what are you doing? gosh darnit stop. fine do it."""

class Button(object):
    # BBBBBBBBBUTTUN

    def __init__(self, center_x, center_y, width, height):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.color = arcade.color.GRAY
        self.hover_color = self.color
        self.pressed_color = self.color
        self.visible = False

    def draw(self):
        if self.visible:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)

    def update(self):
        # not pressed is 0; hovering is 1; pressed is 2; released is 3
        global mouse_released

        if self.center_x - self.width/2 < mouse_x < self.center_x + self.width/2 and \
        self.center_y - self.height/2 < mouse_y < self.center_y + self.height/2:
            if mouse_released:
                mouse_released = False
                return 3
            elif mouse_pressed:
                self.color = self.pressed_color
                return 2
            else:
                self.color = self.hover_color
                return 1

        else:
            return 0


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

part_list = arcade.SpriteList()
obstacle_list = arcade.SpriteList()

# create signpost
menu_list = arcade.SpriteList()

signpost = arcade.Sprite('images/signpost.png', SCALE*4)
signpost.center_x = WIDTH/2 + 20
signpost.center_y = HEIGHT/2 + 20
menu_list.append(signpost)

sign = arcade.Sprite('images/roadtoeternity.png')
menu_list.append(sign)

button = Button(WIDTH/2, HEIGHT*0.75, 683, 194) # the whacky numbers are the tingies for the picture

""" moke the FUNctions """

def fly_carole_fly():
    carole = part_list[3]
    body = part_list[2]
    carole.change_x += 0.1
    if jumping and 0 <= carole.change_y:
        carole.change_y += 4.5
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


def add_points(points):
    global current_score, high_score, cheats_activated

    if cheats_activated:
        current_score = 0
    else:
        current_score += points
        if current_score > high_score:
            high_score = current_score


""" make the fanctions """

def menu():
    global sign, show_menu


    button_condition = button.update()
    menu_list[1].kill()
    if button_condition ==  0:
        sign = arcade.Sprite('images/roadtoeternity.png')
    elif button_condition == 1:
        sign = arcade.Sprite('images/roadtoeternity(hover).png')
    elif button_condition == 2:
        sign = arcade.Sprite('images/roadtoeternity(clicked).png')
    elif button_condition == 3:
        show_menu = False
        reset()

    menu_list.append(sign)

    sign.center_x = WIDTH / 2
    sign.center_y = HEIGHT * 0.75

    menu_list.draw()

def reset():
    global part_list, obstacle_list, carole_is_dying, timer, current_score, cheats_activated

    carole_is_dying = False
    cheats_activated = False
    timer = 0
    current_score = 0

    # create obstacle lirt:
    obstacle_list = arcade.SpriteList()

    # create the motarcycle parts:
    part_list = arcade.SpriteList()

    # create the toires:
    tire_behind = arcade.Sprite('images/wheel.png', SCALE)
    tire_front = arcade.Sprite('images/wheel.png', SCALE)
    part_list.append(tire_behind);
    part_list.append(tire_front)

    # create the boody
    body = arcade.Sprite('images/motorcycle.png', SCALE)
    body.center_x = MOTOR_X;
    body.center_y = MOTOR_Y
    part_list.append(body)

    # create carole (yes. that is his name)
    carole = arcade.Sprite('images/carole.png', SCALE / 2)
    part_list.append(carole)

    update_motorcycle()


def game_over():
    global carole_is_dying, show_menu

    carole = part_list[3]

    if ddup:
        show_menu = True
        carole.change_angle = 20
        carole.change_x = -20
        carole.center_y = GROUND
        carole_is_dying = True
        carole.update()
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
    carole = part_list[3]
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
    window.on_mouse_motion = on_mouse_motion
    window.on_mouse_press = on_mouse_press
    window.on_mouse_release = on_mouse_release

    arcade.run()


def update(delta_time):
    global timer

    for particle in dust_list:
        particle.update()

    if show_menu:
        menu()
    else:
        update_obstacles()
        check_carole_collision()
        update_motorcycle()
        timer += 1
        add_points(1)

    if carole_is_dying:
        game_over()

    if carole_is_flying:
        fly_carole_fly()

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

    if show_menu:
        menu()
    else:
        global current_score, high_score

        font_size = 20
        arcade.draw_text(str(current_score), 10, HEIGHT - font_size - 20, arcade.color.BLACK, font_size = font_size)
        arcade.draw_text(str(high_score), 10, HEIGHT - 2*font_size - 30, arcade.color.BLACK, font_size = font_size)

def on_key_press(key, modifiers):
    global accelerate, decelerate, jumping, falling, carole_is_flying # actooal stuff
    global cheats_activated, ddup # chets

    # cheat codes:
    if key == arcade.key.D:
        if ddup:
            ddup = False
        else:
            ddup = True

        cheats_activated = True

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


def on_mouse_motion(x, y, dx, dy):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y


def on_mouse_press(x, y, button, modifiers):
    global mouse_pressed, mouse_released
    mouse_pressed = True
    mouse_released = False

def on_mouse_release(x, y, button, modifiers):
    global mouse_pressed, mouse_released
    mouse_pressed = False
    mouse_released = True


if __name__ == '__main__':
    setup()
