#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame
from classes.Entity import Entity
from classes.Vec import Vec
from .Bullet import Bullet
from time import time
from math import floor

class Hacker(Entity):
    
    _entity = {
        0:"hacker"
    }
    
    SIZE = Vec(1,1)
    
    RELOAD_TIME = 1
    BULLET_SPEED = 10
    VIEW_DISTANCE = 3
    
    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False):
        super().__init__(pos, vel, acc, type_, highlight)
        self.lastbulletshot = time()
    
    def handle_events(self, events):
        if time() - self.lastbulletshot > self.RELOAD_TIME:
            self.lastbulletshot = time()
            self.shoot()
        
    def shoot(self):
        player = self.world.player
        player_pos = player.pos + player.SIZE/2
        if player_pos.distance_to(self.pos + self.SIZE/2) <= self.VIEW_DISTANCE:
            bullet_pos = self.pos + self.SIZE/2
            bullet_vel = (player_pos - bullet_pos).normalize() * self.BULLET_SPEED
            self.world.add_entity(Bullet(bullet_pos, bullet_vel))
    
    def render(self, surface, pos, size, dimensions=None):
        super().render(surface, pos, size, dimensions)
        #render the viewdistance
        """pos = floor(pos + self.SIZE*Vec(1,-1)*size/2)
        pygame.draw.circle(surface, (0,255,0), pos, int(self.VIEW_DISTANCE*size),1)"""
    
    