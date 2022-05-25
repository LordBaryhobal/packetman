#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Copyable import Copyable
from .Vec import Vec
from .Texture import Texture
import pygame

class Tile(Copyable):
    COLORS = [None,(50,50,50),(255,255,255),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]

    _tiles = {
        0: None
    }

    def __init__(self, x=0, y=0, type_=0):
        """Initializes a Tile instance

        Keyword Arguments:
            x {int} -- x coordinate (default: {0})
            y {int} -- y coordinate (default: {0})
            type_ {int} -- tile type, 0 if empty (default: {0})
        """

        self.pos = Vec(x, y)
        self.type = type_
        self.name = self._tiles[self.type]
        self.texture = Texture(self.name, self.type) if self.name else None
        self.neighbors = 0
    
    def __setattr__(self, name, value):
        if name == "neighbors" and self.texture:
            self.texture = Texture(self.texture.name, value)
        
        super().__setattr__(name, value)
    
    def render(self, surface, pos, size):
        """Renders the tile

        Arguments:
            surface {pygame.Surface} -- surface to render the tile on
            pos {Vec} -- pixel coordinates where to render on the surface
            size {int} -- size of a tile in pixels
        """
        
        if self.texture:
            self.texture.render(surface, pos, size)
        
        """
        else:
            pygame.draw.rect(surface, self.COLORS[self.type], (pos.x, pos.y-size, size, size))"""
    
    def __repr__(self):
        return f"<Tile of type {self.type} at ({self.pos.x}, {self.pos.y})>"