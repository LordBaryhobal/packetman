#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Vec import Vec
import pygame

class Tile:
    def __init__(self, x, y, size, color, type_):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.type = type_ # 0 = empty, 1 = ..., 2 = ..., 3 = ...
    
    def render(self, surface, position):
        pygame.draw.rect(surface, self.color, (position.x, position.y, self.size, self.size))
    