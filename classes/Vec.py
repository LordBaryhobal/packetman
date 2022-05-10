import math

class Vector() :
    def __init__(self, x, y) :
        self.x = x
        self.y = y
    def __add__(self, other) :
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other) :
        return Vector(self.x - other.x, self.y - other.y)
    def __mul__(self, other) :
        return Vector(self.x * other, self.y * other)
    def __truediv__(self, other) :
        return Vector(self.x / other, self.y / other)
    def __floordiv__(self, other) :
        return Vector(self.x // other, self.y // other)
    def __mod__(self, other) :
        return Vector(self.x % other, self.y % other)
    def __pow__(self, other) :
        return Vector(self.x ** other, self.y ** other)
    def __neg__(self) :
        return Vector(-self.x, -self.y)
    def dot(self, other) :
        return self.x * other.x + self.y * other.y
    def length(self) :
        return (self.x ** 2 + self.y ** 2) ** 0.5
    def normalize(self) :
        return self / self.length()
    def get_angle(self) :
        return math.atan2(self.y, self.x)
    def rotate(self, angle) :
        return Vector(self.x * math.cos(angle) - self.y * math.sin(angle), self.x * math.sin(angle) + self.y * math.cos(angle))
    def __abs__(self) :
        return Vector(abs(self.x), abs(self.y))