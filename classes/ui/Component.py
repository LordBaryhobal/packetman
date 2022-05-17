#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Constraints import *

class Component:
    """Basic UI component extend by all other UI elements"""

    def __init__(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def render(self, surface, x, y, w, h):
        pass
    
    @property
    def x(self):
        return self._x.val
    
    @property
    def y(self):
        return self._y.val
    
    @property
    def w(self):
        return self._w.val
    
    @property
    def h(self):
        return self._h.val