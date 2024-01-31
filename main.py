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
GREEN = (20, 80, 20)#(14, 162, 42)
LIGHT_GREEN = (106, 255, 80)
RED = (80, 20, 20)#(255, 42, 42)
LIGHT_RED = (255, 89, 72)
BLUE = (20, 40, 60)
LIGHT_BLUE = (169, 163, 255)
VIOLET = (100, 0, 70)
YELLOW = (255, 194, 0)

# Settings:
WINDOW_SIZE = (1920, 860)
BACKGROUND_COLOR = BLUE
TARGET_COLOR = YELLOW
WEIGHT_RADIUS = 14
PLANET = "jupiter"
ZOOM = 195 # min 120, max 270
FPS = 120

pygame.init()
pygame.display.set_caption("Pendulums")
font = pygame.font.Font("freesansbold.ttf", 90)
font_big = pygame.font.Font("freesansbold.ttf", 200)
reload_img = pygame.image.load("images/reload_btn.png")

class Target:


    """This class represents the target, which
    has to be hitted by the thrown pendulum."""

    def __init__(self):
        self.__width = 120
        self.__height = 20
        self.__position_pixels = [random.randint(0, WINDOW_SIZE[0]-self.__width), WINDOW_SIZE[1]-self.__height]
    
    def get_position(self):
        position_meters = [
            self.__position_pixels[0]/ZOOM,
            self.__position_pixels[1]/ZOOM
        ]
        return position_meters

    def get_width(self):
        return self.__width
    
    def get_area(self):
        return self.__width*self.__height

    def draw(self):
        pygame.draw.rect(
            game.screen, TARGET_COLOR,
            (self.__position_pixels,
            (self.__width, self.__height)
            )
        )


class Pendulum:


    """Class that represents the pendulum cord and the pendulum weight,
    until the weight is detached. Then it only represents the cord."""

    __cord_len = 2 # in meters
    pendulum_fixpoint = (WINDOW_SIZE[0]/ZOOM/2, 1) # in meters

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

        self.__acceleration_arc = -gravity_accel[PLANET] * math.sin(self.__displacement_arc/self.__cord_len)
        self.__velocity_arc += self.__acceleration_arc/FPS # see comment below:
        self.__displacement_arc += self.__velocity_arc/FPS # dividing by fps to get seconds in the calculation. E.G if this is done 60 times per second, the displacement is raised by the velocity (m/s²) every second.
        self.__angle = self.__displacement_arc/self.__cord_len
        self.__position_meters = [
            self.pendulum_fixpoint[0] + self.__cord_len*math.sin(self.__angle),
            self.pendulum_fixpoint[1] + self.__cord_len*math.cos(self.__angle)
        ]
        self.__position_pixels = [self.__position_meters[0]*ZOOM, self.__position_meters[1]*ZOOM]

    def draw(self):
        pygame.draw.circle(game.screen, WHITE, self.__position_pixels, WEIGHT_RADIUS)


