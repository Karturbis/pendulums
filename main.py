"""
In this simulation:
In real life:        In this simulation:

1 Meter         =   1 Pixel / zoom => 1Pixel = 1Meter*zoom
1 Second       =   1 Second (60 frames)

In the physics calculations, SI-units are used.
"""

import math
import random
import pickle
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
BLUE = (20, 40, 60)
LIGHT_BLUE = (169, 163, 255)
VIOLET = (230, 69, 200)
YELLOW = (255, 194, 0)

# Settings:
window_size = (1900, 860)
background_color = BLUE
target_color = YELLOW
weight_radius = 1
planet = "jupiter"
zoom = 200
fps = 60

pygame.init()
pygame.display.set_caption("Pendulums")
font = pygame.font.Font("freesansbold.ttf", 90)
reload_img = pygame.image.load("images/reload_btn.png")

class Target:


    """This class represents the target, which
    has to be hitted by the thrown pendulum."""

    def __init__(self):
        self.__width = 120
        self.__height = 20
        self.__position_pixels = [random.randint(0, window_size[0]-self.__width), window_size[1]-self.__height]
    
    def get_position(self):
        position_meters = [
            self.__position_pixels[0]/zoom,
            self.__position_pixels[1]/zoom
        ]
        return position_meters

    def get_width(self):
        return self.__width

    def draw(self):
        pygame.draw.rect(
            game.screen, target_color,
            (self.__position_pixels,
            (self.__width, self.__height)
            )
        )


class Pendulum:


    """Class that represents the pendulum cord and the pendulum weight,
    until the weight is detached. Then it only represents the cord."""

    __cord_len = 2 # in meters
    pendulum_fixpoint = (window_size[0]/zoom/2, 1) # in meters

    def __init__(self):
        self.__detached = False
        self.__velocity_arc = 0 # the velocity, the pendulum has on the curved x-achsis (arc)
        self.__angle = math.radians(game.input_angle) # angle is defined in radians
        self.__displacement_arc = self.__angle * self.__cord_len # displacement on the curved x-achsis (arc)
        self.simulate()
    
    def get_detached(self):
        return self.__detached

    def get_position_pixles(self):
        return self.__position_pixels

    def detach(self):
        self.__velocity = [
            math.cos(self.__angle)*self.__velocity_arc, -math.sin(self.__angle)*self.__velocity_arc
        ]
        self.__detached = True
        game.make_throw(self.__position_meters, self.__velocity)
    
    def simulate(self):

        self.__acceleration_arc = -gravity_accel[planet] * math.sin(self.__displacement_arc/self.__cord_len)
        self.__velocity_arc += self.__acceleration_arc/fps # see comment below:
        self.__displacement_arc += self.__velocity_arc/fps # dividing by fps to get seconds in the calculation. E.G if this is done 60 times per second, the displacement is raised by the velocity (m/s²) every second.
        self.__angle = self.__displacement_arc/self.__cord_len
        self.__position_meters = [
            self.pendulum_fixpoint[0] + self.__cord_len*math.sin(self.__angle),
            self.pendulum_fixpoint[1] + self.__cord_len*math.cos(self.__angle)
        ]
        self.__position_pixels = [self.__position_meters[0]*zoom, self.__position_meters[1]*zoom]

    def draw(self):
        pygame.draw.circle(game.screen, WHITE, self.__position_pixels, weight_radius)


class Throw:


    """This class represents the pendulum weight when it is
    detached from the pendulum. It simulates an oblique throw,
    with the start position and velocity, which the pendulum
    had, when it was detached."""

    def __init__(self, position_meters, velocity):
        self.__position_meters = position_meters
        self.__velocity = velocity

    def simulate(self):
        self.__velocity[1] += gravity_accel[planet]/fps
        self.__position_meters[0] += self.__velocity[0]/fps
        self.__position_meters[1] += self.__velocity[1]/fps
        if not self.out_of_bound():
            self.collision()

    def collision(self):
        if self.__position_meters[1]+weight_radius/zoom >= game.target.get_position()[1]:
            print("LOG: Collision on y-achsis")
            if self.__position_meters[0]+weight_radius/zoom > game.target.get_position()[0] and self.__position_meters[0]-weight_radius/zoom < game.target.get_position()[0] + game.target.get_width()/zoom:
                print("LOG: Collision on x-achsis")
                print("LOG: Exit game(Won)")
                game.main_game = False
                game.endGame(won=True)
    
    def out_of_bound(self):
        if self.__position_meters[0]-weight_radius/zoom < 0 or self.__position_meters[0]+weight_radius/zoom > window_size[0]/zoom:
            print("LOG: Out of bound on x-achsis")
            print("LOG: Exit game(Lost)")
            game.main_game = False
            game.endGame(won=False)
        if self.__position_meters[1]-weight_radius/zoom < 0 or self.__position_meters[1]+weight_radius/zoom > window_size[1]/zoom:
            print("LOG: Out of bound on y-achsis")
            print("LOG: Exit game(Lost)")
            game.main_game = False
            game.endGame(won=False)

    def draw(self):
        self.__position_pixels = [self.__position_meters[0]*zoom, self.__position_meters[1]*zoom]
        pygame.draw.circle(game.screen, WHITE, self.__position_pixels, weight_radius)


