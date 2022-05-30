#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Event import Event, listener, on
from classes.Tile import Tile
from classes.Vec import Vec

class Electrical(Tile):
    """Electrical component"""
    pass
Electrical.CONNECT_TO = (Electrical, )

class Input(Electrical):
    """Input component which can produce electricity"""

    _TILES = {
        0: "input"
    }
    
    def create_event(self, pressed):
        neighbors = []
        for i, delta in enumerate((Vec(0, 1), Vec(1, 0), Vec(0, -1), Vec(-1, 0))):
            ntile = self.world.get_tile(self.pos+delta)
            if isinstance(ntile, Electrical):
                neighbors.append((i,ntile))
        if neighbors:
            event = Event(Event.CIRCUIT_CHANGE)
            event.power = pressed
            event.input = self
            event.tiles = neighbors
            self.world.game.events.append(event)

class Output(Electrical):
    """Output component which does stuff when powered"""

    _TILES = {
        0: "output"
    }

@listener
class Plate(Input):
    """Pressure plate"""

    _TILES = {
        0: "plate"
    }
    
    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.pressed = False
        self.entity_count = 0
    
    @on(Event.ENTER_TILE)
    def on_enter(self, event):
        if self in event.tiles:
            if self.entity_count == 0:
                self.change_pressed(True)
            self.entity_count += 1
    
    @on(Event.EXIT_TILE)
    def on_exit(self, event):
        if self in event.tiles:
            self.entity_count -= 1
            if self.entity_count == 0:
                self.change_pressed(False)
    
    def change_pressed(self, pressed):
        """Updates pressed state

        Arguments:
            pressed {bool} -- new pressed state
        """
        self.create_event(pressed=pressed)
        self.pressed = pressed
        self.texture.id = int(self.pressed)
    
@listener
class Button(Input):
    """Togglable button"""

    _TILES = {
        0: "button"
    }

    interactive = True
    pressed = False
    rotatable = True
    
    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.rotation = 0
        self.set_pressed(False)

    @on(Event.INTERACTION)
    def on_interact(self, event):
        if self in event.tiles:
            self.set_pressed(not self.pressed)
    
    def set_pressed(self, pressed=True):
        """Sets pressed state

        Keyword Arguments:
            pressed {bool} -- new pressed state (default: {True})
        """
        if self.pressed != pressed:
            self.create_event(pressed=pressed)
        self.pressed = pressed
        self.update_texture()
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
        self.update_texture()
    
    def update_texture(self):
        self.texture.id = (int(self.pressed) << 2) + self.rotation
    
    @on(Event.WORLD_LOADED)
    def on_world_loaded(self, event):
        self.update_texture()
        

class Wire(Electrical):
    """Conductive wire"""

    _TILES = {
        0: "wire"
    }

    CONNECTED = True
    
    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.powered = False
        self.powered_by = []
    
    def update_power(self):
        """Updates power state"""
        if self.powered_by:
            self.powered = True
            self.update_texture()
        else:
            self.powered = False
            self.update_texture()
    
    def update_texture(self):
        self.texture.id = self.neighbors + 16 * int(self.powered)

class InsulatedWire(Wire):
    """Insulated wire"""

    _TILES = {
        0: "insulated_wire"
    }
    
    solid = True

class Gate(Electrical):
    """Logical gate"""
    
    _TILES = {
        0: "gate"
    }