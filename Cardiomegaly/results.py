from measurement import Measurement
from tkinter import filedialog
from database import Database

class Result:

    def __init__(self) -> None:
        self.heart = Measurement("Heart")
        self.thorax = Measurement("Thorax")
        self.image_name = ""  
        self.short_image_name = ""
        self.pixel_spacing = [1.0, 1.0]   
        self.patient_ID = []
        self.patient_gender = []
        self.patient_age = []   

    def ratio(self):
        ratio = self.heart.length() / self.thorax.length()
        return ratio
    
    def percentage(self):
        percentage = round(self.ratio()*100, 2)
        return percentage

    def symptoms(self) -> bool:
        return self.ratio() > 0.5
    
    @staticmethod 
    def initialise_database(database:Database):
        create_users_table = """
        CREATE TABLE IF NOT EXISTS image_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT NOT NULL,
            heart_start_x INTEGER,
            heart_start_y INTEGER,
            heart_end_x INTEGER,
            heart_end_y INTEGER,
            thorax_start_x INTEGER,
            thorax_start_y INTEGER,
            thorax_end_x INTEGER,
            thorax_end_y INTEGER
        );
        """
        database.execute_query(create_users_table)
        
    @staticmethod
    def load_from_database(database:Database):
        select_measurements = """
        SELECT * FROM image_measurements;
        """
        results = database.execute_read_query(select_measurements)
        measurements_list = []

        for row in results:
            result = Result()
            result.image_name = row[1]
            result.heart.start.x = row[2]
            result.heart.start.y = row[3]
            result.heart.end.x = row[4]
            result.heart.end.y = row[5]
            result.thorax.start.x = row[6]
            result.thorax.start.y = row[7]
            result.thorax.end.x = row[8]
            result.thorax.end.y = row[9]

            measurements_list.append(result)

        return measurements_list
    
    def save(self, database:Database, all_results):
        print("save the current measurements to database, if it does'nt exist insert and if it does update")
        
        if self.image_name == database:
            sql = f"""
            UPDATE
              image_measurements
            SET
              heart_start_x = {all_results['self.heart.start.x']},
              heart_start_y = {all_results['self.heart.start.y']},
              heart_end_x = {all_results['self.heart.end.x']},
              heart_end_y = {all_results['self.heart.end.y']},
              thorax_start_x = {all_results['self.thorax.start.x']},
              thorax_start_y = {all_results['self.thorax.start.y']},
              thorax_end_x = {all_results['self.thorax.end.x']},
              thorax_end_y = {all_results['self.thorax.end.y']}
            WHERE
              image_name = '{all_results['self.image_name']}'
                """
        else:
            create_users = """
            INSERT INTO
              image_measurements(image_name, heart_x, heart_y thorax_x, thorax_y)
            VALUES
              (self.image_name, self.heart.start.x, self.heart.start.y, self.heart.end.x, self.heart.end.y, self.thorax.start.x, self.thorax.start.y, self.thorax.end.x, self.thorax.end.y);
            """

