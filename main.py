"""
In real life:        In this simulation:

1 Meter         =   1 Pixel / zoom => 1Pixel = 1Meter*zoom
1 Second        =   1 Second (60 frames)

In the physics calculations, SI-units are used.
Due to complexity reasons, air resistance is ignored.

If in comments the word 'weight' is used, usually
the thing at the end of the pendulum, or the thing
that is doing the oblique throw, is meant.
"""

# Imports:
import math # for the calculations with angles and sqrt
import random # for the setting the target and changing the planet
import pickle # for saving the highscores to a file
import pygame # for the display and a lot of other stuff
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

# Constants:
WINDOW_SIZE = (1920, 860)
BACKGROUND_COLOR = BLUE
TARGET_COLOR = YELLOW
FPS = 120
SCREEN = pygame.display.set_mode(WINDOW_SIZE)
pygame.init() # Initialize pygame

# Initialize fonts:
font = pygame.font.Font("freesansbold.ttf", 90)
font_big = pygame.font.Font("freesansbold.ttf", 200)

class Variables:
    """This class contains variables, that need
    to be accessed from more than one class"""

    # the kay value for the gravitational accelerations dictionary:
    planet = "earth" 
    weight_radius = 30 # min 5, max 50; radius of the pendulum weight
    zoom = 190 # min 120, max 220; scale from meters to pixels


class Target():
    """This class represents the target, that
    to be hit by the thrown pendulum."""

    def __init__(self):
        self.__width = 120
        self.__height = 20
        self.__position_pixels = [
            random.randint(0, WINDOW_SIZE[0]-self.__width),
            WINDOW_SIZE[1]-self.__height
        ]
    
    def get_position(self):
        position_meters = [
            self.__position_pixels[0]/Variables.zoom,
            self.__position_pixels[1]/Variables.zoom
        ]
        return position_meters

    def get_width(self):
        return self.__width
    
    def get_area(self):
        return self.__width*self.__height

    def draw(self):
        pygame.draw.rect(
            SCREEN, TARGET_COLOR,
            (self.__position_pixels,
            (self.__width, self.__height)
            )
        )


class Pendulum():
    """Class that represents the pendulum cord and the pendulum weight,
    until the weight is detached. After that it only represents the cord."""

    __cord_len = 2 # in meters
    pendulum_fixpoint = (WINDOW_SIZE[0]/Variables.zoom/2, 1) # in meters

    def __init__(self):
        self.__detached = False
        # the velocity, that the pendulum has on the curved x-achsis (arc):
        self.__velocity_arc = 0
        self.__angle = math.radians(game.input_angle) # in radians
        # displacement on the curved x-achsis (arc):
        self.__displacement_arc = self.__angle * self.__cord_len
        self.simulate()
    
    def get_detached(self):
        return self.__detached

    def get_position_pixles(self):
        return self.__position_pixels

    def detach(self):
        """Calculates the current velocity and
        returns the current velocity and current
        position, measured in meters.
        Sets the self.__detached variable to True"""

        self.__velocity = [
            math.cos(self.__angle)*self.__velocity_arc,
            -math.sin(self.__angle)*self.__velocity_arc
        ]
        self.__detached = True
        game.make_throw(self.__position_meters, self.__velocity)
    
    def simulate(self):
        """Handles the calculation for displacement,
        velocity, acceleration and angle of the pendulum.
        Based on the physics formula:

        a = g*sin(s/l)

        where 'a' is the acceleration, 'g' is gravitation in our
        case 'g' is negative because of the chosen reference system.
        's' is the displacement on the x-achsis and 'l' is the lenght
        of the pendulum cord.
        The velocity is simply the acceleration added to the
        current velocity every frame. Because all the calculations
        are done with SI units, the acceleration is diveded by FPS.

        The displacement is the velocity, devided by FPS added to the
        current displacement.
        """

        self.__acceleration_arc = (
            -gravity_accel[Variables.planet]
            * math.sin(self.__displacement_arc/self.__cord_len)
            )
        self.__velocity_arc += self.__acceleration_arc/FPS
        self.__displacement_arc += self.__velocity_arc/FPS
        self.__angle = self.__displacement_arc/self.__cord_len
        self.__position_meters = [
            self.pendulum_fixpoint[0]
            + self.__cord_len*math.sin(self.__angle),
            self.pendulum_fixpoint[1]
            + self.__cord_len*math.cos(self.__angle)
        ]
        self.__position_pixels = [
            self.__position_meters[0]*Variables.zoom,
            self.__position_meters[1]*Variables.zoom
        ]

    def draw(self):
        pygame.draw.circle(
            SCREEN, # surface to draw on
            WHITE, # color to draw with
            self.__position_pixels,
            Variables.weight_radius
        )


