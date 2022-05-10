#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from typing import List, Type
import pygame
from Vec import Vec

class Tile:
    def __init__(self, x: int, y: int, size, color: List[int, int, int], type_: int) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.type = type_ # 0 = empty, 1 = ..., 2 = ..., 3 = ...
    
    def render(self, surface: Type[pygame.Surface], position: Type[Vec]) -> None:
        pygame.draw.rect(surface, self.color, (position.x, position.y, self.size, self.size))
    