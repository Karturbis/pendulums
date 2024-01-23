"""
In this simulation:
In real life:        In this simulation:

1 Meter         =   1 Pixel / zoom => 1Pixel = 1Meter*zoom
1 Sekunde       =   1 Sekunde (60 frames)

In the physics calculations, SI-units are used.
"""

import math
import random
import pygame
from pygame.locals import *

# Gravitational Accelerations:
gravity_accel = {
    "merkur": 3.70, 
    "venus": 8.87, 
    "earth": 9.81, 
    "moon": 1.62, 
    "mars": 3.73, 
    "phobos": 0.006, 
    "deimos": 0.003, 
    "jupiter": 24.97, 
    "io": 1.80, 
    "ganymede": 1.43, 
    "europa": 1.31, 
    "callisto": 1.24, 
    "saturn": 10.44, 
    "titan": 1.35, 
    "rhea": 0.26, 
    "uranus": 8.87, 
    "titania": 0.37,
    "oberon": 0.35,
    "ariel": 0.25,
    "umbriel": 0.25,
    "neptune": 11.15,
    "triton": 0.78,
    "proteus": 0.07,
    "nereid": 0.07
    }

# Colors:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (14, 162, 42)
LIGHT_GREEN = (106, 255, 80)
RED = (255, 42, 42)
LIGHT_RED = (255, 89, 72)
BLUE = (100, 100, 240)
LIGHT_BLUE = (169, 163, 255)
VIOLET = (230, 69, 200)
YELLOW = (255, 194, 0)

background_color = GREEN
target_color = YELLOW
planet = "earth"
zoom = 100


class Target:


    """This class represents the target, which
    has to be hitted by the thrown pendulum."""

    def __init__(self):
        self.__position = (random.randint(1200, 1700), 840)
        self.__width = 120
        self.__height = 20

    def draw(self):
        pygame.draw.rect(
            screen, target_color,
            (self.__position,
            (self.__width, self.__height)
            )
        )

    def collision(self):
        pass


class Pendulum:


    """Class that represents the pendulum cord and the pendulum weight,
    until the weight is detached. Then it only represents the cord."""

    __cord_len = 2 # in meter
    pendulum_fixpoint = (400, 200)

    def __init__(self):
        self.__detached = False
        self.__velocity_arc = 0 # the velocity, the pendulum has on the curved x-achsis (arc)
        self.__oscillation_period = ( 
            2*math.pi*math.sqrt((self.__cord_len) / gravity_accel[planet]) # time that the pendulum needs to oscillate one time
        )
        self.__angle = math.radians(input_angle) # angle is defined in radians
        self.__displacement_arc = self.__angle * self.__cord_len # displacement on the curved x-achsis (arc)
        self.simulate()
    
    def get_detached(self):
        return self.__detached

    def get_position(self):
        return self.__position # in pixels

    def detach(self):
        alpha = 90 - self.__angle
        self.__velocity = (
            math.cos(alpha)*self.__velocity_arc, math.sin(alpha)*self.__velocity_arc
        )
        self.__detached = True
        game.make_throw(self.__position, self.__velocity)
    
    def simulate(self):

        self.__acceleration_arc = -gravity_accel[planet] * math.sin(self.__displacement_arc/self.__cord_len)
        self.__velocity_arc += self.__acceleration_arc/fps # see comment below:
        self.__displacement_arc += self.__velocity_arc/fps # dividing by fps to get seconds in the calculation. E.G if this is done 60 times per second, the displacement is raised by the velocity (m/s²) every second.
        self.__angle = self.__displacement_arc/self.__cord_len
        self.__position = ( # in pixels:
            self.pendulum_fixpoint[0] + self.__cord_len*zoom*math.sin(self.__angle),
            self.pendulum_fixpoint[1] + self.__cord_len*zoom*math.cos(self.__angle)
            )

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.__position, 42)
    

    

class Throw:


    """This class represents the pendulum weight when it is
    detached from the pendulum. It simulates an oblique throw,
    with the start position and velocity, which the pendulum
    had, when it was detached."""

    def __init__(self, position, velocity):
        self.__position = position
        self.__velocity = velocity

    def simulate(self):
        self.__velocity[1] += gravity_accel[planet]/fps
        self.__position += self.__velocity/fps


    def collision(self):
        pass

    def draw(self):
        print("LOG: Start throw.draw")
        pygame.draw.circle(screen, WHITE, self.__position, 42)
        print("LOG: End throw.draw")


class Game:


    """The game class redirects some tasks to the more
    specific classes and also does some tasks itself."""


    def simulate(self):

        """This method calculates the position
        of all the objects in the game."""
        if pendulum.get_detached():
            print("LOG: get_detached() returned True")
            self.throw.simulate()
            print("LOG: finished self.throw.simulate()")
        pendulum.simulate()

    def draw(self):
        target.draw()
        if pendulum.get_detached():
            print("LOG: get_detached() returned True")
            self.throw.draw()
            print("LOG: finished self.throw.draw()")
        else:
            pendulum.draw()
        self.draw_pendulum_cord()

    def draw_pendulum_cord(self):
        position = pendulum.get_position()
        pygame.draw.line(screen, WHITE, position, Pendulum.pendulum_fixpoint, 8)

    def make_throw(self, position, velocity):
        self.throw = Throw(position, velocity)

# Gamestate:
start_game = True
main_game = False
end_game = False

# Pygame time management:
clock = pygame.time.Clock()
fps = 60

# minimum and maximum input angle:
angle_min = -45
angle_max = 45

# Start of the game:
input_angle = input(
    f"""\nPlease enter the angle (in degrees),
at which the pendulum starts its movement.
The input has to be an integer between {angle_min} and {angle_max}.\n> """
)
while start_game:

    try:
        input_angle = int(input_angle)
        
        if input_angle <= angle_max and input_angle >= angle_min:
            start_game = False
            main_game = True
        else:
            raise Exception(f"The integer has to be between {angle_min} and {angle_max}.\n>")
    except ValueError:
        input_angle = input("The input has to be an integer!\n>")

    except Exception as e:
        input_angle = input(e)


# Init of pygame and the window:
pygame.init()
pygame.display.set_caption("Pendulums")
window_size = (1900, 860)
screen = pygame.display.set_mode(window_size)

# Object creation:
pendulum = Pendulum()
game = Game()
target = Target()


# Main game loop:
while main_game:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_game = False
            end_game = True
        
        if event.type == pygame.KEYDOWN:
            print("LOG: KEYDON")
            if not pendulum.get_detached():
                pendulum.detach()
            


    screen.fill(background_color)

    game.simulate()
    game.draw()
    pygame.display.flip()
    clock.tick(fps)

# The end of the game loop
while end_game:
    end_game = False

# Quitting of the game:
pygame.quit()
exit(0)