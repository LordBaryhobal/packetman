#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import math

class Vec() :
    """
    Simple vector class
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return Vec(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        return Vec(self.x / other, self.y / other)
    
    def __floordiv__(self, other):
        return Vec(self.x // other, self.y // other)
    
    def __mod__(self, other):
        return Vec(self.x % other, self.y % other)
    
    def __pow__(self, other):
        return Vec(self.x ** other, self.y ** other)
    
    def __neg__(self):
        return Vec(-self.x, -self.y)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    @property
    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def normalize(self):
        l = self.length
        if l == 0:
            return Vec()
        return self / l
    
    def get_angle(self):
        return math.atan2(self.y, self.x)
    
    def rotate(self, angle):
        return Vec(self.x * math.cos(angle) - self.y * math.sin(angle), self.x * math.sin(angle) + self.y * math.cos(angle))
    
    def __abs__(self):
        return Vec(abs(self.x), abs(self.y))
    
    def distance_to(self, other):
        return (other-self).length
    
    def max(self, other):
        return Vec(max(self.x, other.x), max(self.y, other.y))
    
    def min(self, other):
        return Vec(min(self.x, other.x), min(self.y, other.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y