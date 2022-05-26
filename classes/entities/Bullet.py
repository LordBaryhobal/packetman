#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Entity import Entity
from classes.Vec import Vec
from classes.Event import listener, on, Event

@listener
class Bullet(Entity):
    """
        simple bullet object that moves in a straight line
    """
    
    GRAVITY = False
    
    _entity = {
        0: "bullet",
        1: "bit"
    }
    SIZE = Vec(0.2,0.2)

    @on(Event.COLLISION_WORLD)
    def on_collision_world(self, event):
        if event.entity is self:
            self.destroy()

    @on(Event.COLLISION_ENTITY)
    def on_collision_entity(self, event):
        if self in event.entities:
            if self.world.player in event.entities:
                self.hit(self.world.player)
                self.destroy()
    
    def destroy(self):
        self.world.remove_entity(self)
    
    def hit(self, entity):
        print(f"Hit {entity}")
