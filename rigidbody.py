import arcade
from hitbox import CircleHitBox
from standard import Vect2, Timer
from image import Image
import math
from standard import Point
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

DEBUG = False


def wrap(body):
    if body.center.x > SCREEN_WIDTH:
        body.center.x = 0
    elif body.center.x < 0:
        body.center.x = SCREEN_WIDTH

    if body.center.y > SCREEN_HEIGHT:
        body.center.y = 0
    elif body.center.y < 0:
        body.center.y = SCREEN_HEIGHT    

class Rigidbody:
    def __init__(self):
        self.hitBox = CircleHitBox()
        self.velocity = Vect2()
        self.center = Point()
        self.alive = True
        self.speed = 0

    def draw(self):
        pass

    def advance(self, delta_time):
        movement = self.velocity.normalize()
        self.center.x += movement.x * self.velocity.magnitude * delta_time
        self.center.y += movement.y * self.velocity.magnitude * delta_time
        wrap(self)        
    def hit(self):
        pass


class Ship(Rigidbody):
    def __init__(self, texture):
        super().__init__()
        self.hitBox.clip = True  
        self.invulnerable = Timer(300)
        self.invulnerable.paused = False
        self.texture = texture
        self.turnspeed = 3
        self.speed = 0
        self.rotation = 0
        self.radius = 30
        self.acellerationRate = 2.5
        self.decellerationRate = 2.5
        self.maxSpeed = 400
        self.center.x = 400
        self.center.y = 300

    def draw(self):
        if self.alive:
            arcade.draw_texture_rectangle(
            self.center.x, self.center.y, self.radius, self.radius, self.texture, self.rotation-90, 1)
            if(self.invulnerable.isTiming()):
                arcade.draw_circle_outline(self.center.x,self.center.y,self.radius+25,arcade.color.AQUA)

    def advance(self, delta_time):
        if(self.speed > self.maxSpeed):
            self.speed = self.maxSpeed
        elif(self.speed < self.maxSpeed*-1):
            self.speed = self.maxSpeed * -1  
        direction = self.velocity.normalize()
        self.velocity.magnitude = self.speed       
        self.velocity.x = direction.x *self.velocity.magnitude
        self.velocity.y = direction.y *self.velocity.magnitude  
        self.invulnerable.advance() 
        if(self.invulnerable.isTiming()):
            self.hitBox.clip = False
        else:
            self.hitBox.clip = True
        super().advance(delta_time)

    def accelerate(self):
        if self.speed < self.maxSpeed:
            self.speed += self.acellerationRate
        acceleationVelocity = Vect2()
        acceleationVelocity.x = math.cos(
            math.radians(self.rotation))*self.acellerationRate
        acceleationVelocity.y = math.sin(
            math.radians(self.rotation))*self.acellerationRate
        acceleationVelocity.magnitude = self.acellerationRate
        self.velocity += acceleationVelocity
        self.speed = self.velocity.magnitude if self.velocity.magnitude < self.maxSpeed else self.maxSpeed

    def deccelerate(self):
        if self.speed > self.maxSpeed*-1:
            self.speed -= self.decellerationRate
        acceleationVelocity = Vect2()
        acceleationVelocity.x = math.cos(
            math.radians(self.rotation))*self.decellerationRate
        acceleationVelocity.y = math.sin(
            math.radians(self.rotation))*self.decellerationRate
        acceleationVelocity.magnitude = self.decellerationRate
        self.velocity -= acceleationVelocity
        self.speed = self.velocity.magnitude if self.velocity.magnitude < self.maxSpeed else self.maxSpeed

    def rotateCC(self):
        self.rotation += self.turnspeed
        self.rotation = self.rotation

    def rotateC(self):
        self.rotation -= self.turnspeed
        self.rotation = self.rotation
    def hit(self, target,asteroids):
        self.alive = False        


class Asteroid(Rigidbody):
    def __init__(self):
        super().__init__()
        self.rotation = 0
        self.rotationRate = 0
        self.radius = 0
        self.hitBox.radius = 10
        self.speed = 0
        self.radius = 2
        self.texture = arcade.load_texture("images/meteorGrey_med1.png")

    def draw(self):
        arcade.draw_texture_rectangle(
            self.center.x, self.center.y, self.radius, self.radius, self.texture, self.rotation, 1)

    def advance(self, delta_time):
        self.rotation += self.rotationRate
        self.rotation = self.rotation
        movement = self.velocity.normalize()
        self.center.x += movement.x * self.speed * delta_time
        self.center.y += movement.y * self.speed * delta_time
        wrap(self)        
    def hit(self):
        pass

