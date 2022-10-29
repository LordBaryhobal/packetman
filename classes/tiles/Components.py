#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Event import Event, listener, on
from classes.Tile import Tile
from classes.Vec import Vec
from classes.SoundManager import SoundManager
from classes.entities.Triggers import Trigger
from classes.Player import Player
from classes.entities.Drone import Drone
from classes.entities.Hacker import Hacker
from classes.entities.Robot import Robot
from classes.entities.Bullet import Bullet

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
        for i, delta in enumerate((Vec(0, -1), Vec(1, 0), Vec(0, 1), Vec(-1, 0))):
            ntile = self.world.get_tile(self.pos+delta)
            if isinstance(ntile, Electrical):
                neighbors.append((i,ntile))
        if neighbors:
            event = Event(Event.CIRCUIT_CHANGE)
            event.power = pressed
            event.tiles = neighbors
            self.world.game.events.append(event)

class Output(Electrical):
    """Output component which does stuff when powered"""

    _TILES = {
        0: "output"
    }
    
    def create_event(self, pressed):
        neighbors = []
        if self.world:
            tile = self.world.get_tile(self.pos+self.DIRECTION[self.rotation])
            if isinstance(tile, Electrical):
                neighbors.append((self.rotation, tile))
            if neighbors:
                event = Event(Event.CIRCUIT_CHANGE)
                event.power = pressed
                event.tiles = neighbors
                self.world.game.events.append(event)

@listener
class Plate(Input):
    """Pressure plate"""

    _TILES = {
        0: "plate"
    }
    I18N_KEY = "plate"
    
    ACTIVATED_BY = (Player, Drone, Hacker, Robot)
    
    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.pressed = False
        self.entity_count = 0
    
    @on(Event.ENTER_TILE)
    def on_enter(self, event):
        if self in event.tiles:
            if isinstance(event.entity, self.ACTIVATED_BY):
                if self.entity_count == 0:
                    self.change_pressed(True)
                self.entity_count += 1
    
    @on(Event.EXIT_TILE)
    def on_exit(self, event):
        if self in event.tiles:
            if isinstance(event.entity, self.ACTIVATED_BY):
                self.entity_count -= 1
                if self.entity_count == 0:
                    self.change_pressed(False)
    
    def change_pressed(self, pressed):
        """Updates pressed state

        Arguments:
            pressed {bool} -- new pressed state
        """
        SoundManager.play("tile.plate.toggle")
        self.create_event(pressed=pressed)
        self.pressed = pressed
        self.texture.id = int(self.pressed)
    
@listener
class Button(Input):
    """Togglable button"""

    _TILES = {
        0: "button"
    }
    I18N_KEY = "button"

    interactive = True
    rotatable = True
    
    _save = ["neighbors", "rotation", "pressed"]
    
    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.pressed = False
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
            SoundManager.play("tile.button.toggle")
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
        if self.pressed:
            self.create_event(pressed=self.pressed)
        

class Wire(Electrical):
    """Conductive wire"""

    _TILES = {
        0: "wire"
    }
    I18N_KEY = "wire"

    CONNECTED = True
    
    def __init__(self, x=0, y=0, type_=0, world=None):
        self.powered = False
        self.powered_by = 0
        super().__init__(x, y, type_, world)
    
    def update_power(self):
        """Updates power state"""
        self.powered_by = max(self.powered_by, 0)  # can be a problem
        if self.powered_by > 0:
            self.powered = True
        else:
            self.powered = False
        self.update_texture()
    
    def update_texture(self):
        self.texture.id = self.neighbors + 16 * int(self.powered)
    
    def reset_power(self):
        self.powered_by = 0
        self.powered = False
        self.update_texture()
        

class InsulatedWire(Wire):
    """Insulated wire"""

    _TILES = {
        0: "insulated_wire"
    }
    I18N_KEY = "insulated_wire"
    
    solid = True

@listener
class Gate(Output, Input):
    """Logical gate"""
    
    _TILES = {
        0: "gate"
    }

    DIRECTION = (Vec(0, -1), Vec(1, 0), Vec(0, 1), Vec(-1, 0))

    solid = True
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
        self.update_texture()
    
    def update_texture(self):
        self.texture.id = self.rotation + 4*int(self.powered)
    
    @on(Event.GATE_INPUT)
    def update_input(self, event):
        if event.tile == self:
            for i, d in enumerate(self.input_direction):
                if (self.rotation + d)%4 == event.connected_from:
                    if event.power:
                        self.powered_by[i] += 1
                    else:
                        self.powered_by[i] -= 1
                    self.update_activation()
    @on(Event.WORLD_LOADED)
    def on_world_loaded(self, event):
        if self.rotatable:
            self.update_texture()

class BufferGate(Gate):
    """BufferGate let the power flow only in one direction"""

    _TILES = {
        0: "buffer_gate"
    }
    I18N_KEY = "buffer_gate"

    rotatable = True

    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.rotation = 0
        self.powered_by = [0]
        self.powered = False
        #according to the rotation
        self.input_direction = (2,)
    
    def update_activation(self):
        """Updates activation state"""
        self.powered_by = [max(self.powered_by[0], 0)]  # can be a problem
        if self.powered_by[0] > 0:
            new_powered = True
        else:
            new_powered = False
        if self.powered != new_powered:
            self.powered = new_powered
            self.create_event(pressed=self.powered)

            self.update_texture()
    
    def reset_power(self):
        self.powered_by = [0]
        self.powered = False
        self.update_texture()

