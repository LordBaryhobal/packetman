#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Entity import Entity
from math import copysign
import pygame
from .Vec import Vec

class Player(Entity):
    """
    Player class, extends Entity. Holds player-specific information
    and manages interactions
    """

    SPEED = 3
    JUMP_SPEED = 7

    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False):
        super().__init__(pos, vel, acc, type_, highlight)
        self.swinging = (False, None, None)
    
    def jump(self):
        """Makes the player jump if on the ground"""

        if self.on_ground:
            self.vel.y = self.JUMP_SPEED
    
    def move(self, direction):
        """Moves the player horizontally

        Arguments:
            direction {int} -- negative if moving left, positive if moving right
        """

        dv = copysign(self.SPEED, direction)

        if self.swinging[0]:
            """
            swing_vec = self.swinging[1]-self.pos-Vec(self.box.w/2,self.box.h/2)

            swing_len = swing_vec.length**2

            vel = self.vel.copy()
            v = self.vel.dot(swing_vec)/swing_len
            #self.vel -= swing_vec * v
            self.vel = Vec(swing_vec.y, -swing_vec.x).normalize() * dv
            """
            self.forces.append(Vec(copysign(5, direction), 0))
        
        else:
            self.vel.x = dv
    
    def start_swing(self, p):
        self.swinging = (True, p, self.pos.distance_to(p))

    def stop_swing(self):
        self.swinging = (False, None)

    def render(self, surface, pos, size):
        super().render(surface, pos, size)
        
        if self.swinging[0]:
            center = self.pos + Vec(self.box.w, self.box.h)*0.5
            pygame.draw.line(surface, (255,255,255), pos + (center-self.pos)*Vec(1,-1)*size, pos + (self.swinging[1]-self.pos)*Vec(1,-1)*size)
        
    def physics(self, delta):
        if self.swinging[0]:
            """
            half = Vec(self.box.w/2,self.box.h/2)
            swing_vec = self.swinging[1]-(self.pos+half)
            swing_vec = swing_vec.normalize()*self.swinging[2]
            self.pos = self.swinging[1] - swing_vec - half
            

            total_f = sum(self.forces, Vec(0, -20)*self.mass)
            dot = total_f.dot(swing_vec)
            swing_len = self.swinging[2]**2
            force = dot/swing_len
            self.forces.append(swing_vec * force * -1)

            v = self.vel.dot(swing_vec)/swing_len
            self.vel -= swing_vec*v
            """

            k = 20
            
            half = Vec(self.box.w/2,self.box.h/2)
            swing_vec = self.swinging[1]-(self.pos+half)
            force = swing_vec.length-self.swinging[2]*0.5
            self.forces.append(swing_vec.normalize() * force * k)
        
        super().physics(delta)