from point import Point
import math


class Measurement:
    start = Point(0.0, 0.0)
    end = Point(0.0, 0.0)

    def __init__(self, body_part) -> None:
        self.body_part = body_part

    def length(self):
        distance = math.sqrt((self.end.x - self.start.x) ** 2 + (self.end.y - self.start.y) ** 2)
        return distance 
    
    def save(self):
        pass
