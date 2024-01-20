import pygame
import random
from pygame.locals import *

class Target:

    def __init__(self):
        self.__position = (random.randint(1200, 1700), 840)
        self.__width = 100
        self.__height = 20

    def draw(self):
        pygame.draw.rect(screen, target_color,(self.__position, (self.__width, self.__height)))

    def collision(self):
        pass


class Pendulum:
    
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
    """This class represents the pendulum weight, when it is detached from the pendulum."""
    def __init__(position, velocity):
        self.__position = position
        self.__velocity = velocity

    def collision(self):
        pass

class Game:

    def simulate(self):
        """This method calculates the position of all the objects in the game."""
        pass

    def draw(self):
        target.draw()
        if pendulum.get_detached():
            throw.draw()
        pendulum.draw()
        



background_color = (42, 255, 42)
target_color = (255, 42, 42)
gamestart = True
maingame = False
endgame = False

clock = pygame.time.Clock()
fps = 60

pendulum = Pendulum()
game = Game()
target = Target()


inputangle = input("Please enter the angle (in degrees), at which the pendulum starts its movement.\n> ")
while gamestart:

    try:
        inputangle = int(inputangle)
        gamestart = False
        maingame = True
    except Exception as e:
        inputangle = input("Please enter a positive whole number, without any other symbols.\n> ")

print(inputangle)

pygame.init()
pygame.display.set_caption("Pendulums")
windowsize = (1900, 860)
screen = pygame.display.set_mode(windowsize)


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


pygame.quit()
exit(0)