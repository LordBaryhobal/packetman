#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from math import copysign

import pygame

from classes.Entity import Entity
from classes.Vec import Vec

class Player(Entity):
    """Player class, extends Entity.
    
    Holds player-specific information and manages interactions
    """

    _ENTITIES = {
        0: "player"
    }
    JUMP_SPEED = 7
    SIZE = Vec(0.8,0.8)
    
    speed = 3
    
    def jump(self):
        """Makes the player jump if on the ground"""

        if self.on_ground:
            self.vel.y = self.JUMP_SPEED
    
    def move(self, direction):
        """Moves the player horizontally

        Arguments:
            direction {int} -- negative if moving left, positive if moving right
        """

        self.vel.x = copysign(self.speed, direction)
    
    def handle_events(self, events):
        """Handles events for the player

        Arguments:
            events {list[pygame.Event]} -- list of pygame events
        """

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.jump()
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d]:
            self.move(1)
        
        if keys[pygame.K_a]:
            self.move(-1)