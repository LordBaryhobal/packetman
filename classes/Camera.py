#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Vec import Vec
from math import floor

class Camera:
    """
    Camera class responsible for calculating the position and sizes
    of elements to render on the screen. Calls the render functions
    of tiles and entities.
    """

    def __init__(self,game):
        """Initializes a Camera instance

        Arguments:
            game {Game} -- Game instance
        """

        #camera's coordinates are in the bottom left corner of the screen
        self.pos = Vec(0,0)
        self.game = game
        self.follow_player = True
        self.tilesize = self.game.HEIGHT//10
        self.update_visible_tiles()
        self.update_visible_entities()
    
    def update(self):
        """Updates the position of the camera

        If activated, the camera will follow the player so that it stays in the screen
        """

        if self.follow_player:
            player = self.game.world.player
            player_tl = self.world_to_screen(Vec(player.pos.x, player.pos.y+player.box.h))
            player_br = self.world_to_screen(Vec(player.pos.x+player.box.w, player.pos.y))
            
            W, H = self.game.WIDTH, self.game.HEIGHT
            W4, H4 = W/4, H/4

            if player_tl.x < W4:                # left
                self.pos.x -= W4-player_tl.x
            elif player_br.x > W-W4:            # right
                self.pos.x += player_br.x-W+W4
            
            if player_tl.y < H4:                # bottom
                self.pos.y += H4-player_tl.y
            elif player_br.y > H-H4:            # top
                self.pos.y -= player_br.y-H+H4
            
            self.pos = self.pos.max(Vec(0,0))
        
    def update_visible_tiles(self):
        """Updates the list of visible tiles"""

        self.pos = self.pos.max(Vec()) #clamp to (0;0)
        
        #according to the screen
        bottomright = self.screen_to_world(Vec(self.game.WIDTH,self.game.HEIGHT))
        topleft = self.screen_to_world(Vec(0,0))
        
        self.visible_tiles = self.game.world.get_tiles_in_rect(topleft, bottomright).flatten()
    
    def update_visible_entities(self):
        """Updates the list of visible entities"""

        self.pos = self.pos.max(Vec()) #clamp to (0;0)
        
        #according to the screen
        bottomright = self.screen_to_world(Vec(self.game.WIDTH,self.game.HEIGHT))
        topleft = self.screen_to_world(Vec(0,0))

        self.visible_entities = self.game.world.get_entities_in_rect(topleft, bottomright)

    def render(self, world_surf, hud_surf, editor_surf):
        """Renders the visible tiles and entities

        Arguments:
            world_surf {pygame.Surface} -- surface to render the world on
            hud_surf {pygame.Surface} -- surface to render the hud on
            editor_surf {pygame.Surface} -- surface to render selections on
        """
        
        world_surf.fill((0,0,0))
        for tile in self.visible_tiles:
            tile.render(world_surf, self.world_to_screen(tile.pos),self.tilesize)
        
        for entity in self.visible_entities:
            entity.render(world_surf, self.world_to_screen(entity.pos), self.tilesize)

        if self.game.config["edition"]:
            self.game.editor.render(hud_surf, editor_surf)

    def screen_to_world(self, pos, round_=True):
        """Converts screen to world coordinates

        Arguments:
            pos {Vec} -- screen coordinates

        Returns:
            Vec -- world coordinates
        """
        pos = (Vec(pos.x,self.game.HEIGHT-pos.y) + self.pos)/self.tilesize
        return floor(pos) if round_ else pos

    def world_to_screen(self, pos):
        """Converts world to screen coordinates

        Arguments:
            pos {Vec} -- world coordinates

        Returns:
            Vec -- screen coordinates
        """

        return Vec(pos.x*self.tilesize,self.game.HEIGHT-pos.y*self.tilesize) + Vec(-self.pos.x,self.pos.y)
