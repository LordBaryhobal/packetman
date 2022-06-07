#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Tile import Tile

class DetectionTile(Tile):
    """Tile which triggers the end of a level"""
    
    _TILES = {
        0: "detection_tile"
    }
    I18N_KEY = "detection_tile"
    
    def render(self, surface, hud_surf, pos, size, dimensions=None):
        if self.world.game.config["edition"]:
            super().render(surface, hud_surf, pos, size, dimensions)