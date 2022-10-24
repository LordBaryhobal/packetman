#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import math

from classes.Copyable import Copyable

class Vec(Copyable):
    """Simple vector class"""

    def __init__(self, x=0, y=0):
        """Initializes a Vec instance

        Keyword Arguments:
            x {float} -- x component (default: {0})
            y {float} -- y component (default: {0})
        """

        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        if isinstance(other, Vec):
            return Vec(self.x * other.x, self.y * other.y)
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
        """Computes the dot product of two vectors

        Arguments:
            other {Vec} -- vectors to compute the dot product with

        Returns:
            float -- dot product of `self` and `other`
        """

        return self.x * other.x + self.y * other.y
    
    @property
    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def normalize(self):
        """Returns a normalized copy of this vector

        Returns:
            Vec -- normalized copy of this vector
        """

        l = self.length
        if l == 0:
            return Vec()
        return self / l
    
    def get_angle(self):
        """Returns the angle of this vector in radians

        Returns:
            float -- angle of this vector in radians
        """

        return math.atan2(self.y, self.x)
    
    def rotate(self, angle):
        """Returns a rotated copy of this vector

        Arguments:
            angle {float} -- rotation angle in radians

        Returns:
            Vec -- rotated copy of this vector
        """

        return Vec(self.x * math.cos(angle) - self.y * math.sin(angle), self.x * math.sin(angle) + self.y * math.cos(angle))
    
    def __abs__(self):
        return Vec(abs(self.x), abs(self.y))
    
    def distance_to(self, other):
        """Returns the distance between two vectors (points)

        Arguments:
            other {Vec} -- other vector to measure distance from

        Returns:
            float -- distance between `self` and `other`
        """
        return (other-self).length
    
    def max(self, other):
        """Returns the maximum components between two vectors

        Returns a new vector with the maximum components of both vectors

        Arguments:
            other {Vec} -- other vector

        Returns:
            Vec -- maximized vector
        """
        
        return Vec(max(self.x, other.x), max(self.y, other.y))
    
    def min(self, other):
        """Returns the minimum components between two vectors

        Returns a new vector with the minimum components of both vectors

        Arguments:
            other {Vec} -- other vector

        Returns:
            Vec -- minimized vector
        """

        return Vec(min(self.x, other.x), min(self.y, other.y))
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
    
        return f"Vec({self.x}, {self.y})"
    
    def __round__(self, n=0):
        return Vec(round(self.x, n), round(self.y, n))
    
    def __floor__(self):
        return Vec(int(self.x), int(self.y))

    def get_tl_br_corners(self,other):
        """Returns the top-left and bottom-right corners of the rectangle
        formed by `self` and `other`

        Arguments:
            other {Vec} -- other vector

        Returns:
            Vec -- top-left corner
            Vec -- bottom-right corner
        """

        bl = self.min(other)
        tr = self.max(other)
        return bl, tr
    
    """The following methods make this class compatible with pygame"""

    def __getitem__(self, i):
        return [self.x, self.y][i]
    
    def __len__(self):
        return 2