import arcade.color
import math

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Vect2(Point):
    def __init__(self,magnitude=0):
        super().__init__()
        self.magnitude = magnitude
    def __add__(self, vect):
        self.magnitude += vect.magnitude
        self.x += vect.x
        self.y += vect.y
        return self
    def __sub__(self, vect):
        self.magnitude -= vect.magnitude
        self.x -= vect.x
        self.y -= vect.y        
        return self
    def __mul__(self, scalar):
        self.magnitude *= scalar
        self.x *= scalar
        self.y *= scalar        
        return self
    def __repr__(self):
        return f"x:{self.x} y:{self.y} magnitude: {self.magnitude} angle: {self.getDegrees()}deg"
    def __eq__(self, vect):
        self.magnitude = vect.magnitude
        self.x = vect.x
        self.y = vect.y   
    def normalize(self):
        normal = Vect2()
        if int(self.magnitude) is not 0:
            normal.x = self.x / self.magnitude
            normal.y = self.y / self.magnitude
        normal.magnitude = 1
        return normal
    def getDegrees(self):
        angleRad = math.atan2(self.y,self.x)
        angleDeg = math.degrees(angleRad)
        return angleDeg   

class Cursor(Point):
    def __init__(self, style="crosshair", width=3):
        super().__init__()
        self.color = arcade.color.CORNELL_RED
        self.style = style
        self.width = width
    def draw(self):
        if self.style is "crosshair":
            points =(
                    (self.x,self.y+5), 
                    (self.x,self.y+15),
                    (self.x,self.y-5), 
                    (self.x,self.y-15),
                    (self.x+5,self.y), 
                    (self.x+15,self.y),        
                    (self.x-5,self.y), 
                    (self.x-15,self.y)
                    )

            arcade.draw_lines(points, self.color, self.width)

class Timer():
    def __init__(self,timer=0):
        self.timer = timer
        self.paused = True
    def advance(self):
        if(self.isTiming()):
            self.timer -= 1
    def isTiming(self):
        if(self.timer > 0):
            return True
        return False
    def start(self):
        self.paused = False
