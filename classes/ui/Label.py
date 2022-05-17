#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Component import Component
import pygame

class Label(Component):
    font_family = "Arial"
    fonts = {}
    color = (255,255,255)

    def __init__(self, x, y, w, h, text="", halign="center", valign="center", font_size=30):
        super().__init__(x, y, w, h)
        self.text = text
        self.halign = halign
        self.valign = valign
        
        if not font_size in Label.fonts.keys():
            Label.fonts[font_size] = pygame.font.SysFont(self.font_family, font_size)
        
        self.font = Label.fonts[font_size]
    
    def render(self, surface, x, y, w, h):
        super().render(surface, x, y, w, h)

        text = self.font.render(self.text, True, self.color)
        X, Y = x,y

        if self.halign == "center":
            X = x+w/2 - text.get_width()/2
        elif self.halign == "right":
            X = x+w-text.get_width()

        if self.valign == "center":
            Y = y+h/2 - text.get_height()/2
        elif self.valign == "bottom":
            Y = y+h-text.get_height()

        surface.blit(text, [X,Y])