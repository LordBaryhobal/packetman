#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Vec import Vec
from .Texture import Texture
import pygame

class Tile:
    COLORS = [None,(50,50,50),(255,255,255),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]

    def __init__(self, x=0, y=0, type_=0):
        self.pos = Vec(x, y)
        self.type = type_ # 0 = empty, 1 = ..., 2 = ..., 3 = ...
        self.solid = (self.type in [2,3])
        self.texture = Texture("metal", 0)
        self.neighbors = 0
    
    def __setattr__(self, name, value):
        if name == "neighbors":
            self.texture = Texture(self.texture.name, value)
        
        super().__setattr__(name, value)
    
    def render(self, surface, position,size):
        if self.type == 0:
            return
        
        if self.type == 2:
            self.texture.render(surface, position, size)
        
        else:
            pygame.draw.rect(surface, self.COLORS[self.type], (position.x, position.y-size, size, size))
    
    def copy(self):
        """
        Creates a new copy of this tile. Keeps class and all properties
        """
        cls = self.__class__
        new = cls()
        for k,v in self.__dict__.items():
            if hasattr(v, "copy"):
                v = v.copy()
            setattr(new, k, v)
        
        return new
    
    def __repr__(self) -> str:
        return f"<Tile of type {self.type} at ({self.pos.x}, {self.pos.y})>"