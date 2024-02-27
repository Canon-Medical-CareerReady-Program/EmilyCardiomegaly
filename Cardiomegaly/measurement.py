from point import Point
import math
from database import Database

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

    @staticmethod 
    def initialise_database(database:Database):
        create_users_table = """
        CREATE TABLE IF NOT EXISTS image_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            heart_x INTEGER,
            heart_y INTEGER,
            thorax_x INTEGER,
            thorax_y INTEGER
        );
        """

    @staticmethod
    def from_database(database:Database):
        all_results : List[Result] = []
        all_measurements 
        print("select all measurements and create array")
        return all_results
    
    def save(self, database:Database):
        print("save the current measurements to database, if it does'nt exist insert and if it does update")
        for loops in range (0, len(database)):
            if all_measurements.filename == database[loops]:
                update_post_description = """
                UPDATE
                  image_measurements
                SET
                  heart_x = all_measurements.heart_x,
                  heart_y = all_measurements.heart_y,
                  thorax_x = all_measurements.thorax_x,
                  thorax_y = all_measurements.thorax_y
                WHERE
                  filename = all_measurements.filename
                """
            else:
                create_users = """
                INSERT INTO
                  image_measurements (filename, heart_x, heart_y thorax_x, thorax_y)
                VALUES
                  (all_measurements.filename, all_measurements.heart_x, all_measurements.heart_y, all_measurements.thorax_x, all_measurements.thorax_y);
                """


