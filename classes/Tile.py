#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Vec import Vec
import pygame

class Tile:
    def __init__(self, x=0, y=0, type_=0):
        self.coo = Vec(x, y)
        self.color = [None,(0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]
        self.type = type_ # 0 = empty, 1 = ..., 2 = ..., 3 = ...
        self.solid = (self.type in [2,3])
    
    def render(self, surface, position,size):
        if self.type != 0:
            pygame.draw.rect(surface, self.color[self.type], (position.x, position.y-size, size, size))
    
    def copy(self):
        """
        Creates a new copy of this tile. Keeps class and all properties
        """
        cls = self.__class__
        new = cls()
        for k,v in self.__dict__.items():
            setattr(new, k, v.copy())
        
        return new
        