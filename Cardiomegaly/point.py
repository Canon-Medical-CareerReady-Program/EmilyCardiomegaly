class Point:
    def __init__(self, x:float, y:float) -> None:
        #defining the points x and y as floats and assigning them variables 
        self.x = x
        self.y = y
    
    #truediv is a special python method
    #this allows instances of the Points class to be divided by another value
    def __truediv__(self, other):
       #this checks if the divider is an integer or a float
       if isinstance(other, (int, float)):
            #if the divisor is a number, it will divide the x and y coordinated currently stored by it
            #this then returns the newly divided Point
            return Point(self.x / other, self.y / other)
