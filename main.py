import pygame

class Target:

    def __init__(self):
        pass

    def draw(self):
        pass

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
        Target.draw
        if pendulum.detached:
            Throw.draw()
        pendulum.draw()
        


pygame.init()
pygame.display.set_caption("Pendulums")
windowsize = (1900, 860)
screen = pygame.display.set_mode(windowsize)
background_color = (42, 255, 42)

clock = pygame.time.Clock()
fps = 60

done = False

pendulum = Pendulum()
game = Game()
target = Target()


while not done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
            pendulum.detach


    screen.fill(background_color)

    game.simulate()
    game.draw()
    pygame.display.flip()
    clock.tick(fps)


pygame.quit()
exit(0)