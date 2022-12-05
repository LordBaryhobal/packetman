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
            self.ground_tiles[pos.y, pos.x] = tile
        else:
            self.tiles[pos.y, pos.x] = tile
    
    def get_tile(self, pos, ground=False):
        if ground:
            return self.ground_tiles[pos.y, pos.x]
        
        return self.tiles[pos.y, pos.x]
    
    def get_tiles_in_rect(self, tl, br, ground=False):
        if ground:
            return self.ground_tiles[tl.y:br.y, tl.x:br.x]
        
        return self.tiles[tl.y:br.y, tl.x:br.x]

    def is_empty(self):
        return np.all(self.ground_tiles == None) and np.all(self.tiles == None)
