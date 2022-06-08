#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

from classes.Entity import Entity
from classes.Event import Event, listener, on
from classes.Logger import Logger
from classes.Rect import Rect
from classes.TextManager import TextManager
from classes.Vec import Vec

class Trigger(Entity):
    """Simple trigger entity"""
    
    SIZE = Vec(1, 1)

    gravity = False
    
    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False, world=None):
        super().__init__(pos, vel, acc, type_, highlight, world)
        self.text_id = ""
        self.triggered = False

    def trigger(self):
        if not self.triggered:
            self.triggered = True
            if self.text_id:
                TextManager.show(self.text_id)
            else:
                Logger.warn(f"{self.__class__.__name__} triggered but no text id was set")
    
    def render(self, surface, hud_surf, pos, size, dimensions=None):
        if self.world.game.config["edition"]:
            super().render(surface, hud_surf, pos, size, dimensions)
        
        elif self.triggered:
            pygame.draw.rect(surface, (77,196,240), [pos.x,pos.y-self.SIZE.y*size,self.SIZE.x*size, self.SIZE.y*size],2)

@listener
class PlayerTrigger(Trigger):
    _ENTITIES = {
        0: "player_trigger"
    }
    I18N_KEY = "player_trigger"

    @on(Event.COLLISION_ENTITY)
    def trigger(self, event):
        if self in event.entities:
            if self.world.player in event.entities:
                super().trigger()

@listener
class TileTrigger(Trigger):
    _ENTITIES = {
        0: "tile_trigger"
    }
    I18N_KEY = "tile_trigger"

    @on(Event.TILE_TRIGGER_UPDATE)
    def trigger(self, event):
        r = Rect(event.tile.pos.x, event.tile.pos.y, 1, 1)
        
        if self.box.overlaps(r):
            if event.tile.powered_by > 0:
                super().trigger()