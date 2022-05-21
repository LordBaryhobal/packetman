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

    COLORS = [(100,100,100),(100,0,0),(0,100,0),(0,0,100),(100,100,0),(100,0,100),(0,100,100)]

    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False):
        """
        @param pos: position Vec of bottom-left corner
        @param vel: velocity Vec
        @param acc: acceleration Vec
        @param type_: type of entity (0 to 6 inc.)
        """

        if pos is None: pos = Vec()
        if vel is None: vel = Vec()
        if acc is None: acc = Vec()
        if type_ is None: type_ = random.randint(0,6)

        self.pos = pos
        self.vel = vel
        self.acc = acc

        self.type = type_

        self.box = Rect(self.pos.x, self.pos.y, 0.5, 0.5) # width and height in tiles

        self.on_ground = False
        
        self.highlight = highlight

    def render(self, surface, pos, size):
        """
        Renders the entity on a given surface at a given position and scale
        @param surface: pygame.Surface to render on
        @param pos: Vec instance containing the relative position of the entity on the surface
        @param size: size in pixel of a tile
        """
        
        color = self.COLORS[self.type]
        pygame.draw.rect(surface, color, (pos.x, pos.y-self.box.h*size, self.box.w*size, self.box.h*size))
        if self.highlight:
            pygame.draw.rect(surface, (255,255,255), (pos.x, pos.y-self.box.h*size, self.box.w*size, self.box.h*size), 2)
            

    def physics(self, delta):
        """Simulates physics"""

        self.acc = Vec(0,-10)

        self.pos += self.vel * delta
        self.vel += self.acc * delta
        
        self.pos = round(self.pos, 6)
        self.vel = round(self.vel, 6)
        self.acc = round(self.acc, 6)

        self.update()
    
    def update(self):
        self.box.x = self.pos.x
        self.box.y = self.pos.y
