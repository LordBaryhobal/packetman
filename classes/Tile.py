#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

from classes.Copyable import Copyable
from classes.Texture import Texture
from classes.Utility import import_class
from classes.Vec import Vec

TILES = {
    "Aluminium": "classes.tiles.Metals",
    "AndGate": "classes.tiles.Components",
    "Brass": "classes.tiles.Metals",
    "Bridge": "classes.tiles.Components",
    "BufferGate": "classes.tiles.Components",
    "Button": "classes.tiles.Components",
    "Copper": "classes.tiles.Metals",
    "DetectionTile": "classes.tiles.DetectionTile",
    "DroneSpawner": "classes.tiles.Terrain",
    "Gold": "classes.tiles.Metals",
    "Insulator": "classes.tiles.Terrain",
    "InsulatedWire": "classes.tiles.Components",
    "Iron": "classes.tiles.Metals",
    "Lead": "classes.tiles.Metals",
    "NotGate": "classes.tiles.Components",
    "OrGate": "classes.tiles.Components",
    "Plastic": "classes.tiles.Terrain",
    "Plate": "classes.tiles.Components",
    "PuzzleDoor": "classes.tiles.Components",
    "Spike": "classes.tiles.Terrain",
    "ThermalConductor": "classes.tiles.Terrain",
    "Wire": "classes.tiles.Components",
    "Zinc": "classes.tiles.Metals"
}

class Tile(Copyable):
    """World tile, can be solid, interactive, etc."""

    _save = ["neighbors", "rotation"]
    
    _TILES = {
        -1: None,
        0: None
    }
    I18N_KEY = ""

    CONNECTED = False
    CONNECT_TO = None
    HINT_SIZE = Vec(0.5, 0.5)
    HINT_TEXTURE = None

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
        
        if self.CONNECTED:
            self.neighbors = 0
        
        self.world = world
        self.interact_hint = False

        if Tile.HINT_TEXTURE is None:
            Tile.HINT_TEXTURE = Texture("interaction_hint", width=64, height=64)
    
    def __del__(self, *args, **kwargs):
        pass
    
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if self.CONNECTED and name == "neighbors" and self.texture:
            self.update_texture()
        
    
    def get_cls(cls):
        """Get class from class name

        Arguments:
            cls {str} -- class name

        Returns:
            class -- corresponding class
        """
        
        return import_class(TILES, cls)
    
    def render(self, surface, hud_surf, pos, size, dimensions=None):
        """Renders the tile

        Arguments:
            surface {pygame.Surface} -- surface to render the tile on
            surface {pygame.Surface} -- surface to render the hud elements on
            pos {Vec} -- pixel coordinates where to render on the surface
            size {int} -- size of a tile in pixels
            dimensions {Vec} -- dimensions of the tile (default: {None})
        """
        
        if self.texture:
            self.texture.render(surface, pos, size)
        
        if self.interact_hint:
            if self.rotatable:
                offset = [(0, -1), (1, 0), (0, 1), (-1, 0)][self.rotation]
                hintpos = pos + Vec(0.5 + offset[0]*0.5, -0.5 + offset[1]*0.5)*size

                hintpos -= Vec(
                    self.HINT_SIZE.x*size*(0.5 - offset[0]*0.5),
                    self.HINT_SIZE.y*size*(-0.5 - offset[1]*0.5)
                )
            
            else:
                hintpos = pos + Vec(0.5 - self.HINT_SIZE.x*0.5, self.HINT_SIZE.y)*size

            self.HINT_TEXTURE.render(hud_surf, hintpos, size, self.HINT_SIZE)
            self.interact_hint = False
        """if hasattr(self, "powered") and self.powered:
            pygame.draw.rect(hud_surf, (255, 0, 0), (pos.x, pos.y-size, size, size))"""
    
    def __repr__(self):
        return f"<{self.__class__.__name__} Tile of type {self.type} at ({self.pos.x}, {self.pos.y})>"
    
    def on_update(self):
        pass
    
    def update_texture(self):
        self.texture.id = self.neighbors
    
    def get_i18n_key(self):
        if self.name:
            return "tile."+self.__class__.I18N_KEY
        
        return ""