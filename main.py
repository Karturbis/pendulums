import pygame
import random
import math
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

windowsize = (1900, 860)
background_color = (140, 42, 120)
pen_cord_color =(255, 21, 240)
pen_weight_color = (75, 200, 72)

fps = 60



# Position of the pendulum(cord) fixpoint:
fixpoint_position = (400, 200)

# Position of the target:
x_target_min = 100
x_target_max = 200
y_target = 300


class Pendulum:
    pass

class PendulumWeight(Pendulum):

    def __init__(self):
        pass
    
    def detach(self):
        print("detach!")
    
    def draw(self, pendulum_posi):
        pygame.draw.circle(screen, pen_weight_color, pendulum_posi, 42)


class PendulumCord(Pendulum):

    def __init__(self):
        #self.fixpoint_position = fixpoint_position
        pass

    def draw(self, pendulum_posi):
        
        pygame.draw.line(screen, pen_cord_color, fixpoint_position, pendulum_posi)


class Target:

    def __init__(self):
        self.x_position = random.randint(x_target_min, x_target_max)
        self.y_position = y_target


def gameloop():
    """This method contains the game loop, which runs until the game is stopped,
    it contains all the calls to functions and methods, that have to be called
    every frame of the game."""
    
    done = False
    
    pendulum = Pendulum()
    pencord = PendulumCord()
    penweight = PendulumWeight

    while not done: # This loop runs the game until it is stopped

        for event in pygame.event.get(): # for statement to check for events
            if event.type == pygame.QUIT: # event to exit the game (this event is triggered, if the x button of the window is clicked)
                done = True
            
            if event.type == pygame.KEYDOWN:
                penweight.detach(penweight)

        
        pendulum_posi = [pygame.time.get_ticks()%1000, pygame.time.get_ticks()%1000]
        screen.fill(background_color)
        pencord.draw(pendulum_posi)
        penweight.draw(penweight, pendulum_posi)
        pygame.display.update()
        
        clock.tick(fps)

    pygame.quit()
    exit(0)

if __name__ == "__main__":
    """The following code gets executed, if this file is executed"""

    """this block is ran at the begin of the game
    it initializes pygame,
    defines the clock variable,
    sets the screen size,
    and sets the window caption."""
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(windowsize)
    pygame.display.set_caption("Pendulums")

    gameloop()
    