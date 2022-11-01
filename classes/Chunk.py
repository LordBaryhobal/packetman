#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import numpy as np

class Chunk:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tiles = np.full((16, 16), None, dtype="object")
        self.ground_tiles = np.full((16, 16), None, dtype="object")
    
    def set_tile(self, tile, pos, ground=False):
        if ground:
            self.ground_tiles[pos.x, pos.y] = tile
        else:
            self.tiles[pos.x, pos.y] = tile
    
    def get_tile(self, pos, ground=False):
        if ground:
            return self.ground_tiles[pos.y, pos.x]
        
        return self.tiles[pos.y, pos.x]
    
    def get_tile_in_rect(self, tl, br, ground=False):
        if ground:
            return self.ground_tiles[br.y:tl.y+1, tl.x:br.x+1]
        
        return self.tiles[br.y:tl.y+1, tl.x:br.x+1]
