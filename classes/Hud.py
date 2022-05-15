#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Tile import Tile
from .Vec import Vec
from .Logger import Logger
import pygame

class Hud:
    """Class to display editor hud"""

    MARGIN = 20

    def __init__(self, game):
        self.game = game
        self.slot = 0
        self.hotbar = 0
        self.hotbars = [
            [Tile(type_=1), Tile(type_=2), Tile(type_=3), Tile(type_=4), Tile(type_=5), Tile(type_=7), Tile(type_=8)]
        ]
    
    def get_type(self):
        if self.hotbar < len(self.hotbars) and self.slot < len(self.hotbars[self.hotbar]):
            return self.hotbars[self.hotbar][self.slot].type
        
        return 0

    def render(self, surface):
        WIDTH, HEIGHT = surface.get_width(), surface.get_height()
        hotbar_width = 0.5*WIDTH
        hotbar_height = 0.1*hotbar_width

        ox, oy = WIDTH/2 - hotbar_width/2, HEIGHT-hotbar_height-self.MARGIN
        gap = (hotbar_width-9*hotbar_height)/10
        margin = hotbar_height*0.1

        for i in range(9):
            x, y = ox + gap + i*(hotbar_height+gap), oy
            #color = (200,80,80) if i == self.slot else (150,150,150)
            color = (150,150,150)
            pygame.draw.rect(surface, color, [x, y, hotbar_height, hotbar_height])

            if self.hotbar < len(self.hotbars) and i < len(self.hotbars[self.hotbar]):
                self.hotbars[self.hotbar][i].render(surface, Vec(x+margin, y+hotbar_height-margin), hotbar_height*0.8)
        
        w, h = hotbar_height*0.75, self.MARGIN/4
        pygame.draw.rect(surface, (200,80,80), [ox + gap + self.slot*(hotbar_height+gap) + hotbar_height*0.5 - w/2, HEIGHT-self.MARGIN*0.75, w, h])

        # Thumbs
        world_w = self.game.world.WIDTH*self.game.camera.tilesize
        world_h = self.game.world.HEIGHT*self.game.camera.tilesize

        pos_x, pos_y = self.game.camera.pos.x, self.game.camera.pos.y
        
        rx = pos_x/(world_w - self.game.WIDTH)
        ry = pos_y/(world_h - self.game.HEIGHT)
        rx, ry = max(0, min(1, rx)), max(0, min(1, ry))
        
        x_thumb_w = min(1, self.game.WIDTH/world_w) * self.game.WIDTH
        y_thumb_h = min(1, self.game.HEIGHT/world_h) * self.game.HEIGHT

        x = rx*(self.game.WIDTH-x_thumb_w)
        y = (1-ry)*(self.game.HEIGHT-y_thumb_h)

        pygame.draw.rect(surface, (255,255,255), [x, HEIGHT-5, x_thumb_w,5])
        pygame.draw.rect(surface, (255,255,255), [0, y, 5, y_thumb_h])

    
    def set_hotbar(self, i):
        if i < len(self.hotbars):
            self.hotbar = i
        
        else:
            Logger.warn(f"Tried to set hotbar of index {i} but only {len(self.hotbars)} are defined")