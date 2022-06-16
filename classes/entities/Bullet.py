#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Entity import Entity
from classes.Event import Event, listener, on
from classes.SoundManager import SoundManager
from classes.Vec import Vec
from classes.entities.Triggers import Trigger

@listener
class Bullet(Entity):
    """Simple bullet object that moves in a straight line"""
    
    _ENTITIES = {
        0: "bullet",
        1: "bit"
    }
    I18N_KEY = "bullet"
    
    SIZE = Vec(0.2,0.2)

    gravity = False
    
    DAMAGE = 1
    
    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False, world=None, owner= None):
        super().__init__(pos, vel, acc, type_, highlight, world)
        
        self.owner = owner

    @on(Event.COLLISION_WORLD)
    def on_collision_world(self, event):
        if event.entity is self:
            self.die()

    @on(Event.COLLISION_ENTITY)
    def on_collision_entity(self, event):
        if self in event.entities:
            for entity in event.entities:
                self.damage(entity)
    
    def damage(self, entity):
        
        if entity is not self and entity is not self.owner and not isinstance(entity, Trigger):
            self.die()
            entity.hit(self.DAMAGE)
