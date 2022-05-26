#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Entity import Entity
from math import copysign
from .Vec import Vec
from .Event import Event, on, listener
import pygame

@listener
class Player(Entity):
    """
    Player class, extends Entity. Holds player-specific information
    and manages interactions
    """

    SPEED = 3
    JUMP_SPEED = 7
    
    SIZE = Vec(0.8,0.8)
    
    _entity = {
        0: "player"
    }
    
    def jump(self):
        """Makes the player jump if on the ground"""

        if self.on_ground:
            self.vel.y = self.JUMP_SPEED
    
    def move(self, direction):
        """Moves the player horizontally

        Arguments:
            direction {int} -- negative if moving left, positive if moving right
        """

        self.vel.x = copysign(self.SPEED, direction)
    
    def handle_events(self, events):
        """Handles events for the player

        Arguments:
            events {list} -- list of pygame events
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
    
    @on(Event.COLLISION_WORLD)
    def on_world_collision(self, event):
        if event.entity is self:
            self.jump()