class Throw:


    """This class represents the pendulum weight when it is
    detached from the pendulum. It simulates an oblique throw,
    with the start position and velocity, which the pendulum
    had, when it was detached."""

    def __init__(self, position_meters, velocity):
        self.__position_meters = position_meters
        self.__velocity = velocity

    def simulate(self):
        self.__velocity[1] += gravity_accel[PLANET]/FPS
        self.__position_meters[0] += self.__velocity[0]/FPS
        self.__position_meters[1] += self.__velocity[1]/FPS
        if not self.collision():
            self.out_of_bound()

    def collision(self):
        if self.yCollision() and self. xCollision():
                print("LOG: Exit game(Won)")
                game.main_game = False
                game.endGame(won=True)
                return True
        return False

    
    def yCollision(self):
        if self.__position_meters[1] + WEIGHT_RADIUS/ZOOM >= game.target.get_position()[1]:
            print("LOG: Collision on y-achsis")
            return True
        else:
            return False
    
    def xCollision(self):
        if self.__position_meters[0] + WEIGHT_RADIUS/ZOOM > game.target.get_position()[0] and self.__position_meters[0] - WEIGHT_RADIUS/ZOOM < game.target.get_position()[0] + game.target.get_width()/ZOOM:
                print("LOG: Collision on x-achsis")
                return True
        else:
            return False
    
    def out_of_bound(self):
        if self.__position_meters[0]*ZOOM < 0 or self.__position_meters[0]*ZOOM > WINDOW_SIZE[0]:
            print("LOG: Out of bound on x-achsis")
            print("LOG: Exit game(Lost)")
            game.main_game = False
            game.endGame(won=False)
        if self.__position_meters[1]*ZOOM < 0 or self.__position_meters[1]*ZOOM > WINDOW_SIZE[1]:
            print("LOG: Out of bound on y-achsis")
            print("LOG: Exit game(Lost)")
            game.main_game = False
            game.endGame(won=False)

    def draw(self):
        self.__position_pixels = [self.__position_meters[0]*ZOOM, self.__position_meters[1]*ZOOM]
        pygame.draw.circle(game.screen, WHITE, self.__position_pixels, WEIGHT_RADIUS)


class MainGame:


    """The game class redirects some tasks to the more
    specific classes and also does some tasks itself."""

    def __init__(self):
        # Gamestate:
        self.start_game = True
        self.main_game = True
        self.done = False
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
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
        fixpoint_pixels = [Pendulum.pendulum_fixpoint[0]*ZOOM, Pendulum.pendulum_fixpoint[1]*ZOOM]
        pygame.draw.line(self.screen, WHITE, position, fixpoint_pixels, 2)

    def make_throw(self, position_meters, velocity):
        self.throw = Throw(position_meters, velocity)
    
    def reset_highscore(self):
            Files.set_highscores([0, 0, 0, 0, 0])
            print("LOG: highscore has beeen reset to zero.")

    def loop(self):
        pygame.mouse.set_visible(0)
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
                    if event.key == K_ESCAPE:
                        menu = Menu()
                        menu.loop()
                    elif not self.pendulum.get_detached():
                            self.pendulum.detach()
                    
            self.screen.fill(BACKGROUND_COLOR)
            self.simulate()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        
    def endGame(self, won):
        self.endgame = EndGame()
        self.endgame.checkWin(won)
        self.endgame.loop(won)


