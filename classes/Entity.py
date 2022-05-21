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

    def __init__(self, pos=None, vel=None, acc=None, type_=None):
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
        if type_ is None: type_ = random.randint(0,6)

        self.pos = pos
        self.vel = vel
        self.acc = acc

        self.type = type_

        self.box = Rect(self.pos.x, self.pos.y, 0.5, 0.5) # width and height in tiles

        self.on_ground = False

    def render(self, surface, pos, size):
        """Renders the entity

        Renders the entity on a given surface at a given position and scale

        Arguments:
            surface {pygame.Surface} -- surface to render the entity on
            pos {Vec} -- pixel coordinates where to render on the surface
            size {int} -- size of a tile in pixels
        """
        
        color = self.COLORS[self.type]
        pygame.draw.rect(surface, color, (pos.x, pos.y-self.box.h*size, self.box.w*size, self.box.h*size))

    def physics(self, delta):
        """Simulates physics

        Arguments:
            delta {float} -- time elapsed in last fram in seconds
        """

        self.acc = Vec(0,-20)

        pos1 = self.pos.copy()
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
