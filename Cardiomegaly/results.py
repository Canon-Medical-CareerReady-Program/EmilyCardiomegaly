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
        
    @staticmethod
    def from_database(database:Database):
        all_results : List[Result] = []
        select_users = "SELECT * from image_measurements"
        Measurement = select_users
        print("select all measurements and create array")
        return all_results
    
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

