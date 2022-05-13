#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY
from .Vec import Vec

#TODO: fix circular import
try:
    from .Game import Game
except ImportError:
    pass

class Camera:
    """
    Camera class responsible for calculating the position and sizes
    of elements to render on the screen. Calls the render functions
    of tiles and entities.
    """

    def __init__(self):
        #camera's coordinates are in the bottom left corner of the screen
        self.coo = Vec()
        self.game = Game.instance
        self.tilesize = self.game.HEIGHT//10
        
    def uptade_visible_tiles(self):
        bottomright = self.screen_to_world(self.coo+Vec(0,self.coo.y))
        topleft = self.screen_to_world(self.coo+Vec(self.game.WIDTH,0))
        self.visible_tiles = self.game.world.get_tiles_in_rect(topleft, bottomright).flatten()

    def render(self, surface):
        """Renders the visible tiles and entities
        @param surface: pygame surface to render on
        """
        for tile in self.visible_tiles:
            tile.render(surface, self.world_to_screen(tile.coo))

    def screen_to_world(self, pos):
        """Converts screen to world coordinates
        @param pos: Vec to convert
        """
        return (Vec(self.game.HEIGHT,self.game.WIDTH)-pos+self.coo)//self.tilesize

    def world_to_screen(self, pos):
        """Converts world to screen coordinates
        @param pos: Vec to convert
        """
        return Vec(self.game.HEIGHT,self.game.WIDTH)+self.coo-(pos*self.tilesize)
