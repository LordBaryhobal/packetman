#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame
from classes.Entity import Entity
from classes.Vec import Vec
from math import copysign, floor


class Drone(Entity):
    
    _entity = {
        0: "drone",
        1: "drone_pig"
    }
    
    SPEED = 2
    SIZE = Vec(0.7,0.7)
    GRAVITY = False
    
    def handle_events(self, events):
        player = self.world.player
        player_pos = player.pos + player.SIZE/2
        
        current_pos = self.pos + self.SIZE/2
        
        direction = (player_pos-current_pos).normalize()
        self.vel = direction * self.SPEED
    