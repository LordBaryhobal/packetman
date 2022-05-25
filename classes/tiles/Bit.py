#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Texture import Texture
from classes.Tile import Tile

class Bit(Tile):
    solid = True
    
    _tiles = {
        0: "bit"
    }

    def __init__(self, x=0, y=0, type_=0):
        super().__init__(x, y, type_)
        self.value = 0
    
    def on_update(self):
        self.texture.id = self.value