class Throw():
    """This class represents the pendulum weight when it is
    detached from the pendulum. It simulates an oblique throw,
    with the start position and velocity, which the pendulum
    had, when it was detached."""

    def __init__(self, position_meters, velocity):
        self.__position_meters = position_meters
        self.__velocity = velocity

    def simulate(self):
        """This method handles the calculation of the
        oblique throw of the weight. It claculates the
        position and the velocity of the weight.
        The calculations are based on the real physics,
        the velocity in x direction remains the same,
        the velocity in y direction is accelerated by
        the gravitational acceleration."""

        self.__velocity[1] += gravity_accel[Variables.planet]/FPS
        self.__position_meters[0] += self.__velocity[0]/FPS
        self.__position_meters[1] += self.__velocity[1]/FPS
        if not self.collision(): # checks for collision
            self.out_of_bound() # checks for out of the window

    def collision(self):
        """This method combines the results of
        yCollision and xCollision, to get the
        final collision result."""

        if self.yCollision() and self. xCollision():
                print("LOG: Exit game(Won)")
                game.main_game = False
                game.endGame(won=True)
                return True
        else:
            return False

    def yCollision(self):
        """Checks for a collision between the weight
        and the target on the y-achsis.
        Returns True if a collision is taking place."""

        if (
            self.__position_meters[1]
            + Variables.weight_radius/Variables.zoom
            >= game.target.get_position()[1]
        ):
            print("LOG: Collision on y-achsis")
            return True
        else:
            return False
    
    def xCollision(self):
        """Checks for a collision between the weight
        and the target on the x-achsis.
        Returns True if a collision is taking place."""

        if (
            self.__position_meters[0] + Variables.weight_radius/Variables.zoom
            > game.target.get_position()[0]
            and self.__position_meters[0]
            - Variables.weight_radius/Variables.zoom
            < game.target.get_position()[0]
            + game.target.get_width()/Variables.zoom
        ):
            print("LOG: Collision on x-achsis")
            return True
        else:
            return False
    
    def out_of_bound(self):
        """Checks, if the weight is still in the window.
        If the weight is not in the window anymore, it
        initiates the end of the game."""

        if (
            self.__position_meters[0]*Variables.zoom < 0
            or self.__position_meters[0]*Variables.zoom > WINDOW_SIZE[0]
        ):
            print("LOG: Out of bound on x-achsis")
            print("LOG: Exit game(Lost)")
            game.main_game = False
            game.endGame(won=False)
        if (
            self.__position_meters[1]*Variables.zoom < 0
            or self.__position_meters[1]*Variables.zoom > WINDOW_SIZE[1]
        ):
            print("LOG: Out of bound on y-achsis")
            print("LOG: Exit game(Lost)")
            game.main_game = False
            game.endGame(won=False)

    def draw(self):
        self.__position_pixels = [
            self.__position_meters[0]*Variables.zoom,
            self.__position_meters[1]*Variables.zoom
        ]
        pygame.draw.circle(
            SCREEN, # surface to draw on
            WHITE, # color to draw with
            self.__position_pixels,
            Variables.weight_radius
        )


