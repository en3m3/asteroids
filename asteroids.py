import arcade
import hitbox
from scene import Scene
import rigidbody
from standard import Point, Vect2, Cursor
import math
import random
import os.path
from player import Player
from rigidbody import LargeAsteroid, MediumAsteroid, SmallAsteroid, Ship, Bullet

DEBUG = False

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Message:
    '''
    message(eventriggered: object that triggered, target: target object if there is one, option: option value)
    '''
    def __init__(self, messages):
        self.messages = messages
        if "playerHit" in self.messages:
            trigger = self.messages['playerHit']         
            
        elif "playerAccelerate" in self.messages:
            trigger = self.messages['playerAccelerate'] 
            trigger.ship.accelerate()
        elif "playerDeccelerate" in self.messages:
            trigger = self.messages['playerDeccelerate'] 
            trigger.ship.deccelerate()
        elif "playerRotateClockwise" in self.messages:
            trigger = self.messages['playerRotateClockwise']              
            trigger.ship.rotateC()

        elif "playerRotateCounterClockwise" in self.messages:
            trigger = self.messages['playerRotateCounterClockwise']           
            trigger.ship.rotateCC() 

        elif "playerFire" in self.messages:
            trigger = self.messages['playerFire']           
            bullet = Bullet(trigger.ship)
            window.level.bullets.append(bullet)
    def __repr__(self):
        for message in self.messages:
            return message


def buildLevelOne(textures):
    levelOne = Scene()
    levelOne.name = "Level One"
    levelAsteroids = [LargeAsteroid(),LargeAsteroid(),LargeAsteroid(),LargeAsteroid(),LargeAsteroid()]
    for asteroid in levelAsteroids:
        asteroid.center.x = random.randint(0,SCREEN_WIDTH)
        asteroid.center.y = random.randint(0,SCREEN_HEIGHT)
    levelOne.asteroids = levelAsteroids
    return levelOne

def buildLevelTwo(textures):
    levelTwo = Scene()
    levelTwo.name = "Test"
    levelAsteroids = [LargeAsteroid(),LargeAsteroid(),LargeAsteroid(),LargeAsteroid(),MediumAsteroid(),SmallAsteroid(),SmallAsteroid()]
    for asteroid in levelAsteroids:
        asteroid.center.x = random.randint(0,SCREEN_WIDTH)
        asteroid.center.y = random.randint(0,SCREEN_HEIGHT)    
    levelTwo.asteroids = levelAsteroids
    return levelTwo                          


class Game(arcade.Window):
    def __init__(self, width, height, fullscreen=True):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.textures = {}
        self.gameDifficulty = 0
        self.mouseCursor = Cursor()
        self.set_mouse_visible(False)
        self.levels = []
        shipTexture = arcade.load_texture("images/playerShip1_orange.png")
        self.player1 = Player(shipTexture,"Player One",3)
        self.player1.ship.center.x = SCREEN_WIDTH/2
        self.player1.ship.center.y = SCREEN_HEIGHT/2
        
        self.levels.append(buildLevelOne(self.textures))
        self.levels.append(buildLevelTwo(self.textures))
        self.level = self.levels[0]
        self.level.players.append(self.player1)
        self.held_keys = set()
        self.ship = self.level.players[0].ship
        
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mouseCursor.x = x
        self.mouseCursor.y = y
        dx =self.player1.ship.center.x - self.mouseCursor.x
        dy =self.player1.ship.center.y - self.mouseCursor.y 
        if(dx is not 0):
            self.player1.ship.rotation = math.degrees(math.atan(dy/dx))
        if self.mouseCursor.x < self.player1.ship.center.x:
            self.player1.ship.rotation += 180

    def on_draw(self):
        """
        Called automatically by the arcade framework.0
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        self.mouseCursor.draw()
        self.level.draw()
        # TODO: draw each object

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.level.advance(delta_time)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        eventMessage = {}
        if arcade.key.LEFT in self.held_keys or arcade.key.A in self.held_keys:
            eventMessage = Message({"playerRotateCounterClockwise": self.player1})

        if arcade.key.RIGHT in self.held_keys or arcade.key.D in self.held_keys:
            eventMessage = Message({"playerRotateClockwise": self.player1})

        if arcade.key.UP in self.held_keys or arcade.key.W in self.held_keys: 
            eventMessage = Message({"playerAccelerate": self.player1})

        if arcade.key.DOWN in self.held_keys or arcade.key.S in self.held_keys:
            eventMessage = Message({"playerDeccelerate": self.player1})

        if(DEBUG and bool(eventMessage)):
            print(eventMessage)

        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE: 
                Message({"playerFire": self.player1})

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()


