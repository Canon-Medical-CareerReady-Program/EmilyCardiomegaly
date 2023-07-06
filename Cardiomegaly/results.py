from Cardiomegaly.measurement import Measurement

class Result:
    heart = Measurement("Heart")
    thorax = Measurement("Thorax")
    def __init__(self, image_name) -> None:
        self.image_name = image_name
