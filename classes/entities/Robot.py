#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame
from classes.Entity import Entity
from classes.Vec import Vec
from math import copysign, floor
from random import uniform


class Robot(Entity):
    
    _entity = {
        0: "robot"
    }
    
    SIZE = Vec(0.5,0.5)
    
    SPEED = uniform(1,3)
    JUMP_SPEED = 7
    VIEW_DISTANCE = 3
    
    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False, world=None):
        super().__init__(pos, vel, acc, type_, highlight, world)
        self.direction = 0 #1 = right, -1 = left
        self.SPEED = uniform(1,3)
    
    def jump(self):
        """Makes the Robot jump if on the ground"""

        if self.on_ground:
            self.vel.y = self.JUMP_SPEED
    
    def move(self, direction):
        """Moves the Robot horizontally

        Arguments:
            direction {int} -- negative if moving left, positive if moving right
        """

        self.vel.x = copysign(self.SPEED, direction)
    
    def handle_events(self, events):
        #follow the player if player is in viewdistance
        player = self.world.player
        player_pos = player.pos + player.SIZE/2
        if player_pos.distance_to(self.pos + self.SIZE/2) <= self.VIEW_DISTANCE:
            self.direction = copysign(1,self.world.player.pos.x - self.pos.x)
            self.move(self.direction)
        
            if player_pos.y -self.pos.y-self.SIZE.y/2 > 0.5:
                self.jump()
    
    def render(self, surface, pos, size, dimensions=None):
        super().render(surface, pos, size, dimensions)
        #render the viewdistance
        """pos = floor(pos + self.SIZE*Vec(1,-1)*size/2)
        pygame.draw.circle(surface, (0,255,0), pos, int(self.VIEW_DISTANCE*size),1)"""
        
    