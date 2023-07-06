from measurement import Measurement

class Result:
    heart = Measurement("Heart")
    thorax = Measurement("Thorax")
    image_name = ""
    def __init__(self) -> None:
        pass

    def ratio(self):
        ratio = self.heart.length() / self.thorax.length()
        return ratio
    
    def percentage(self):
        percentage = round(self.ratio()*100, 2)
        return percentage