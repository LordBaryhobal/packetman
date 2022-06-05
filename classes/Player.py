#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from math import copysign

import pygame

from classes.Entity import Entity
from classes.Event import Event, listener, on
from classes.SoundManager import SoundManager
from classes.Vec import Vec
from classes.tiles.Detection_tile import Detection_tile
from time import time

@listener
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
    TIME_STEP = 0.3
    
    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False, world=None):
        super().__init__(pos, vel, acc, type_, highlight, world)
        self.finishing_level = False
        self.last_step = time()
    
    def jump(self):
        """Makes the player jump if on the ground"""

        if self.on_ground:
            self.vel.y = self.JUMP_SPEED
            SoundManager.play("entity.player.jump")
    
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
    
    @on(Event.ENTER_TILE)
    def on_enter_tile(self, event):
        if event.entity is self:
            for tile in event.tiles:
                if isinstance(tile, Detection_tile):
                    if self.on_ground:
                        self.world.game.finish_level()
                    else:
                        self.finishing_level = True
                    break
    
    @on(Event.HIT_GROUND)
    def on_hit_ground(self, event):
        if event.entity is self:
            SoundManager.play("entity.player.hit_ground")
            if self.finishing_level:
                self.finishing_level = False
                self.world.game.finish_level()
    
    def play_step(self, material=""):
        newtime = time()
        if newtime - self.last_step > self.TIME_STEP:
            SoundManager.play("entity.player.step_" + material)
            self.last_step = newtime
