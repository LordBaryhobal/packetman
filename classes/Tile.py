#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Vec import Vec
from .Texture import Texture
import pygame

class Tile:
    COLORS = [None,(50,50,50),(255,255,255),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]

    def __init__(self, x=0, y=0, type_=0):
        """Initializes a Tile instance

        Keyword Arguments:
            x {int} -- x coordinate (default: {0})
            y {int} -- y coordinate (default: {0})
            type_ {int} -- tile type, 0 if empty (default: {0})
        """

        self.pos = Vec(x, y)
        self.type = type_ # 0 = empty, 1 = ..., 2 = ..., 3 = ...
        self.solid = (self.type in [-1,2,3])
        self.texture = Texture("metal", 0)
        self.neighbors = 0
    
    def __setattr__(self, name, value):
        if name == "neighbors":
            self.texture = Texture(self.texture.name, value)
        
        super().__setattr__(name, value)
    
    def render(self, surface, pos, size):
        """Renders the tile

        Arguments:
            surface {pygame.Surface} -- surface to render the tile on
            pos {Vec} -- pixel coordinates where to render on the surface
            size {int} -- size of a tile in pixels
        """

        if self.type == 0:
            return
        
        if self.type == 2:
            self.texture.render(surface, pos, size)
        
        else:
            pygame.draw.rect(surface, self.COLORS[self.type], (pos.x, pos.y-size, size, size))
    
    def copy(self):
        """Creates a new copy this tile

        Keeps class and all properties

        Returns:
            Tile -- deepcopy of this tile
        """

        cls = self.__class__
        new = cls()
        for k,v in self.__dict__.items():
            if hasattr(v, "copy"):
                v = v.copy()
            setattr(new, k, v)
        
        return new
    
    def __repr__(self):
        return f"<Tile of type {self.type} at ({self.pos.x}, {self.pos.y})>"