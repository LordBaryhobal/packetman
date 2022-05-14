#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Vec import Vec
from .Rect import Rect
import pygame, random

class Entity:
    """
    Non grid-locked entity, either alive or not
    Subject to physics
    """

    def __init__(self, pos=None, vel=None, acc=None, type_=None):
        """
        @param pos: position Vec of bottom-left corner
        @param vel: velocity Vec
        @param acc: acceleration Vec
        @param type_: type of entity (0 to 7 inc.)
        """

        if pos is None: pos = Vec()
        if vel is None: vel = Vec()
        if acc is None: acc = Vec()
        if type_ is None: type_ = random.randint(0,7)

        self.pos = pos
        self.vel = vel
        self.acc = acc

        self.color = [(100,100,100),(0,0,0),(100,0,0),(0,100,0),(0,0,100),(100,100,0),(100,0,100),(0,100,100)][type_]

        self.box = Rect(self.pos.x, self.pos.y, 1, 1) # width and height in tiles
    
    def render(self, surface, pos, size):
        """
        Renders the entity on a given surface at a given position and scale
        @param surface: pygame.Surface to render on
        @param pos: Vec instance containing the relative position of the entity on the surface
        @param size: size in pixel of a tile
        """
        
        pygame.draw.rect(surface, self.color, (pos.x, pos.y-self.box.h*size, self.box.w*size, self.box.h*size))
