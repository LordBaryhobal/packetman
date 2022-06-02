#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Copyable import Copyable
from classes.Texture import Texture
from classes.Utility import import_class
from classes.Vec import Vec

TILES = {
    "Aluminium": "classes.tiles.Metals",
    "Brass": "classes.tiles.Metals",
    "Buffer_Gate": "classes.tiles.Components",
    "Button": "classes.tiles.Components",
    "Copper": "classes.tiles.Metals",
    "Gate": "classes.tiles.Components",
    "Gold": "classes.tiles.Metals",
    "Insulator": "classes.tiles.Terrain",
    "InsulatedWire": "classes.tiles.Components",
    "Iron": "classes.tiles.Metals",
    "Lead": "classes.tiles.Metals",
    "OrGate": "classes.tiles.Components",
    "Plastic": "classes.tiles.Terrain",
    "Plate": "classes.tiles.Components",
    "PuzzleDoor": "classes.tiles.Components",
    "ThermalConductor": "classes.tiles.Terrain",
    "Wire": "classes.tiles.Components",
    "Zinc": "classes.tiles.Metals"
}

class Tile(Copyable):
    """World tile, can be solid, interactive, etc."""

    _no_save = ["type", "pos", "texture", "world"]
    _TILES = {
        -1: None,
        0: None
    }
    CONNECTED = False
    CONNECT_TO = None

    interactive = False
    solid = False
    rotatable = False

    def __init__(self, x=0, y=0, type_=0, world=None):
        """Initializes a Tile instance

        Keyword Arguments:
            x {int} -- x coordinate (default: {0})
            y {int} -- y coordinate (default: {0})
            type_ {int} -- tile type, 0 if empty (default: {0})
            world {World} -- world the tile is in (default: {None})
        """

        self.pos = Vec(x, y)
        self.type = type_
        self.name = self._TILES[self.type]
        self.texture = Texture(self.name, self.type) if self.name else None
        self.neighbors = 0
        self.world = world
    
    def __setattr__(self, name, value):
        if self.CONNECTED and name == "neighbors" and self.texture:
            self.texture.id = value
        
        super().__setattr__(name, value)
    
    def get_cls(cls):
        """Get class from class name

        Arguments:
            cls {str} -- class name

        Returns:
            class -- corresponding class
        """
        
        return import_class(TILES, cls)
    
    def render(self, surface, pos, size, dimensions=None):
        """Renders the tile

        Arguments:
            surface {pygame.Surface} -- surface to render the tile on
            pos {Vec} -- pixel coordinates where to render on the surface
            size {int} -- size of a tile in pixels
            dimensions {Vec} -- dimensions of the tile (default: {None})
        """
        
        if self.texture:
            self.texture.render(surface, pos, size)
    
    def __repr__(self):
        return f"<{self.__class__.__name__} Tile of type {self.type} at ({self.pos.x}, {self.pos.y})>"
    
    def on_update(self):
        pass