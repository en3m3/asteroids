import scene
class LevelOne(Scene):
    def __init__(self):
        super().__init__()
        self.name = "Level One"
        self.createAsteroids()
    def createAsteroids(self):
        levelAsteroids = [LargeAsteroid(),LargeAsteroid(),LargeAsteroid(),LargeAsteroid(),LargeAsteroid()]
        self.asteroids.extend(levelAsteroids)
    def start(self):
        for asteroid in self.asteroids:
            asteroid

class LevelTwo(Scene):
    def __init__(self):
        super().__init__()        
        self.name = "Level One"
        self.createAsteroids()
    def createAsteroids(self):
        levelAsteroids = [LargeAsteroid(),LargeAsteroid(),LargeAsteroid(),LargeAsteroid(),MediumAsteroid(),SmallAsteroid(),SmallAsteroid()]
        self.asteroids.extend(levelAsteroids)
    def start(self):
        for asteroid in self.asteroids:
            asteroid