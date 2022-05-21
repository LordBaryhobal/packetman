#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Component import Component
import pygame

class Label(Component):
    font_family = "Arial"
    fonts = {}
    color = (255,255,255)

    def __init__(self, text="", halign="center", valign="center", font_size=30, name=None):
        """Initializes a Label instance

        Keyword Arguments:
            text {str} -- text content (default: {""})
            halign {str} -- horizontal alignment, one of: "left","center","right" (default: {"center"})
            valign {str} -- vertical alignment, one of: "top","center","bottom" (default: {"center"})
            font_size {int} -- font size (default: {30})
            name {str} -- component's name (default: {None})
        """

        super().__init__(name)
        self.text = text
        self.halign = halign
        self.valign = valign
        
        if not font_size in Label.fonts.keys():
            Label.fonts[font_size] = pygame.font.SysFont(self.font_family, font_size)
        
        self.font = Label.fonts[font_size]
    
    def render(self, surface):
        """Renders the component

        Arguments:
            surface {pygame.Surface} -- surface to render the component on
        """
        
        super().render(surface)

        text = self.font.render(self.text, True, self.color)
        x, y, w, h = self.get_shape()
        X, Y = x, y

        if self.halign == "center":
            X = x+w/2 - text.get_width()/2
        elif self.halign == "right":
            X = x+w-text.get_width()

        if self.valign == "center":
            Y = y+h/2 - text.get_height()/2
        elif self.valign == "bottom":
            Y = y+h-text.get_height()

        surface.blit(text, [X, Y])