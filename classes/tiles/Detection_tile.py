#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Event import Event, listener, on
from classes.Tile import Tile
from classes.Player import Player


@listener
class Detection_tile(Tile):
    """a tile to trigger the end of a level"""
    
    _TILES = {
        0: "detection_tile"
    }
    
    def render(self, surface, hud_surf, pos, size, dimensions=None):
        """Renders the tile

        Arguments:
            surface {pygame.Surface} -- surface to render the tile on
            surface {pygame.Surface} -- surface to render the hud elements on
            pos {Vec} -- pixel coordinates where to render on the surface
            size {int} -- size of a tile in pixels
            dimensions {Vec} -- dimensions of the tile (default: {None})
        """
        if self.world.game.config["edition"]:
            self.texture.render(surface, pos, size)
    
    @on(Event.ENTER_TILE)
    def on_entity_enter(self, event):
        if isinstance(event.entity, Player) and self in event.tiles:
            self.world.game.finish_level()