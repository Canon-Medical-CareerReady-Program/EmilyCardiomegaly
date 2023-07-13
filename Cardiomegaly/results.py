from measurement import Measurement
from tkinter import filedialog

class Result:

    def __init__(self) -> None:
        self.heart = Measurement("Heart")
        self.thorax = Measurement("Thorax")
        self.image_name = ""        

    def ratio(self):
        ratio = self.heart.length() / self.thorax.length()
        return ratio
    
    def percentage(self):
        percentage = round(self.ratio()*100, 2)
        return percentage
    
    def save(self):
        pass

    def symptoms(self) -> bool:
        return self.ratio() > 0.5
