#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from math import floor

from classes.Vec import Vec

class Camera:
    """
    Camera class responsible for calculating the position and sizes
    of elements to render on the screen. Calls the render functions
    of tiles and entities.
    """

    def __init__(self, game):
        """Initializes a Camera instance

        Arguments:
            game {Game} -- Game instance
        """

        # Coordinates are in pixels from the bottom-left corner of the screen
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
            hm, vm = W/3, H/3

            prev_pos = self.pos.copy()

            if player_tl.x < hm:                # left
                self.pos.x -= hm-player_tl.x
            elif player_br.x > W-hm:            # right
                self.pos.x += player_br.x-W+hm
            
            if player_tl.y < vm:                # bottom
                self.pos.y += vm-player_tl.y
            elif player_br.y > H-vm:            # top
                self.pos.y -= player_br.y-H+vm
            
            self.pos = self.pos.max(Vec(0,0))
            
            if prev_pos != self.pos:
                self.update_visible_tiles()
                self.update_visible_entities()
        
    def update_visible_tiles(self):
        """Updates the list of visible tiles"""

        self.pos = self.pos.max(Vec())  # clamp to (0;0)
        
        # According to the screen
        bottomright = self.screen_to_world(Vec(self.game.WIDTH, self.game.HEIGHT))
        topleft = self.screen_to_world(Vec())
        
        self.visible_tiles = self.game.world.get_tiles_in_rect(topleft, bottomright).flatten()
    
    def update_visible_entities(self):
        """Updates the list of visible entities"""

        self.pos = self.pos.max(Vec())  # clamp to (0;0)
        
        # According to the screen
        bottomright = self.screen_to_world(Vec(self.game.WIDTH, self.game.HEIGHT))
        topleft = self.screen_to_world(Vec())

        self.visible_entities = self.game.world.get_entities_in_rect(topleft, bottomright)

    def render(self, world_surf, hud_surf, editor_surf):
        """Renders the visible tiles and entities

        Arguments:
            world_surf {pygame.Surface} -- surface to render the world on
            hud_surf {pygame.Surface} -- surface to render the hud on
            editor_surf {pygame.Surface} -- surface to render selections on
        """
        
        world_surf.fill((40,40,40))
        for tile in self.visible_tiles:
            tile.render(world_surf, self.world_to_screen(tile.pos), self.tilesize)
        
        for entity in self.visible_entities:
            entity.render(world_surf, self.world_to_screen(entity.pos), self.tilesize)

        if self.game.config["edition"]:
            self.game.editor.render(hud_surf, editor_surf)

    def screen_to_world(self, pos, round_=True):
        """Converts screen to world coordinates

        Arguments:
            pos {Vec} -- screen coordinates
        
        Keyword Arguments:
            round_ {bool} -- wether to floor the resulting coordinates (i.e. tile coordinates) (default: {True})

        Returns:
            Vec -- world coordinates
        """

        pos = (Vec(pos.x, self.game.HEIGHT-pos.y) + self.pos)/self.tilesize
        return floor(pos) if round_ else pos

    def world_to_screen(self, pos):
        """Converts world to screen coordinates

        Arguments:
            pos {Vec} -- world coordinates

        Returns:
            Vec -- screen coordinates
        """

        return Vec(
            pos.x*self.tilesize - self.pos.x,
            self.game.HEIGHT - pos.y*self.tilesize + self.pos.y
        )