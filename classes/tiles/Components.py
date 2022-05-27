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

@listener
class Plate(Input):
    _tiles = {
        0: "plate"
    }
    
    def __init__(self, x=0, y=0, type_=0):
        super().__init__(x, y, type_)
        self.pressed = False
        self.number_of_entities = 0
    
    @on(Event.ENTER_TILE)
    def on_enter(self, event):
        if self in event.tiles:
            if self.number_of_entities == 0:
                self.change_pressed(True)
            self.number_of_entities += 1
    
    @on(Event.EXIT_TILE)
    def on_exit(self, event):
        if self in event.tiles:
            self.number_of_entities -= 1
            if self.number_of_entities == 0:
                self.change_pressed(False)
    
    def change_pressed(self, pressed):
        self.pressed = pressed
        self.texture.id = int(self.pressed)
    
@listener
class Button(Input):
    _tiles = {
        0: "button"
    }
    INTERACTIVE = True

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
        self.pressed = pressed
        self.update_texture()
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
        self.update_texture()
    
    def update_texture(self):
        self.texture.id = (int(self.pressed) << 2) + self.rotation
        

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