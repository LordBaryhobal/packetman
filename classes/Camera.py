#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Vec import Vec

class Camera:
    """
    Camera class responsible for calculating the position and sizes
    of elements to render on the screen. Calls the render functions
    of tiles and entities.
    """

    def __init__(self,game):
        #camera's coordinates are in the bottom left corner of the screen
        self.pos = Vec(0,0)
        self.game = game
        self.tilesize = self.game.HEIGHT//10
        self.update_visible_tiles()
        self.update_visible_entities()
        
    def update_visible_tiles(self):
        self.pos = self.pos.max(Vec()) #clamp to (0;0)
        
        #according to the screen
        bottomright = self.screen_to_world(Vec(self.game.WIDTH,self.game.HEIGHT))
        topleft = self.screen_to_world(Vec(0,0))
        
        self.visible_tiles = self.game.world.get_tiles_in_rect(topleft, bottomright).flatten()
    
    def update_visible_entities(self):
        self.pos = self.pos.max(Vec()) #clamp to (0;0)
        
        #according to the screen
        bottomright = self.screen_to_world(Vec(self.game.WIDTH,self.game.HEIGHT))
        topleft = self.screen_to_world(Vec(0,0))

        self.visible_entities = self.game.world.get_entities_in_rect(topleft, bottomright)

    def render(self, world_surf, hud_surf, editor_surf):
        """Renders the visible tiles and entities
        @param surface: pygame surface to render on
        """
        world_surf.fill((0,0,0))
        for tile in self.visible_tiles:
            tile.render(world_surf, self.world_to_screen(tile.pos),self.tilesize)
        
        for entity in self.visible_entities:
            entity.render(world_surf, self.world_to_screen(entity.pos), self.tilesize)

        if self.game.config["edition"]:
            self.game.editor.render(hud_surf, editor_surf)

    def screen_to_world(self, pos):
        """Converts screen to world coordinates
        @param pos: Vec to convert
        """
        return (Vec(pos.x,self.game.HEIGHT-pos.y) + self.pos)//self.tilesize

    def world_to_screen(self, pos):
        """Converts world to screen coordinates
        @param pos: Vec to convert
        """
        return Vec(pos.x*self.tilesize,self.game.HEIGHT-pos.y*self.tilesize) + Vec(-self.pos.x,self.pos.y)
