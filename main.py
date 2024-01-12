import pygame
import random
import math
from pygame.locals import *

import data # Imports the data from the data.py file, this includes the gravitational vlaues and the window size.

class PeendulumWeight:

    def __init__(self, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position

class PendulumCord:

    def __init__(self, angle, length):
        self.x_fixpoint_position = data.x_fixpoint_position
        self.y_fixpoint_position = data.y_fixpoint_position


class Target:

    def __init__(self):
        self.x_position = random.randint(data.x_target_min, data.x_target_max)
        self.y_position = data.y_target


def gameloop():
    """This method contains the game loop, which runs until the game is stopped,
    it contains all the calls to functions and methods, that have to be called
    every frame of the game."""
    
    while True: # This loop runs the game until it is stopped

        for event in pygame.event.get(): # for statement, to close the window and end the game if the pygame event is quit
            if event.type == QUIT:
                pygame.quit()
                exit(0)

        screen.fill([140, 42, 120])
        pygame.display.update()



if __name__ == "__main__":
    """The following code gets executed, if this file is executed"""

    """this block is ran at the begin of the game
    it initializes pygame,
    defines the clock variable,
    sets the screen size,
    and sets the window caption."""
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(data.windowsize)
    pygame.display.set_caption("Pendulums")
    


    gameloop()
    