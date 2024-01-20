import pygame
import random
from pygame.locals import *

# Gravitational Accelerations:
gravityaccel = {
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

class Target:


    """This class represents the target, which
    has to be hitted by the thrown pendulum."""

    def __init__(self):
        self.__position = (random.randint(1200, 1700), 840)
        self.__width = 100
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


    """Class that represents the pendulum cordand the pendulum weight,
    until the weight is detached. Then it only represents the cord."""

    __detached = False

    def __init__(self):
        self.__detached = False

    def detach(self):
        self.__detached = True
        throw = Throw()
        return throw
    
    def get_detached(self):
        return self.__detached

    def draw(self):
        pass
    

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


class Game:


    """The game class redirects some tasks to the more
    specific classes and also does some tasks itself."""

    def simulate(self):
        """This method calculates the position
        of all the objects in the game."""
        pass

    def draw(self):
        target.draw()
        if pendulum.get_detached():
            throw.draw()
        pendulum.draw()
        
# Colors:
background_color = (42, 255, 42)
target_color = (255, 42, 42)

# Gamestate:
gamestart = True
maingame = False
endgame = False

# Pygame time management:
clock = pygame.time.Clock()
fps = 60

# Object creation:
pendulum = Pendulum()
game = Game()
target = Target()

# Start of the game:
inputangle = input(
    "Please enter the angle (in degrees), at which the pendulum starts its movement.\n> "
)
while gamestart:

    try:
        inputangle = int(inputangle)
        gamestart = False
        maingame = True
    except Exception as e:
        inputangle = input(
            "Please enter a positive whole number, without any other symbols.\n> "
        )


# Init of pygame and the window:
pygame.init()
pygame.display.set_caption("Pendulums")
windowsize = (1900, 860)
screen = pygame.display.set_mode(windowsize)


# Main game loop:
while maingame:


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            maingame = False
        
        if event.type == pygame.KEYDOWN:
            pendulum.detach


    screen.fill(background_color)

    game.simulate()
    game.draw()
    pygame.display.flip()
    clock.tick(fps)

# End of the game:
pygame.quit()
exit(0)