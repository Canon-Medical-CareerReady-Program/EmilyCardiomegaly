from point import Point
import math


class Measurement:

    def __init__(self, body_part) -> None:
        self.body_part = body_part
        self.clear()

    def length(self):
        distance = math.sqrt((self.end.x - self.start.x) ** 2 + (self.end.y - self.start.y) ** 2)
        return distance 
    
    def clear(self):
        self.start = Point(0.0, 0.0)
        self.end = Point(0.0, 0.0)

    def mm_conversion(self):
        pass 

