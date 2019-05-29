import random
import arcade


WIDTH = 640
HEIGHT = 480


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


def draw_ground():
    arcade.draw_lrtb_rectangle_filled(0, WIDTH, HEIGHT/6, 0, arcade.color.LIGHT_BROWN)


dust_list = []
for particle in range(30):
    particle = Dust()
    dust_list.append(particle)


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


def on_draw():
    arcade.start_render()

    # Draw The Ground (OH REALLY?)
    draw_ground()

    # Draw Dust
    for particle in dust_list:
        particle.draw()


def on_key_press(key, modifiers):
    pass


def on_key_release(key, modifiers):
    pass


def on_mouse_press(x, y, button, modifiers):
    pass

def on_mouse_release(x, y, button, modifiers):
    pass


if __name__ == '__main__':
    setup()

