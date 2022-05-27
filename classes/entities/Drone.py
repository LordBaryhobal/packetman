#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame
from classes.Entity import Entity
from classes.Vec import Vec
from math import copysign, floor
from classes.Event import Event, listener, on

@listener
class Drone(Entity):
    
    _entity = {
        0: "drone",
        1: "drone_pig"
    }
    
    SPEED = 2
    SIZE = Vec(0.7,0.7)
    GRAVITY = True
    INTERACTIVE = True
    
    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False, world=None):
        super().__init__(pos, vel, acc, type_, highlight, world)
        self.following = False
    
    def handle_events(self, events):
        if self.following:
            player = self.world.player
            player_pos = player.pos + player.SIZE/2
            
            current_pos = self.pos + self.SIZE/2
            
            direction = (player_pos-current_pos).normalize()
            self.vel = direction * self.SPEED
    
    @on(Event.INTERACTION)
    def on_interract(self, event):
        if self in event.entities:
            self.update_following(not self.following)
            
    def update_following(self, following):
        self.following = following
        if not self.following:
            self.vel = Vec()
            self.GRAVITY = True
        else:
            self.GRAVITY = False
    