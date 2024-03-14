class Point:
    def __init__(self, x:float, y:float) -> None:
        self.x = x
        self.y = y

    def __truediv__(self, other):
       if isinstance(other, (int, float)):
            return Point(self.x / other, self.y / other)
