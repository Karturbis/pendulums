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

background_color = VIOLET
target_color = YELLOW

time_seconds = 1


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

    __cord_len = 200
    __detached = False
    pendulum_fixpoint = (200, 200)

    def __init__(self):
        self.__detached = False
        self.angle = math.radians(input_angle)
        self.simulate()
        print(self.__position)

    def detach(self):
        self.__detached = True
        throw = Throw(self.__position, self.velocity)
        return throw
    
    def get_detached(self):
        return self.__detached

    def simulate(self):
        self.__position = (
            self.pendulum_fixpoint[0] + self.__cord_len*math.sin(self.angle),
            self.pendulum_fixpoint[1] + self.__cord_len*math.cos(self.angle)
            )

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.__position, 42)
    

    

class Throw:


    """This class represents the pendulum weight when it is
    detached from the pendulum. It simulates an oblique throw,
    with the start position and velocity, which the pendulum
    had, when it was detached."""

    def __init__(position, velocity):
        self.__position = position
        self.__velocity = velocity

    def collision(self):
        pass

    def draw(self):
        pass


class Game:


    """The game class redirects some tasks to the more
    specific classes and also does some tasks itself."""

    def simulate(self):
        """This method calculates the position
        of all the objects in the game."""
        pendulum.simulate()

    def draw(self):
        target.draw()
        if pendulum.get_detached():
            throw.draw()
        pendulum.draw()
        

# Gamestate:
start_game = True
main_game = False
end_game = False

# Pygame time management:
clock = pygame.time.Clock()
fps = 60


# Start of the game:
input_angle = input(
    "Please enter the angle (in degrees), at which the pendulum starts its movement.\n> "
)
while start_game:

    try:
        input_angle = int(input_angle)
        start_game = False
        main_game = True
    except Exception as e:
        input_angle = input(
            "Please enter a positive whole number, without any other symbols.\n> "
        )


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
            pendulum.detach


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