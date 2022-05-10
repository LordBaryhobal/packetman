import pygame

class Tile:
    def __init__(self, x, y, size, color,type):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.type = type # 0 = empty, 1 = ..., 2 = ..., 3 = ...
    def render(self, surface, position):
        pygame.draw.rect(surface, self.color, (position.x, position.y, self.size, self.size))
    