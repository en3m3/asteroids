from rigidbody import Ship
from image import Image
import arcade

class Player:
    def __init__(self,shipTexture, name="", lives=3):
        self.name = name
        self.ship = Ship(shipTexture)
        self.lives = 3
    def advance(self,delta_time):
        self.ship.advance(delta_time)
    def draw(self):
        self.ship.draw()
    def hit(self, target, players):
        self.lives -= 1
        self.ship.hit(target,players)
