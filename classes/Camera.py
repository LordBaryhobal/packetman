#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY
from classes.Vec import Vec

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

    def __init__(self,game):
        #camera's coordinates are in the bottom left corner of the screen
        self.coo = Vec(0,0)
        self.game = game
        self.tilesize = self.game.HEIGHT//10
        self.update_visible_tiles()
        self.update_visible_tiles()
        
    def update_visible_tiles(self):
        self.coo = self.coo.max(Vec())
        
        #according to the screen
        bottomright = self.screen_to_world(Vec(self.game.WIDTH,self.game.HEIGHT))
        topleft = self.screen_to_world(Vec(0,0))
        
        self.visible_tiles = self.game.world.get_tiles_in_rect(topleft, bottomright).flatten()

    def render(self, surface):
        """Renders the visible tiles and entities
        @param surface: pygame surface to render on
        """
        for tile in self.visible_tiles:
            tile.render(surface, self.world_to_screen(tile.coo),self.tilesize)

    def screen_to_world(self, pos):
        """Converts screen to world coordinates
        @param pos: Vec to convert
        """
        return (Vec(pos.x,self.game.HEIGHT-pos.y) + self.coo)//self.tilesize

    def world_to_screen(self, pos):
        """Converts world to screen coordinates
        @param pos: Vec to convert
        """
        return Vec(pos.x*self.tilesize,self.game.HEIGHT-(pos.y+1)*self.tilesize) + Vec(-self.coo.x,self.coo.y)
