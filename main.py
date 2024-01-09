import pygame
from pygame.locals import *

import data # Imports the data from the data.py file, this includes the gravitational vlaues.

pygame.init() # Initialize pygame

clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("pendulums")


def gameloop():
    
    
    while True: # This loop runs the game until it is stopped

        for event in pygame.event.get(): # for statement to close the window and end the game, if the pygame event is quit
            if event.type == QUIT:
                pygame.quit()
                exit(0)

        screen.fill([140, 42, 120])
        pygame.display.update()



if __name__ == "__main__":
    """The following code gets executed, if this file is executed"""
    gameloop()
    