class Point:
    def __init__(self, x:float, y:float) -> None:
        self.x = x
        self.y = y

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Point(self.x * scalar, self.y * scalar)
        else:
            raise TypeError("Unsupported operand type for multiplication")
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, other):
       if isinstance(other, (int, float)):
            return Point(self.x / other, self.y / other)
       raise TypeError("Unsupported operand type for /: 'Point' and '{}'".format(type(other).__name__))
