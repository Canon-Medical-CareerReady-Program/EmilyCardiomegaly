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
            thorax_end_y INTEGER,
            percentage INTEGER
        );
        """
        database.execute_query(create_users_table)
    
    @staticmethod
    def print_database(database:Database):
        print("Printing the database")
        print("id, image_name, heart_start_x, heart_start_y, heart_end_x, heart_end_y, thorax_start_x, thorax_start_y, thorax_end_x, thorax_end_y, percentage")
        select_measurements = f"""
        SELECT * FROM image_measurements;
        """

        results = database.execute_read_query(select_measurements)

        n = len(results)
        # Convert tuples to lists
        results = [list(row) for row in results]
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if results[j][10] < results[j + 1][10]:
                    results[j][10], results[j + 1][10] = results[j + 1][10], results[j][10]

        for row in results:
            print(row)
    
    def load_from_database(self, database:Database):
        select_measurements = f"""
        SELECT * FROM image_measurements WHERE image_name = '{self.image_name}';
        """
        results = database.execute_read_query(select_measurements)
        measurements_list = []

        for row in results:
            self.image_name = row[1]
            self.heart.start.x = row[2]
            self.heart.start.y = row[3]
            self.heart.end.x = row[4]
            self.heart.end.y = row[5]
            self.thorax.start.x = row[6]
            self.thorax.start.y = row[7]
            self.thorax.end.x = row[8]
            self.thorax.end.y = row[9]

            measurements_list.append(self)

        return measurements_list
    
    def save(self, database:Database):
        #print("save the current measurements to database, if it does'nt exist insert and if it does update")

        select_measurements = f"""
        SELECT * FROM image_measurements WHERE image_name = '{self.image_name}';
        """
        results = database.execute_read_query(select_measurements)

        if len(results) > 0:
            update_results = f"""
            UPDATE
              image_measurements
            SET
              heart_start_x = {self.heart.start.x},
              heart_start_y = {self.heart.start.y},
              heart_end_x = {self.heart.end.x},
              heart_end_y = {self.heart.end.y},
              thorax_start_x = {self.thorax.start.x},
              thorax_start_y = {self.thorax.start.y},
              thorax_end_x = {self.thorax.end.x},
              thorax_end_y = {self.thorax.end.y},
              percentage = {self.percentage()}
            WHERE
              image_name = '{self.image_name}'
                """
            database.execute_query(update_results)

        else:
            create_results = f"""
            INSERT INTO
              image_measurements(
              image_name, 
              heart_start_x, 
              heart_start_y, 
              heart_end_x, 
              heart_end_y, 
              thorax_start_x, 
              thorax_start_y, 
              thorax_end_x, 
              thorax_end_y,
              percentage)
            VALUES
              ('{self.image_name}', 
              {self.heart.start.x}, 
              {self.heart.start.y}, 
              {self.heart.end.x}, 
              {self.heart.end.y}, 
              {self.thorax.start.x}, 
              {self.thorax.start.y}, 
              {self.thorax.end.x}, 
              {self.thorax.end.y},
              {self.percentage()});
            """

            database.execute_query(create_results)
