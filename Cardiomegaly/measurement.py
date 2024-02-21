from point import Point
import math
from database import Database


class Measurement:

    def __init__(self, body_part) -> None:
        self.body_part = body_part
        self.heart = 0
        self.thorax = 0
        self.clear()

    def length(self):
        distance = math.sqrt((self.end.x - self.start.x) ** 2 + (self.end.y - self.start.y) ** 2)
        return distance 
    
    def clear(self):
        self.start = Point(0.0, 0.0)
        self.end = Point(0.0, 0.0)

    @staticmethod 
    def initialise_database(database:Database):
        print("Create tables")

    @staticmethod
    def from_database(database:Database):
        all_results : List[Result] = []
        print("select all measurements and create array")
        return all_results
    
    def save(self, database:Database):
        print("save the current measurements to database, if it doesnt exist insert and if it does update")


