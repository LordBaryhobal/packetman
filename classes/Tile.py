#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Vec import Vec
import pygame

class Tile:
    def __init__(self, x, y, type_):
        self.coo = Vec(x, y)
        self.color = [(255,255,255),(0,0,0),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]
        self.type = type_ # 0 = empty, 1 = ..., 2 = ..., 3 = ...
    
    def render(self, surface, position,size):
        pygame.draw.rect(surface, self.color[self.type], (position.x, position.y, size, size))
    