class MainGame():
    """The game class redirects some tasks to the more
    specific classes.
    Some other tasks are directly implemented into
    the MainGame class."""

    def __init__(self):
        # Gamestate:
        self.start_game = True
        self.main_game = True
        # variable to let the main loop run:
        self.done = False
        # defining the clock:
        self.clock = pygame.time.Clock()

    def simulate(self):
        """This method calculates the position
        of all the objects in the game.
        It does this, by redirecting the
        tasks to the right places."""

        if self.pendulum.get_detached():
            self.throw.simulate()
        self.pendulum.simulate()

    def draw(self):
        """This method redirects the call
        to the draw methods that are
        needed in the moment."""

        self.target.draw()
        if self.pendulum.get_detached():
            self.throw.draw()
        else:
            self.pendulum.draw()
        self.draw_pendulum_cord()

    def draw_pendulum_cord(self):
        """This method draws the pendulum cord.
        The pendulum cord is a line between the
        pendulum fixpoint and the position of
        the pendulum. If the pendulum weight is
        detached, the pendulum cord is still drawn
        between the fixpoint and the point, where
        the pendulum would be, if it was not detached."""

        position = self.pendulum.get_position_pixles()
        fixpoint_pixels = [
            Pendulum.pendulum_fixpoint[0]*Variables.zoom,
            Pendulum.pendulum_fixpoint[1]*Variables.zoom
        ]
        pygame.draw.line(SCREEN, WHITE, position, fixpoint_pixels, 2)

    def make_throw(self, position_meters, velocity):
        """This method initializes an instance of
        the Throw class and passes the given parameters."""

        self.throw = Throw(position_meters, velocity)
    
    def reset_highscore(self):
        """This method resets all
        highscores to zero."""

        Files.set_highscores([0, 0, 0, 0, 0])
        print("LOG: highscore has beeen reset to zero.")

    def loop(self):
        """This method contains the gameloop.
        It checks for events and runs at the FPS,
        that are defined at the beginning of the prgogram."""

        pygame.mouse.set_visible(0) # set mouse invisible
        pygame.display.set_caption("Pjendol   -   In Game")
        # The game loop:
        while self.main_game:

            # check for gamestates:
            if self.start_game:
                # Start of the game:
                # set the angle, at which the pendulum starts to 90°:
                self.input_angle = 90
                # save time to later calculate the needed time:
                self.start_ticks = pygame.time.get_ticks()
                # intitialize target and pendulum:
                self.target = Target()
                self.pendulum = Pendulum()
                # exit the start_game phase:
                self.start_game = False

            for event in pygame.event.get(): # event listener
                # making the window closable:
                if event.type == pygame.QUIT:
                    self.main_game = False
                    pygame.QUIT
                    exit(0)
                
                # add key control and shortkeys:
                if event.type == pygame.KEYDOWN:
                    print("LOG: KEYDOWN")
                    if event.key == K_ESCAPE:
                        menu = Menu()
                        menu.loop()
                    elif event.key == K_BACKSPACE:
                        self.main_game = False
                        self.endGame(won=False)
                    elif not self.pendulum.get_detached():
                            self.pendulum.detach()
                    
            SCREEN.fill(BACKGROUND_COLOR)
            self.simulate()
            self.draw()
            pygame.display.flip() # update display content
            self.clock.tick(FPS)

    def endGame(self, won):
        """This method initializes
        the end of the game and passes
        the given victory state."""

        self.endgame = EndGame()
        self.endgame.checkWin(won)
        self.endgame.loop(won)