class EndGame:

    def __init__(self):
        pygame.mouse.set_visible(1)
        self.menu_button = TextButton(WINDOW_SIZE[0]/8, WINDOW_SIZE[1]/9*8, "Menu", 255)
        self.reload_button = TextButton(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/9*8, "Play again!", 500)
        self.exit_button = TextButton(WINDOW_SIZE[0]/9*8, WINDOW_SIZE[1]/9*8, "Exit", 195)

    def calcScore(self):
        self.__score = int(round(gravity_accel[PLANET]/((self.__time_needed)/2))*40000000/ZOOM/WEIGHT_RADIUS/game.target.get_area())
        if gravity_accel[PLANET] < 4.2:
            self.__score = int(round(gravity_accel[PLANET]/((self.__time_needed)/2))*40000000/ZOOM/WEIGHT_RADIUS/game.target.get_area()/gravity_accel[PLANET]*4.2)
    
    def calcHighscores(self):
        score_loose = self.__score
        for i in range(len(self.__highscores)):
                if score_loose < self.__highscores[i]:
                    continue
                if score_loose == self.__highscores[i]:
                    break
                else:
                    print(f"LOG: The old highscore is: {self.__highscores[i]}")
                    highscore_loose = self.__highscores[i]
                    self.__highscores[i] = score_loose
                    score_loose = highscore_loose
        Files.set_highscores(self.__highscores)

    def calcTime(self):
        self.__time_needed = round(pygame.time.get_ticks()/1000 - game.start_ticks/1000, 3)

    def loop(self, won):
        self.done = False
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    exit(0)
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu = Menu()
                        menu.loop()
                        break
                    else:
                        self.done = True
                        break
            if won:
                game.screen.fill(GREEN)
            else:
                game.screen.fill(RED)
            self.draw()
            if self.reload_button.checkClicked():
                self.done = True
                break
            if self.menu_button.checkClicked():
                menu = Menu()
                menu.loop()
                break
            if self.exit_button.checkClicked():
                pygame.QUIT
                exit(0)
            pygame.display.flip()

    def draw(self):
        text_score_headline = font.render("Your score: ", True, WHITE)
        text_score = font_big.render(str(self.__score), True, YELLOW)
        text_highscore_headline = font.render("Highscores:", True, WHITE)
        game.screen.blit(text_score_headline, (WINDOW_SIZE[0]/12, WINDOW_SIZE[1]/(6*5)))
        game.screen.blit(text_score, (WINDOW_SIZE[0]/8, WINDOW_SIZE[1]/3))
        game.screen.blit(text_highscore_headline, (WINDOW_SIZE[0]/32*21, WINDOW_SIZE[1]/(6*5)))
        for i in range(len(self.__highscores)):
            if self.__highscores[i] == self.__score and self.__score != 0:
                text_highscore = font.render(str(self.__highscores[i]), True, YELLOW)
                game.screen.blit(text_highscore, (WINDOW_SIZE[0]/4*3, WINDOW_SIZE[1]/(6*5) + 115*(i+1)))
                continue

            text_highscore = font.render(str(self.__highscores[i]), True, WHITE) # the true enables anti-aliasing, White is the color of the text.
            game.screen.blit(text_highscore, (WINDOW_SIZE[0]/4*3, WINDOW_SIZE[1]/(6*5) + 115*(i+1)))
            


        self.reload_button.draw()
        self.menu_button.draw()
        self.exit_button.draw()

    def checkWin(self, won):
        
        self.__score = 0
        self.__highscores = Files.get_highscores()
        self.calcTime()

        if won:
            self.calcScore()
            print(f"LOG: Time needed: {self.__time_needed}s.")
            self.calcHighscores()
            print(f"LOG: Score: {self.__score}")
            

        else:
            print("LOG: Game lost.")
            print(f"LOG: Time elapsed: {self.__time_needed}s.")


class Files:

    def get_highscores():

        try:
            with open("data/highscores.pickle", "rb") as reader:
                highscores = pickle.load(reader)
                return highscores
        except FileNotFoundError as e:
            game.reset_highscore()

        
    
    def set_highscores(highscores):
        with open("data/highscores.pickle", "wb") as writer:
            print(f"LOG: highscores: {highscores}")
            pickle.dump(highscores, writer)


class Menu:
    
    def __init__(self):
        pygame.mouse.set_visible(1)
        self.__play_button = TextButton(WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/4, "Play", 205)
        self.__exit_button = TextButton(WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/2, "Exit", 195)
        self.__planets_button = TextButton(WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/4*3, "Choose planet", 650)
        self.__reset_highscore_button = TextButton(WINDOW_SIZE[0]/4*3, WINDOW_SIZE[1]/4, "Reset highscore", 710)
        self.__weight_size_slider = Slider(WINDOW_SIZE[0]/4*3, WINDOW_SIZE[1]/2)
        self.__zoom_slider = Slider(WINDOW_SIZE[0]/4*3, WINDOW_SIZE[1]/4*3)

    def draw(self):
        self.__play_button.draw()
        self.__exit_button.draw()
        self.__planets_button.draw()
        self.__reset_highscore_button.draw()
        self.__weight_size_slider.draw()
        self.__zoom_slider.draw()    

    def loop(self):
        
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    exit(0)
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                       pygame.QUIT
                       exit(0)
                    if event.key == pygame.K_RETURN:
                        done = True
                        try:
                            game.endgame.done = True
                        except Exception as e:
                            pass
                        
                if event.type == MOUSEBUTTONDOWN:
                    if self.__play_button.checkClicked():
                        done = True
                        try:
                            game.endgame.done = True
                        except Exception as e:
                            pass
                    if self.__reset_highscore_button.checkClicked():
                        game.reset_highscore()
                    if self.__exit_button.checkClicked():
                        pygame.QUIT
                        exit(0)

                if event.type == pygame.MOUSEWHEEL:
                    print(event.y)

            game.screen.fill(VIOLET)
            self.draw()

            
            
            self.__weight_size_slider.checkMoved()
            self.__zoom_slider.checkMoved()





            pygame.display.flip()


