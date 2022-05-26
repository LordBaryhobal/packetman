#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Copyable import Copyable
from .Vec import Vec
from .Rect import Rect
import pygame, random
from classes.Texture import Texture

class Entity(Copyable):
    """
    Non grid-locked entity, either alive or not
    Subject to physics
    """

    COLORS = [(100,100,100),(100,0,0),(0,100,0),(0,0,100),(100,100,0),(100,0,100),(0,100,100)]
    
    SIZE = Vec(0.5,0.5)
    
    GRAVITY = True
    
    _entity = {
        0: None
    }

    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False):
        """Initializes an Entity instance

        Keyword Arguments:
            pos {Vec} -- position of entity in world coordinates (default: {None})
            vel {Vec} -- velocity of entity in world units (default: {None})
            acc {Vec} -- acceleration of entity in world units (default: {None})
            type_ {int} -- entity type (default: {None})
        """

        if pos is None: pos = Vec()
        if vel is None: vel = Vec()
        if acc is None: acc = Vec()
        if type_ is None: type_ = 0

        self.pos = pos
        self.vel = vel
        self.acc = acc

        self.type = type_
        self.name = self._entity[self.type]
        self.texture = Texture(self.name, self.type) if self.name else None

        self.box = Rect(self.pos.x, self.pos.y, self.SIZE.x, self.SIZE.y) # width and height in tiles

        self.on_ground = False
        
        self.highlight = highlight

    def render(self, surface, pos, size, dimensions=None):
        """Renders the entity

        Renders the entity on a given surface at a given position and scale

        Arguments:
            surface {pygame.Surface} -- surface to render the entity on
            pos {Vec} -- pixel coordinates where to render on the surface
            size {int} -- size of a tile in pixels
            dimension {Vec} -- dimensions of the object in tiles (default: {None})
        """
        if dimensions is None:
            dimensions = self.SIZE
        
        if self.texture:
            self.texture.render(surface, pos, size, dimensions)
        else:
            color = self.COLORS[self.type]
            pygame.draw.rect(surface, color, (pos.x, pos.y-self.box.h*size, self.box.w*size, self.box.h*size))
        if self.highlight:
            pygame.draw.rect(surface, (255,255,255), (pos.x, pos.y-self.box.h*size, self.box.w*size, self.box.h*size), 2)
            

    def physics(self, delta):
        """Simulates physics

        Arguments:
            delta {float} -- time elapsed in last fram in seconds
        """
        if self.GRAVITY:
            self.acc = Vec(0,-20)

        self.pos += self.vel * delta
        self.vel += self.acc * delta
        
        self.pos = round(self.pos, 6)
        self.vel = round(self.vel, 6)
        self.acc = round(self.acc, 6)

        self.update()
    
    def update(self):
        """Updates the entity's hitbox"""
        
        self.box.x = self.pos.x
        self.box.y = self.pos.y
