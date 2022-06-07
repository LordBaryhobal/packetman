#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

from classes.I18n import i18n
from classes.ui.Component import Component

class Input(Component):
    """Input field"""

    FONTS = {}
    VALID = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"

    font_family = "Arial"
    border_color = (255,255,255)
    border_focus_color = (80,140,227)
    color = (255,255,255)
    placeholder_color = (175,175,175)

    def __init__(self, default="", placeholder="", font_size=20, name=None):
        """Initializes an Input instance

        Keyword Arguments:
            default {str} -- default value (default: {""})
            placeholder {str} -- placeholder value displayed when empty (default: {""})
            font_size {int} -- font size (default: {30})
            name {str} -- component's name (default: {None})
        """

        super().__init__(name)
        self.value = default
        self.placeholder = placeholder
        self.focused = False
        
        if not font_size in Input.FONTS.keys():
            Input.FONTS[font_size] = pygame.font.SysFont(self.font_family, font_size)
        
        self.font = Input.FONTS[font_size]
    
    def render(self, surface):
        super().render(surface)
        
        if self.value:
            text = self.font.render(self.value, True, self.color)
        else:
            text = self.font.render(i18n(self.placeholder), True, self.placeholder_color)
        
        x, y, w, h = self.get_shape()
        X, Y = x+10, y+h/2 - text.get_height()/2

        surface.blit(text, [X, Y])
        if self.focused and self.value:
            start = [X+text.get_width(), Y]
            end = [X+text.get_width(), Y+text.get_height()]
            pygame.draw.line(surface, self.color, start, end)
        pygame.draw.rect(surface, self.border_focus_color if self.focused else self.border_color, [x,y,w,h], 1)
    
    def get_value(self):
        return self.value

    def set_value(self, value):
        if self.value != value:
            self.value = value
            self.set_changed(1)

    def on_click(self, event):
        self.focused = True
        self.set_changed(1)
        return True
    
    def on_key_down(self, event):
        if self.focused:
            if event.key == pygame.K_ESCAPE:
                self.focused = False
                self.set_changed(1)
                return True
            
            elif event.key == pygame.K_BACKSPACE:
                self.set_value(self.value[:-1])
                return True
            
            elif event.unicode in self.VALID:
                self.set_value(self.value + event.unicode)
                return True
                
        return False