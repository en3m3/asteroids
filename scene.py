import arcade

DEBUG = False

class Scene:
    def __init__(self):
        self.asteroids = []
        self.players = []
        self.bullets = []
        self.menus = []
    def draw(self):
        for bullet in self.bullets:
            bullet.draw()          
        for asteroid in self.asteroids:
            asteroid.draw()
        for player in self.players:
            player.draw()
        for menu in self.menus:
            menu.draw()
    def start(self):
        pass
    def advance(self,delta_time):
        for bullet in self.bullets:
            bullet.advance(delta_time)   
            if not bullet.life.isTiming():
                self.bullets.remove(bullet)
        for asteroid in self.asteroids:
            asteroid.advance(delta_time)
        for player in self.players:
            player.ship.advance(delta_time)
        for menu in self.menus:
            menu.advance(delta_time)
        self.checkHits()  
    def checkHits(self):
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                hit = bullet.hitBox.checkHit(bullet, asteroid)
                if hit == True:
                    bullet.hit(asteroid,self.bullets)
                    asteroid.hit(bullet,self.asteroids)
                    self.bullets.remove(bullet)
            for player in self.players:
                hit = bullet.hitBox.checkHit(bullet, player.ship)
                if hit == True:
                    player.hit(bullet,self.players)
                    bullet.hit(player,self.bullets)                    
                    if(DEBUG):
                        print("player hit detected")                
        for asteroid in self.asteroids:
            for player in self.players:
                hit = asteroid.hitBox.checkHit(asteroid, player.ship)
                if hit == True:
                    asteroid.hit(player.ship,self.asteroids)
                    player.hit(asteroid,self.players)
                    if(DEBUG):
                        print("player hit detected")    
            for otherAsteroid in self.asteroids:
                if(otherAsteroid.center.x is not asteroid.center.x and otherAsteroid.center.y is not asteroid.center.y):
                    hit = asteroid.hitBox.checkHit(asteroid, otherAsteroid)                            
                    if hit == True:
                        asteroid.hit(asteroid, self.asteroids)
                        asteroid.hit(otherAsteroid, self.asteroids)