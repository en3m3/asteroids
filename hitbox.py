import math
class Hitbox:
    def __init__(self, radius=0):
        self.clip = False        
        self.radius = radius
    def checkHit(self, insider, outsider):
        pass
        
class CircleHitBox(Hitbox):
    def __init__(self, radius=0):
        super().__init__()
        self.radius = radius
    def checkHit(self, insider, outsider):
        distanceX = insider.center.x - outsider.center.x
        distanceY = insider.center.y - outsider.center.y
        distance = math.sqrt( (distanceX*distanceX) + (distanceY*distanceY) )
        if (distance <= outsider.radius+self.radius):
            if(insider.hitBox.clip and outsider.hitBox.clip):
                return True
        return False
        

# class rectangleHitbox(Hitbox):
#     def __init__(self,width=0,height=0):
#         self.width = width
#         self.height = height
#     def checkHit(self,insider, outsider):
#         if (insider.center.x >= rx &&         // right of the left edge AND
#             px <= rx + rw &&    // left of the right edge AND
#             py >= ry &&         // below the top AND
#             py <= ry + rh) {    // above the bottom
#                 return true;
#         }
#         return false;   