class EndGame():
    """This class is called when
    the game is over, depending
    on if the player won or not
    the screen is green or red.
    The score and the five best
    highscores are displayed and
    buttons to exit, to retry
    and to go to menu are implemented."""

    def __init__(self):
        pygame.mouse.set_visible(1) # makes the mouse visible
        # Initialization of the buttons:
        self.__menu_button = TextButton(
            WINDOW_SIZE[0]/8, WINDOW_SIZE[1]/9*8,
            "Menu", 255
        )
        self.__reload_button = TextButton(
            WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/9*8,
            "Play again!", 500, YELLOW, BLACK
        )
        self.__exit_button = TextButton(
            WINDOW_SIZE[0]/9*8, WINDOW_SIZE[1]/9*8,
            "Exit", 195
        )

    def calcScore(self):
        """This method calculates the
        score that the player reached."""

        self.__score = int(
            round(gravity_accel[Variables.planet]
            /((self.__time_needed)/2))*400000000
            /Variables.zoom/Variables.weight_radius
            /game.target.get_area()
        )
        if gravity_accel[Variables.planet] < 4.2:
            self.__score = int(
                round(gravity_accel[Variables.planet]
                /((self.__time_needed)/2))*400000000
                /Variables.zoom/Variables.weight_radius
                /game.target.get_area()/gravity_accel[Variables.planet]*4.2
            )
    
    def calcHighscores(self):
        """This method calculates the highscores
        that are the five best, after the current
        score was calculated."""
        
        # calculation of the hihgscores, by iterating through the list:
        score_loose = self.__score
        for i in range(len(self.__highscores)):
                if score_loose < self.__highscores[i]:
                    continue
                if score_loose == self.__highscores[i]:
                    break
                else:
                    highscore_loose = self.__highscores[i]
                    self.__highscores[i] = score_loose
                    score_loose = highscore_loose
        # setting the new highscores and saving them to the file:
        Files.set_highscores(self.__highscores)

    def calcTime(self):
        # calculates the time that was elapsed, since the game started.
        self.__time_needed = round(
            pygame.time.get_ticks()
            /1000 - game.start_ticks/1000, 3
        )

    def loop(self, won):
        """The 'game loop' of the endgame
        handles the buttons and the
        redistributing of tasks to other methods."""

        self.done = False
        while not self.done:
            # Event listener:
            for event in pygame.event.get():
                # Exits the game, if the window is closed:
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    exit(0)
                # Add shortkeys:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu = Menu()
                        menu.loop()
                        break
                    else:
                        self.done = True
                        break

            if won:
                pygame.display.set_caption("Pjendol   -   Game won")
                SCREEN.fill(GREEN)
            else:
                pygame.display.set_caption("Pjendol   -   Game lost")
                SCREEN.fill(RED)

            self.draw()
            # Button checks:
            if self.__reload_button.checkClicked():
                self.done = True
                break
            if self.__menu_button.checkClicked():
                menu = Menu()
                menu.loop()
                break
            if self.__exit_button.checkClicked():
                pygame.QUIT
                exit(0)
            # Update display and limit fps to FPS:
            pygame.display.flip()
            game.clock.tick(FPS)

    def checkWin(self, won):
            """Checks if the player won the game.
            redirects tasks to other methods."""
            
            self.__score = 0
            # loading the highscores from file:
            self.__highscores = Files.get_highscores()
            # Time calculation:
            self.calcTime()
            print(f"LOG: Time elapsed: {self.__time_needed}s.")
            # Checking if the player won or lost:
            if won:
                self.calcScore()
                self.calcHighscores()
                print(f"LOG: Score: {self.__score}")
            else:
                print("LOG: Game lost.")

    def draw(self):
        """This method displays the score
        and the highscores, It also draws
        the buttons to the window.
        The 'True' in the text definition
        enables antialiasing."""

        # Defining the texts:
        text_score_headline = font.render("Your score: ", True, WHITE)
        text_score = font_big.render(str(self.__score), True, YELLOW)
        text_highscore_headline = font.render("Highscores:", True, WHITE)
        # Drawing the texts to the screen:
        SCREEN.blit(
            text_score_headline,
            (WINDOW_SIZE[0]/12, WINDOW_SIZE[1]/(6*5))
        )
        SCREEN.blit(
            text_score,
            (WINDOW_SIZE[0]/8, WINDOW_SIZE[1]/3)
        )
        SCREEN.blit(
            text_highscore_headline,
            (WINDOW_SIZE[0]/32*21, WINDOW_SIZE[1]/(6*5))
        )
        # Highlighting the highscore, equal to the scored score:
        for i in range(len(self.__highscores)):
            if self.__highscores[i] == self.__score and self.__score != 0:
                text_highscore = font.render(
                    str(self.__highscores[i]), True, YELLOW
                )
                SCREEN.blit(
                    text_highscore,
                    (WINDOW_SIZE[0]/4*3, WINDOW_SIZE[1]/(6*5) + 115*(i+1))
                )
                continue
            text_highscore = font.render(
                str(self.__highscores[i]), True, WHITE
            )
            SCREEN.blit(
                text_highscore,
                (WINDOW_SIZE[0]/4*3, WINDOW_SIZE[1]/(6*5) + 115*(i+1))
            )

        # Draw the buttons:
        self.__reload_button.draw()
        self.__menu_button.draw()
        self.__exit_button.draw()


class Files():
    """This class is not ment
    to be initialized.
    The Files class is used to read and write
    to the highscores.pickle file."""

    def get_highscores():
        """Opens the highscores.pickle file and
        loads the highscores list from there.
        If that fails, it calls the reset highscores
        method, to avoid having no highscores list."""

        try:
            with open("data/highscores.pickle", "rb") as reader:
                highscores = pickle.load(reader)
                return highscores
        except FileNotFoundError as e:
            game.reset_highscore()

    def set_highscores(highscores):
        """Opens the highscores.pickle file and
        writes the highscores list to it, which
        is given as a parameter."""

        with open("data/highscores.pickle", "wb") as writer:
            print(f"LOG: highscores: {highscores}")
            pickle.dump(highscores, writer)


