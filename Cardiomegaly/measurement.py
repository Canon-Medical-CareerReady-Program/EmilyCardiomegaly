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
            image_name TEXT NOT NULL,
            heart_x INTEGER,
            heart_y INTEGER,
            thorax_x INTEGER,
            thorax_y INTEGER
        );
        """
        #right now only one point of x and y are being accounted for so i want to make a 2D array that 
        #will create heart_start.x and heart_end.x then repeat this for y and thorax but if i use a 2D array 
        #that means that it will still only be heart_start, heart_end, thorax_start, and thorax_end

    @staticmethod
    def from_database(database:Database):
        all_results : List[Result] = []
        select_users = "SELECT * from image_measurements"
        print("select all measurements and create array")
        return all_results
    
    def save(self, database:Database, all_results):
        print("save the current measurements to database, if it does'nt exist insert and if it does update")
        
        if all_results.image_name == database:
            sql = f"""
            UPDATE
              image_measurements
            SET
              heart_x = {all_results['heart_x']},
              heart_y = {all_results['heart_y']},
              thorax_x = {all_results['thorax_x']},
              thorax_y = {all_results['thorax_y']}
            WHERE
              image_name = '{all_results['image_name']}'
                """
        else:
            create_users = """
            INSERT INTO
              image_measurements(image_name, heart_x, heart_y thorax_x, thorax_y)
            VALUES
              (all_results.image_name, all_results.heart_x, all_results.heart_y, all_results.thorax_x, all_results.thorax_y);
            """


