import random
import arcade


WIDTH = 640
HEIGHT = 480
SCALE = 0.3

MOTOR_SPEED = 0.15
MOTOR_SPEED_CAP = 10


# Conditional varioobles:
Accelerate = False
Decelerate = False

class Dust(object):
    # DDDDDDDOST

    def __init__(self):
        # Create a random spawning point
        self.x = random.randrange(WIDTH, 2*WIDTH)
        self.y = random.randrange(HEIGHT)

        # set dust width to be able to delete it off screen
        self.dust_radius = 8

        self.speed = random.randrange(-7, -1)
        self.fall = random.uniform(-0.3, -0.1)

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.dust_radius, arcade.color.EARTH_YELLOW)

    def update(self):
        self.x += self.speed
        self.y += self.fall
        if self.x < -self.dust_radius or self.y < -self.dust_radius:
            self.__init__()


""" initiate the stuffses """


def draw_ground():
    arcade.draw_lrtb_rectangle_filled(0, WIDTH, HEIGHT/6, 0, arcade.color.LIGHT_BROWN)


dust_list = []
for particle in range(30):
    particle = Dust()
    dust_list.append(particle)

# create the motorcycle parts:
part_list = arcade.SpriteList()

body = arcade.Sprite("images/motorcycle_drawing_new.png", SCALE)
body.center_x = 50; body.center_y = 50
part_list.append(body)

# motorcycle movement:
def change_speed():
    for part in part_list:
        part.change_x -= 0.05

        if Accelerate:
            part.change_x += MOTOR_SPEED
        if Decelerate:
            part.change_x -= MOTOR_SPEED  # we brake quicker
            if part.change_x < -5:
                part.change_x = -5
        else:
            if part.change_x < -1:
                part.change_x += 0.3
                if part.change_x > -1 and Accelerate == False:
                    part.change_x = -1

        if part.change_x > MOTOR_SPEED_CAP:
            part.change_x = MOTOR_SPEED_CAP

        # update the part:
        part.update()

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

    change_speed()


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
    global Accelerate, Decelerate

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
    