class Menu():
    """The Menu class displays the game
    menu, for example at the start of the
    game. It has multiple buttons and a slider."""
    
    def __init__(self):
        pygame.mouse.set_visible(1) # set the mouse visible
        # Initializing the buttons and sliders:
        self.__play_button = TextButton(
            WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/4, "Play", 205, YELLOW, BLACK
        )
        self.__planets_button = TextButton(
            WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/2, "Change planet", 665
        )
        self.__reset_highscore_button = TextButton(
            WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/4*3, "Reset highscore", 720
        )
        self.__weight_size_heading = Text(
            WINDOW_SIZE[0]/4*3, WINDOW_SIZE[1]/4, "Weight size:"
        )
        self.__weight_size_slider = Slider(
            WINDOW_SIZE[0]/4*3, WINDOW_SIZE[1]/2
        )
        self.__exit_button = TextButton(
            WINDOW_SIZE[0]/4*3, WINDOW_SIZE[1]/4*3, "Exit", 195
        )

    def calcWeightSize(self):
        """This method calculates the size of
        the weight, depending on the value
        of the weight size slider."""

        self.__weight_size_slider.checkMoved()
        Variables.weight_radius = self.__weight_size_slider.get_value()/2
        # making sure the number always has two digits:
        if Variables.weight_radius < 10:
            weight_size_text = Text(
                WINDOW_SIZE[0]/4*3, WINDOW_SIZE[1]/8*3,
                "0" + str(int(Variables.weight_radius)), 120
            )
        else:
            weight_size_text = Text(
                WINDOW_SIZE[0]/4*3, WINDOW_SIZE[1]/8*3,
                str(int(Variables.weight_radius)), 120
            )
        weight_size_text.draw()
        Variables.weight_radius += 5 # to avoid the weight size being to small
    
    def changePlanet(self):
        """This method sets the 'planet'
        variable to a random, accepted value."""
        
        # Generate a random index for the gravity_accel dict:
        planet_num = random.randint(0, len(gravity_accel)-1)
        # Mapping the index to a key:
        planets = list(gravity_accel.keys())
        # Set the global planet variable to the new planet:
        Variables.planet = planets[planet_num]
        print(f"LOG: Planet = {Variables.planet}")

    def loop(self):
        """This method is the menu loop,
        it loops through the things that
        have to be done until the menu is closed."""

        pygame.display.set_caption("Pjendol   -   Menu")
        # The menu loop:
        done = False
        while not done:
            # Event listener:
            for event in pygame.event.get():
                # Exits the game, if the window is closed:
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    exit(0)
                # Shortkeys:
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                       pygame.QUIT
                       exit(0)
                    if (
                        event.key == pygame.K_RETURN
                        or event.key == pygame.K_SPACE
                    ):
                        # runs the main game
                        done = True
                        try:
                            game.endgame.done = True
                        except Exception as e:
                            pass
                        
                # Button events:
                if event.type == MOUSEBUTTONDOWN:
                    if self.__play_button.checkClicked():
                        done = True
                        try:
                            game.endgame.done = True
                        except Exception as e:
                            pass
                    if self.__reset_highscore_button.checkClicked():
                        game.reset_highscore()
                    if self.__planets_button.checkClicked():
                        self.changePlanet()
                    if self.__exit_button.checkClicked():
                        pygame.QUIT
                        exit(0)

            SCREEN.fill(VIOLET)
            self.draw()
            self.calcWeightSize()
            pygame.display.flip()
            game.clock.tick(FPS)
    
    def draw(self):
        self.__play_button.draw()
        self.__exit_button.draw()
        self.__planets_button.draw()
        self.__reset_highscore_button.draw()
        self.__weight_size_heading.draw()
        self.__weight_size_slider.draw()



class UserInput():
    """This is the parent class for Slider and TextButton."""

    def __init__(self, x_position, y_position, width, height, color):
        self._x_position = x_position - width/2
        self._y_position = y_position - height/2
        self._color = color