class PlanetMenu:
    pass


class Button:
    
    def __init__(self, x_position, y_position, image):
        self.__image = image
        self.__rect = self.__image.get_rect()
        self.__rect.topleft = (x_position, y_position)
        
    def draw(self):
        game.screen.blit(self.__image, (self.__rect.x, self.__rect.y))


class TextButton:
    def __init__(self, x_position, y_position, text, width=523, height=100):
        self.__x_position = x_position - width/2
        self.__y_position = y_position - height/2
        self.__text = text
        self.__width = width
        self.__height = height
        self.button_rect = pygame.rect.Rect((self.__x_position, self.__y_position),(self.__width, self.__height))

    def draw(self):
        button_text = font.render(self.__text, True, WHITE)   
        pygame.draw.rect(game.screen, BLUE, self.button_rect, 0, 5)
        game.screen.blit(button_text, (self.__x_position + 5, self.__y_position + 5))
    
    def checkClicked(self):
        left_click = pygame.mouse.get_pressed()[0]
        mouse_position = pygame.mouse.get_pos()
        if left_click and self.button_rect.collidepoint(mouse_position):
            return True
        else:
            return False

class Slider:
    def __init__(self, x_position, y_position, width=700, height=100):
        self.__x_position = x_position - width/2
        self.__y_position = y_position - height/2
        self.__x_right_position = x_position + width/2
        self.__slider_width = width/25
        self.__slider_value = 50
        self.__slider_x_position = x_position
        self.__width = width
        self.__height = height
        self.__container_rect = pygame.rect.Rect((self.__x_position, self.__y_position), (self.__width, self.__height))
        self.__container_collision = False

    def draw(self):
        self.__slider_rect = pygame.rect.Rect((self.__slider_x_position - self.__slider_width/2, self.__y_position), (self.__slider_width, self.__height))
        pygame.draw.rect(game.screen, BLUE, self.__container_rect, 0, 5)
        pygame.draw.rect(game.screen, YELLOW, self.__slider_rect, 0, 5)

    def get_value(self):
        return self.__slider_value
    
    def checkMoved(self):
        mouse_position = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        
        if left_click:
            if self.__container_collision:
                self.__slider_x_position = mouse_position[0]
                if self.__slider_x_position - self.__slider_width/2 < self.__x_position:
                    self.__slider_x_position = self.__x_position + self.__slider_width/2
                if self.__slider_x_position + self.__slider_width/2 > self.__x_right_position:
                    self.__slider_x_position = self.__x_right_position - self.__slider_width/2
                self.__slider_value = int((((self.__slider_x_position - self.__slider_width/2 - self.__x_position)) / (self.__width-self.__slider_width)*100))
                print(f"LOG: Slider value: {self.__slider_value}")
        elif self.__container_rect.collidepoint(mouse_position):
            self.__container_collision = True
        else:
            self.__container_collision = False

game = MainGame()

menu = Menu()
menu.loop()

while not game.done:
    print("\n--------------------\nLOG: Start the game!\n--------------------")
    game.start_game = True
    game.main_game = True
    game.loop()
