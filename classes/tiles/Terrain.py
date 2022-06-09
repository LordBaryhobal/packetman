#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Event import Event, listener, on
from classes.Tile import Tile
from classes.Vec import Vec
from classes.entities.Drone import Drone

class Terrain(Tile):
    """Static tile used for world building and decoration"""

    _TILES = {
        0: "metal"
    }
    CONNECTED = False

    solid = True
    

class Insulator(Terrain):
    _TILES = {
        0: "insulator"
    }
    I18N_KEY = "insulator"

class Plastic(Terrain):
    _TILES = {
        0: "plastic"
    }
    I18N_KEY = "plastic"

class ThermalConductor(Terrain):
    _TILES = {
        0: "thermal_conductor"
    }
    I18N_KEY = "thermal_conductor"
    
@listener
class Spike(Terrain):
    _TILES = {
        0: "spike"
    }
    I18N_KEY = "spike"
    solid = False
    
    @on(Event.ENTER_TILE)
    def on_enter(self, event):
        if self in event.tiles and hasattr(event.entity, "die"):
            event.entity.die()
    
@listener
class DroneSpawner(Terrain):
    _TILES = {
        0: "drone_spawner"
    }
    I18N_KEY = "drone_spawner"
    solid = False
    
    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.drone = None
    
    @on(Event.WORLD_LOADED)
    def on_world_loaded(self, event):
        if self.world and not self.world.game.config["edition"]:
            self.create_drone()
    
    def create_drone(self):
        pos = Vec(self.pos.x+0.5-Drone.SIZE.x/2, self.pos.y+0.5-Drone.SIZE.y/2)
        self.drone = Drone(pos, type_=1)
        self.world.add_entity(self.drone)
    
    @on(Event.DIE)
    def on_die(self, event):
        if self.drone and event.entity is self.drone:
            self.create_drone()
        