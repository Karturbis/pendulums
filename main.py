import pygame
import random
from pygame.locals import *

class Target:

    def __init__(self):
        self.position = (random.randint(1200, 1700), 840)
        self.width = 100
        self.height = 20

    def draw(self):
        pygame.draw.rect(screen, target_color,(self.position, (self.width, self.height)))

    def collision(self):
        pass


class Pendulum:
    
    detached = False

    def __init__(self):
        detached = False

    def detach(self):
        
        self.detached = True
        throw = Throw()
        return throw
    
    def draw(self):
        pass
    

class Throw:
    """This class represents the pendulum weight, when it is detached from the pendulum."""
    def __init__(position, velocity):
        self.position = position
        self.velocity = velocity

    def collision(self):
        pass

class Game:

    def simulate(self):
        """This method calculates the position of all the objects in the game."""
        pass

    def draw(self):
        target.draw()
        if pendulum.detached:
            throw.draw()
        pendulum.draw()
        


pygame.init()
pygame.font.init()
pygame.display.set_caption("Pendulums")
windowsize = (1900, 860)
screen = pygame.display.set_mode(windowsize)
font = pygame.font.SysFont('freesanbold.ttf', 50)

background_color = (42, 255, 42)
target_color = (255, 42, 42)
gamestart = True
maingame = False
endgame = False
inputangle = ""
clock = pygame.time.Clock()
fps = 60

pendulum = Pendulum()
game = Game()
target = Target()

while gamestart:

    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            gamestart = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:

                try:
                    inputangle = int(inputangle)
                except Exception as e:
                    pass
                gamestart = False
                maingame = True

            elif event.key == pygame.K_BACKSPACE:
                inputangle = inputangle[:-1]
            
            else:
                inputangle += event.uniode
    
    screen.fill((20, 20, 20))
    text_render = font(inputangle, True, (255, 255, 255))
    screen.flip()

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