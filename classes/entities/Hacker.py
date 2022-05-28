#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from math import floor
from time import time

import pygame

from classes.entities.Bullet import Bullet
from classes.Entity import Entity
from classes.Vec import Vec

class Hacker(Entity):
    """Hacker ennemy

    Shoots towards the player when in a certain view distance.
    """
    
    _ENTITIES = {
        0:"hacker"
    }
    BULLET_SPEED = 10
    RELOAD_TIME = 1  # in seconds
    SIZE = Vec(1,1)
    VIEW_DISTANCE = 3  # in tiles
    
    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False):
        super().__init__(pos, vel, acc, type_, highlight)
        self.last_shot = time()
    
    def handle_events(self, events):
        """Handles events

        Manages shooting

        Arguments:
            events {list[pygame.Event]} -- list of pygame events
        """

        if time() - self.last_shot > self.RELOAD_TIME:
            player = self.world.player
            player_pos = player.pos + player.SIZE/2
            if player_pos.distance_to(self.pos + self.SIZE/2) <= self.VIEW_DISTANCE:
                self.shoot(player_pos)
        
    def shoot(self, pos):
        """Shoots a bullet

        Arguments:
            pos {Vec} -- target position
        """

        bullet_pos = self.pos + self.SIZE/2
        bullet_vel = (pos - bullet_pos).normalize() * self.BULLET_SPEED
        self.world.add_entity(Bullet(bullet_pos, bullet_vel))
        self.last_shot = time()
    
    def render(self, surface, pos, size, dimensions=None):
        super().render(surface, pos, size, dimensions)
        #render the viewdistance
        """pos = floor(pos + self.SIZE*Vec(1,-1)*size/2)
        pygame.draw.circle(surface, (0,255,0), pos, int(self.VIEW_DISTANCE*size),1)"""
    
    