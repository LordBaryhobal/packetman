#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Tile import Tile
from classes.Event import listener, on, Event

class Electrical(Tile):
    pass

class Input(Electrical):
    _tiles = {
        0: "input"
    }

class Output(Electrical):
    _tiles = {
        0: "output"
    }

class Plate(Input):
    _tiles = {
        0: "plate"
    }

@listener
class Button(Input):
    _tiles = {
        0: "button"
    }
    INTERACTIVE = True

    pressed = False
    rotatable = True

    @on(Event.INTERACTION)
    def on_interact(self, event):
        if self in event.tiles:
            if self.pressed:
                self.set_pressed(False)
            else:
                self.set_pressed(True)
    
    def set_pressed(self, pressed=True):
        self.pressed = pressed
        self.texture.id = int(self.pressed) << 2

class Wire(Electrical):
    _tiles = {
        0: "wire"
    }
    connected = True
    connect_strict = True

class Gate(Electrical):
    _tiles = {
        0: "gate"
    }