class MainGame:


    """The game class redirects some tasks to the more
    specific classes and also does some tasks itself."""

    def __init__(self):
        # Gamestate:
        self.start_game = True
        self.main_game = True
        self.done = False
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()


    def simulate(self):

        """This method calculates the position
        of all the objects in the game."""
        if self.pendulum.get_detached():
            self.throw.simulate()
        self.pendulum.simulate()

    def draw(self):
        self.target.draw()
        if self.pendulum.get_detached():
            self.throw.draw()
        else:
            self.pendulum.draw()
        self.draw_pendulum_cord()

    def draw_pendulum_cord(self):
        position = self.pendulum.get_position_pixles()
        fixpoint_pixels = [Pendulum.pendulum_fixpoint[0]*zoom, Pendulum.pendulum_fixpoint[1]*zoom]
        pygame.draw.line(self.screen, WHITE, position, fixpoint_pixels, 2)

    def make_throw(self, position_meters, velocity):
        self.throw = Throw(position_meters, velocity)
    
    def reset_highscore(self):
        Files.set_highscores([0, 0, 0, 0, 0])
        print("LOG: highscore has beeen reset to zero.")


    def mainGame(self):
        
        while self.main_game:

            # check for gamestates:
            if self.start_game:
                # Start of the game:
                self.input_angle = 90
                self.start_ticks = pygame.time.get_ticks()
                while self.start_game:
                    
                    self.target = Target()
                    self.pendulum = Pendulum()
                    self.start_game = False


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_game = False
                    pygame.QUIT
                    exit(0)
                
                if event.type == pygame.KEYDOWN:
                    print("LOG: KEYDOWN")
                    if not self.pendulum.get_detached():
                        self.pendulum.detach()
                    
            self.screen.fill(background_color)
            self.simulate()
            self.draw()
            pygame.display.flip()
            self.clock.tick(fps)
        
    def endGame(self, won):
        endgame = EndGame()
        endgame.checkWin(won)
        endgame.draw(won)


class EndGame:


    def __init__(self):
        self.reload_button = TextButton(window_size[0]/2-262, window_size[1]/4, "Play again!")
        self.menu_button = TextButton(window_size[0]/2-262, window_size[1]/2, "Menu")
        self.exit_button = TextButton(window_size[0]/2-262, window_size[1]/4*3, "Exit")

    def calcScore(self):
        self.__score = int(round(gravity_accel[planet]/self.__time_needed, 2)*1000/weight_radius)
        if gravity_accel[planet] < 4.2:
            self.__score = int(round(gravity_accel[planet]/self.__time_needed, 2)*1000/weight_radius/gravity_accel[planet]*4.2)
    
    def calcHighscores(self):
        for i in range(len(self.__highscores)):
                if self.__score < self.__highscores[i]:
                    continue
                else:
                    print(f"LOG: The old highscore is: {self.__highscores[i]}")
                    highscore_loose = self.__highscores[i]
                    self.__highscores[i] = self.__score
                    self.__score = highscore_loose
        Files.set_highscores(self.__highscores)

    def calcTime(self):
        self.__time_needed = round(pygame.time.get_ticks()/1000 - game.start_ticks/1000, 3)

    def draw(self, won):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    exit(0)
            if won:
                game.screen.fill(GREEN)
            else:
                game.screen.fill(LIGHT_RED)
            self.reload_button.draw()
            self.menu_button.draw()
            self.exit_button.draw()
            if self.reload_button.checkClicked():
                done = True
            if self.menu_button.checkClicked():
                pass
            if self.exit_button.checkClicked():
                pygame.QUIT
                exit(0)
            pygame.display.flip()

    def checkWin(self, won):
        
        self.__score = 0
        self.__highscores = Files.get_highscores()
        self.calcTime()

        if won:
            self.calcScore()
            print(f"LOG: Time needed: {self.__time_needed}s.")
            self.calcHighscores()
            print(f"LOG: Your score is: {self.__score} points!")
            

        else:
            print("LOG: Game lost.")
            print(f"LOG: Time elapsed: {self.__time_needed}s.")


class Files:

    def get_highscores():
        with open("data/highscores.pickle", "rb") as reader:
            highscores = pickle.load(reader)
        return highscores
    
    def set_highscores(highscores):
        with open("data/highscores.pickle", "wb") as writer:
            print(f"LOG: highscores: {highscores}")
            pickle.dump(highscores, writer)


class Menu:
    
    def __init__(self):
        pass

    def draw(self):
        pass

    def handle_buttons(self):
        pass

    def menu_loop(self):
        pass
        

class Button:
    
    def __init__(self, x_position, y_position, image):
        self.__image = image
        self.__rect = self.__image.get_rect()
        self.__rect.topleft = (x_position, y_position)
        
    def draw(self):
        game.screen.blit(self.__image, (self.__rect.x, self.__rect.y))


class TextButton:
    def __init__(self, x_position, y_position, text):
        self.__x_position = x_position
        self.__y_position = y_position
        self.__text = text

    def draw(self):
        button_text = font.render(self.__text, True, WHITE)
        self.button_rect = pygame.rect.Rect((self.__x_position, self.__y_position),(523, 100))
        pygame.draw.rect(game.screen, BLUE, self.button_rect, 0, 5)
        game.screen.blit(button_text, (self.__x_position + 4, self.__y_position + 4))
    
    def checkClicked(self):
        mouse_position = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        if left_click and self.button_rect.collidepoint(mouse_position):
            return True
        else:
            return False

game = MainGame()

while not game.done:
    print("\n--------------------\nLOG: Start the game!\n--------------------")
    game.start_game = True
    game.main_game = True
    game.mainGame()





