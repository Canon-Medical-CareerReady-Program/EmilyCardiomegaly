from measurement import Measurement
from tkinter import filedialog
from database import Database

class Result:

    def __init__(self) -> None:
        self.heart = Measurement("Heart")
        self.thorax = Measurement("Thorax")
        self.image_name = ""  
        self.short_image_name = ""
        self.heart_x = 0
        self.heart_y = 0
        self.thorax_x = 0
        self.thorax_y = 0
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
