#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from math import copysign, floor
from random import uniform

import pygame

from classes.Entity import Entity
from classes.Vec import Vec

class Robot(Entity):
    """Robot which follow the player

    Friendly robot which follows the player when in range.
    """
    
    _ENTITIES = {
        0: "robot"
    }
    JUMP_SPEED = 7
    SIZE = Vec(0.5,0.5)
    VIEW_DISTANCE = 3  # in tiles
    
    speed = 2
    
    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False, world=None):
        super().__init__(pos, vel, acc, type_, highlight, world)
        self.direction = 0  # -1 = left, 1 = right
        self.speed = uniform(1,3)
    
    def jump(self):
        """Makes the Robot jump if on the ground"""

        if self.on_ground:
            self.vel.y = self.JUMP_SPEED
    
    def move(self, direction):
        """Moves the robot horizontally

        Arguments:
            direction {int} -- negative if moving left, positive if moving right
        """

        self.vel.x = copysign(self.speed, direction)
    
    def handle_events(self, events):
        """Handles event

        Manages following

        Arguments:
            events {list[pygame.Event]} -- list of pygame events
        """

        #follow the player if player is in viewdistance
        player = self.world.player
        player_pos = player.pos + player.SIZE/2
        if player_pos.distance_to(self.pos + self.SIZE/2) <= self.VIEW_DISTANCE:
            self.direction = copysign(1, self.world.player.pos.x - self.pos.x)
            self.move(self.direction)
        
            if player_pos.y - self.pos.y - self.SIZE.y/2 > 0.5:
                self.jump()
    
    def render(self, surface, pos, size, dimensions=None):
        super().render(surface, pos, size, dimensions)
        #render the viewdistance
        """pos = floor(pos + self.SIZE*Vec(1,-1)*size/2)
        pygame.draw.circle(surface, (0,255,0), pos, int(self.VIEW_DISTANCE*size),1)"""
        
    