class LargeAsteroid(Asteroid):
    def __init__(self):
        super().__init__()
        self.rotationRate = 1
        self.radius = 60
        self.hitBox.clip = True  
        self.hitBox.radius = 20
        self.speed = 5
        angle = math.radians(random.randint(0, 359))
        self.velocity.magnitude = self.speed
        self.velocity.x = math.cos(angle)*self.speed
        self.velocity.y = math.sin(angle)*self.speed
        self.image = arcade.load_texture("images/meteorGrey_big1.png")
    def hit(self, target, asteroids):
        if self.hitBox.clip:
            if(DEBUG):
                print("asteroid hit")            
            self.alive = False
            self.hitBox.clip = False
    
            asteroids.remove(self)  
            asteroid = MediumAsteroid()
            asteroidVelocity = Vect2()
            asteroidVelocity.x = 3
            asteroidVelocity.y = 3
            asteroidVelocity.magnitude = 3
            asteroid.center.x = self.center.x
            asteroid.center.y = self.center.y
            asteroid.velocity = asteroidVelocity
            asteroids.append(asteroid) 

            asteroid = MediumAsteroid()
            asteroid.center.x = self.center.x
            asteroid.center.y = self.center.y
            asteroidVelocity = Vect2()
            asteroidVelocity.x = -3
            asteroidVelocity.y = 3
            asteroidVelocity.magnitude = 3
            asteroid.velocity = asteroidVelocity            
            asteroids.append(asteroid)          

            asteroid = MediumAsteroid()
            asteroid.center.x = self.center.x
            asteroid.center.y = self.center.y                                           
            asteroidVelocity = Vect2()
            asteroidVelocity.x = 0
            asteroidVelocity.y = 6
            asteroidVelocity.magnitude = 3
            asteroid.velocity = asteroidVelocity
            asteroids.append(asteroid)                 



class MediumAsteroid(Asteroid):
    def __init__(self, velocity=Vect2()):
        super().__init__()
        self.rotationRate = -2
        self.radius = 20
        self.hitBox.radius = 20
        self.speed = 15
        self.hitBox.clip = True          
        angle = math.radians(random.randint(0, 359))
        self.velocity.magnitude = self.speed
        self.velocity.x = math.cos(angle)*self.speed
        self.velocity.y = math.sin(angle)*self.speed
        self.image = arcade.load_texture("images/meteorGrey_med1.png")
    def hit(self, target,asteroids):
        if(type(target) is Ship or type(target) is Bullet):        
            if self.hitBox.clip:     
                self.alive = False
                self.hitBox.clip = False            
                asteroids.remove(self)  
                asteroid = SmallAsteroid()
                asteroid.center.x = self.center.x
                asteroid.center.y = self.center.y  
                asteroidVelocity = Vect2()          
                asteroidVelocity.x = 0
                asteroidVelocity.y = 2
                asteroidVelocity.magnitude = 5            
                asteroid.velocity = asteroidVelocity
                asteroids.append(asteroid) 
  

              

class SmallAsteroid(Asteroid):
    def __init__(self, velocity=Vect2()):
        super().__init__()
        self.rotationRate = 5
        self.radius = 10
        self.speed = 20
        self.hitBox.radius = 10
        self.hitBox.clip = True          
        angle = math.radians(random.randint(0, 359))
        self.velocity.magnitude = self.speed
        self.velocity.x = math.cos(angle)*self.speed
        self.velocity.y = math.sin(angle)*self.speed
        self.image = arcade.load_texture("images/meteorGrey_small1.png")
    def hit(self, target,asteroids):
        if self.hitBox.clip:
            self.alive = False
            self.hitBox.clip = False            
            if(DEBUG):
                print("asteroid hit")         
            asteroids.remove(self)            




class Bullet(Rigidbody):
    def __init__(self, ship):      
        super().__init__()
        self.radius = 1
        self.life = Timer(60) 
        self.life.paused = False
        self.hitBox.clip = False    
        self.speed = Vect2()
        self.speed = ship.speed/50 + 5
        self.activateTimer = Timer(10)
        self.activateTimer.paused = False
        self.rotation = ship.rotation
        self.center = Point(ship.center.x,ship.center.y)
        self.velocity.magnitude = self.speed
        self.velocity.x = math.cos(math.radians(ship.rotation))*self.speed 
        self.velocity.y = math.sin(math.radians(ship.rotation))*self.speed
        self.texture = arcade.load_texture("images/laserBlue01.png")
    def hit(self, target,bullets):
        if self.hitBox.clip:
            self.alive = False
            self.hitBox.clip = False            
            if(DEBUG):
                print("bullet hit") 
                     
    def draw(self):
        arcade.draw_texture_rectangle(
            self.center.x, self.center.y, self.texture.width, self.texture.height, self.texture, self.rotation, 1)         
    def advance(self, delta_time):
        self.activateTimer.advance()
        self.life.advance()
        movement = self.velocity.normalize()
        self.center.x += movement.x * self.velocity.magnitude
        self.center.y += movement.y * self.velocity.magnitude
        if not self.activateTimer.isTiming():
            self.hitBox.clip = True
            if(DEBUG):
                print("bullet Active")
        wrap(self)        