import pygame
from pygame.locals import *

import data # Imports the data from the data.py file, this includes the gravitational vlaues and the window size.

 # Initialize pygame


def game_init():
    """this method is ran at the begin of the game
    it initializes pygame,
    defines the clock variable,
    sets the screen size,
    and sets the window caption."""
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(data.windowsize)
    pygame.display.set_caption("Pendulums")

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
    game_init()
    gameloop()
    