class TextButton(UserInput):
    """This class represents a simple
    button with text. It takes the parameters:
    x- and y position and text. Optional parameters:
    width, color, text color and height.
    Inherits from UserInput class."""

    def __init__(
        self, x_position, y_position, text,
        width=523, color=BLUE, text_color=WHITE, height=100
    ):
        super().__init__(x_position, y_position, width, height, color)
        self.__text = text
        self.__width = width
        self.__height = height
        
        self.__text_color = text_color
        # Create body of the button:
        self.button_rect = pygame.rect.Rect(
            (self._x_position, self._y_position),
            (self.__width, self.__height)
        )
 
    def checkClicked(self):
        """This method checks, if the mouse
        left click is pressed and the mouse
        collides with the button. If the button
        is clicked, it returns 'True'"""

        left_click = pygame.mouse.get_pressed()[0]
        mouse_position = pygame.mouse.get_pos()
        if left_click and self.button_rect.collidepoint(mouse_position):
            return True
        else:
            return False

    def draw(self):
        # define text:
        button_text = font.render(self.__text, True, self.__text_color)
        # draw the button:
        pygame.draw.rect(SCREEN, self._color, self.button_rect, 0, 5)
        SCREEN.blit(button_text, (self._x_position + 5, self._y_position + 5))


class Slider(UserInput):
    """This class represents a simple
    slider, that has a value between 0
    and 100. The contructor takes the 
    required parameters: x- and y position
    and the optional parameters:
    width and height.
    Inherits from UserIput class."""

    def __init__(
        self, x_position, y_position,
        width=700, color=BLUE, height=100
    ):
        super().__init__(x_position, y_position, width, height, color)
        self.__x_right_position = x_position + width/2
        self.__slider_width = width/25
        self.__slider_value = 50
        self.__slider_x_position = x_position
        self.__width = width
        self.__height = height
        # define the container rectangle:
        self.__container_rect = pygame.rect.Rect(
            (self._x_position, self._y_position),
            (self.__width, self.__height)
        )
        self.__container_collision = False

    def get_value(self):
        return self.__slider_value
    
    def checkMoved(self):
        """This method checks, if the slider
        was moved. If the slider would be moved
        outside the container, it stays in the 
        container as near as possible to the
        still clicked mouse.
        If it was, the value of the
        slider gets calculated."""

        mouse_position = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        
        if left_click:
            if self.__container_collision:
                # set slider position to be same as mouse position:
                self.__slider_x_position = mouse_position[0]
                # check for slider being out of the container:
                if (
                    self.__slider_x_position
                    - self.__slider_width/2
                    < self._x_position
                ):
                    self.__slider_x_position = (
                        self._x_position + self.__slider_width/2
                    )
                if (
                    self.__slider_x_position
                    + self.__slider_width/2
                    > self.__x_right_position
                ):
                    self.__slider_x_position = (
                        self.__x_right_position
                        - self.__slider_width/2
                    )
                # calculating the slider value:
                self.__slider_value = int(
                    ((self.__slider_x_position
                    - self.__slider_width/2 - self._x_position))
                    / (self.__width-self.__slider_width)*100
                )
        # if mouse stays clicked, while moving out of the container:
        elif self.__container_rect.collidepoint(mouse_position):
            self.__container_collision = True
        else:
            self.__container_collision = False

    def draw(self):
        # define the slider rectangle:
        self.__slider_rect = pygame.rect.Rect((self.__slider_x_position - self.__slider_width/2, self._y_position), (self.__slider_width, self.__height))
        # draw the slider and container:
        pygame.draw.rect(SCREEN, self._color, self.__container_rect, 0, 5)
        pygame.draw.rect(SCREEN, YELLOW, self.__slider_rect, 0, 5)


class Text():
    """This class prints the given text
    to the given x- and y position.
    """
    def __init__(self, x_position, y_position, text, width=523, height=100):
        self.__x_position = x_position - width/2
        self.__y_position = y_position - height/2
        self.__text = font.render(text, True, WHITE)
        self.__width = width
        self.__height = height

    def draw(self):
        # draw the text to the screen:
        SCREEN.blit(self.__text, (self.__x_position, self.__y_position))


variables = Variables()
game = MainGame()

menu = Menu()
menu.loop()

while not game.done:
    print("\n--------------------\nLOG: Start the game!\n--------------------")
    game.start_game = True
    game.main_game = True
    game.loop()
