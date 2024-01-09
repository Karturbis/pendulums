import pygame


import data # Imports the data from the data.py file, this includes the gravitational vlaues.

pygame.init() # Initialize pygame


screen = pygame.display.set_mode(data.windowsize)


def gameloop():
    
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)












if __name__ == "__main__":
    """The following code gets executed, if this file is executed"""
    