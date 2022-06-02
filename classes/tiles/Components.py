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
        self.powered_by = [] # optimizable ( change to a number instead of list of tiles)
    
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

class Gate(Output, Input):
    """Logical gate"""
    
    _TILES = {
        0: "gate"
    }

    DIRECTION = (Vec(0, 1), Vec(1, 0), Vec(0, -1), Vec(-1, 0))

    def create_event(self, pressed):
        neighbors = []
        tile = self.world.get_tile(self.pos+self.DIRECTION[self.rotation])
        if isinstance(tile, Electrical):
            neighbors.append((self.rotation, tile))
        if neighbors:
            event = Event(Event.CIRCUIT_CHANGE)
            event.power = pressed
            event.input = self
            event.tiles = neighbors
            self.world.game.events.append(event)
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
        self.update_texture()
    
    @on(Event.WORLD_LOADED)
    def on_world_loaded(self, event):
        self.update_texture()
    
    def update_texture(self):
        self.texture.id = self.rotation + 4*int(self.powered)
    
    @on(Event.GATE_INPUT)
    def update_input(self, event):
        if event.tile == self:
            for i, d in enumerate(self.input_direction):
                if (self.rotation + d)%4 == event.connected_from:
                    if event.power:
                        self.powered_by[i].append(event.input)
                    else:
                        self.powered_by[i].remove(event.input)
                    self.update_activation()

@listener
class Buffer_Gate(Gate):
    """Buffer_Gate let the power flow only in one direction"""

    _TILES = {
        0: "test_gate"
    }

    rotatable = True

    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.rotation = 0
        self.powered_by = [[]]
        self.powered = False
        #according to the rotation
        self.input_direction = (2,)
    
    def update_activation(self):
        """Updates activation state"""
        if self.powered_by[0]:
            new_powered = True
        else:
            new_powered = False
        if self.powered != new_powered:
            self.powered = new_powered
            self.create_event(pressed=self.powered)

            self.update_texture()

@listener
class NotGate(Gate):
    """NotGate let the power flow only in one direction"""

    _TILES = {
        0: "not_gate"
    }

    rotatable = True

    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.rotation = 0
        self.powered_by = [[]]
        self.powered = False
        #according to the rotation
        self.input_direction = (2,)
    
    def update_activation(self):
        """Updates activation state"""
        if self.powered_by[0]:
            new_powered = False
        else:
            new_powered = True
        if self.powered != new_powered:
            self.powered = new_powered
            self.create_event(pressed=self.powered)

            self.update_texture()

@listener
class AndGate(Gate):
    """AndGate let the power flow only in one direction"""

    _TILES = {
        0: "and_gate"
    }

    rotatable = True

    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.rotation = 0
        self.powered_by = [[],[]]
        self.powered = False
        #according to the rotation
        self.input_direction = (1,3)
    
    def update_activation(self):
        """Updates activation state"""
        if self.powered_by[0] and self.powered_by[1]:
            new_powered = True
        else:
            new_powered = False
        if self.powered != new_powered:
            self.powered = new_powered
            self.create_event(pressed=self.powered)

            self.update_texture()

@listener
class OrGate(Gate):
    """OrGate let the power flow only in one direction"""

    _TILES = {
        0: "or_gate"
    }

    rotatable = True

    def __init__(self, x=0, y=0, type_=0, world=None):
        super().__init__(x, y, type_, world)
        self.rotation = 0
        self.powered_by = [[],[]]
        self.powered = False
        #according to the rotation
        self.input_direction = (1,3)
    
    def update_activation(self):
        """Updates activation state"""
        if self.powered_by[0] or self.powered_by[1]:
            new_powered = True
        else:
            new_powered = False
        if self.powered != new_powered:
            self.powered = new_powered
            self.create_event(pressed=self.powered)

            self.update_texture()
