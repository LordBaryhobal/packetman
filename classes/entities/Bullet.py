#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Entity import Entity
from classes.Event import Event, listener, on
from classes.Player import Player
from classes.SoundManager import SoundManager
from classes.Vec import Vec

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
        """Destroys this bullet"""

        self.world.remove_entity(self)
    
    def hit(self, entity):
        """Processes a hit with an entity

        Arguments:
            entity {Entity} -- entity hit by this bullet
        """

        print(f"Hit {entity}")
        if isinstance(entity, Player):
            SoundManager.play("entity.player.get_hit")