@listener
class NotGate(Gate):
    """NotGate let the power flow only in one direction"""

    _TILES = {
        0: "not_gate"
    }
    I18N_KEY = "not_gate"

    rotatable = True

    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.rotation = 0
        self.powered_by = [0]
        self.powered = False
        #according to the rotation
        self.input_direction = (2,)
    
    def update_activation(self):
        """Updates activation state"""
        self.powered_by = [max(self.powered_by[0], 0)]  # can be a problem
        if self.powered_by[0] > 0:
            new_powered = False
        else:
            new_powered = True
        if self.powered != new_powered:
            self.powered = new_powered
            self.create_event(pressed=self.powered)

            self.update_texture()
    
    @on(Event.WORLD_LOADED)
    def on_world_loaded(self, event):
        self.update_texture()
        self.update_activation()
    
    def reset_power(self):
        self.powered_by = [0]
        self.powered = False
        self.update_texture()

class AndGate(Gate):
    """AndGate let the power flow only in one direction"""

    _TILES = {
        0: "and_gate"
    }
    I18N_KEY = "and_gate"

    rotatable = True

    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.rotation = 0
        self.powered_by = [0,0]
        self.powered = False
        #according to the rotation
        self.input_direction = (1,3)
    
    def update_activation(self):
        """Updates activation state"""
        self.powered_by = [max(self.powered_by[0], 0),max(self.powered_by[1], 0)]  # can be a problem
        if self.powered_by[0] > 0 and self.powered_by[1] > 0:
            new_powered = True
        else:
            new_powered = False
        if self.powered != new_powered:
            self.powered = new_powered
            self.create_event(pressed=self.powered)

            self.update_texture()
    
    def reset_power(self):
        self.powered_by = [0,0]
        self.powered = False
        self.update_texture()

class OrGate(Gate):
    """OrGate let the power flow only in one direction"""

    _TILES = {
        0: "or_gate"
    }
    I18N_KEY = "or_gate"

    rotatable = True

    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.rotation = 0
        self.powered_by = [0,0]
        self.powered = False
        #according to the rotation
        self.input_direction = (1,3)
    
    def update_activation(self):
        """Updates activation state"""
        self.powered_by = [max(self.powered_by[0], 0),max(self.powered_by[1], 0)]  # can be a problem
        if self.powered_by[0] > 0 or self.powered_by[1] > 0:
            new_powered = True
        else:
            new_powered = False
        if self.powered != new_powered:
            self.powered = new_powered
            self.create_event(pressed=self.powered)

            self.update_texture()
    
    def reset_power(self):
        self.powered_by = [0,0]
        self.powered = False
        self.update_texture()

@listener
class PuzzleDoor(Wire):
    """PuzzleDoor"""

    _TILES = {
        0: "puzzle_door"
    }
    I18N_KEY = "puzzle_door"

    solid = True

    CONNECTED = True

    def update_power(self):
        """Updates power state"""
        self.powered_by = max(self.powered_by, 0)  # can be a problem
        if self.powered_by > 0:
            self.powered = True
            self.solid = False
            self.update_texture()
        else:
            if self.powered == True:
                self.kill_entities()
            self.powered = False
            self.solid = True
            self.update_texture()
    
    def kill_entities(self):
        """Kills entities inside the door"""
        if self.world.game.config["edition"]:
            return
        tl, br = self.pos.get_tl_br_corners(self.pos + Vec(1, 1))
        entities = self.world.get_entities_in_rect(tl, br)
        entities_to_kill = filter(lambda e: not isinstance(e, Trigger), entities)
        for e in entities_to_kill:
            e.die()
            if isinstance(e, Player):
                break
        
PuzzleDoor.CONNECT_TO = (PuzzleDoor, )


class CrossWire(Electrical):
    _TILES = {
        0: "crosswire2"
    }
    DIRECTION = (Vec(0, -1), Vec(1, 0), Vec(0, 1), Vec(-1, 0))
    
    I18N_KEY = "crosswire"

    CONNECTED = True
    
    def __init__(self, x=0, y=0, type_=0, world=None):
        self.powered = [False, False]
        self.powered_by = [0,0]
        super().__init__(x, y, type_, world)
    
    def update_power(self):
        """Updates power state"""
        if self.powered_by[0] > 0:
            self.powered[0] = True
        else:
            self.powered[0] = False
        
        if self.powered_by[1] > 0:
            self.powered[1] = True
        else:
            self.powered[1] = False
        self.update_texture()
    
    def update_texture(self):
        self.texture.id = self.neighbors + 16 * (int(self.powered[0]) + 2 * int(self.powered[1]))
    
    def reset_power(self):
        self.powered_by = [0,0]
        self.powered = [False, False]
        self.update_texture()

@listener
class Target(Input):
    
    _TILES = {
        0: "target"
    }
    I18N_KEY = "target"

    solid = True
    
    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.pressed = False
    
    @on(Event.COLLISION_WORLD)
    def on_collision_world(self, event):
        if self in event.tiles:
            if isinstance(event.entity, Bullet):
                self.toggle_power()
    
    def toggle_power(self):
        self.pressed = not self.pressed
        self.create_event(pressed=self.pressed)
        self.update_texture()
    
    def update_texture(self):
        self.texture.id = int(self.pressed)