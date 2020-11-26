from standard import Point

class Image:
    def __init__(self,offsetX=0,offsetY=0,texture="",height="1", width="1"):
        self.offset = Point()
        self.offset.x = offsetX
        self.offset.y = offsetY
        self.texture = ""
        self.height = height
        self.width = width