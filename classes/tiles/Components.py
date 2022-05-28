#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Event import Event, listener, on
from classes.Tile import Tile

class Electrical(Tile):
    """Electrical component"""
    pass

class Input(Electrical):
    """Input component which can produce electricity"""

    _TILES = {
        0: "input"
    }

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
    
    def __init__(self, x=0, y=0, type_=0):
        super().__init__(x, y, type_)
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
    
    def __init__(self, x=0, y=0, type_=0):
        super().__init__(x, y, type_)
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
    CONNECT_STRICT = True

class Gate(Electrical):
    """Logical gate"""
    
    _TILES = {
        0: "gate"
    }