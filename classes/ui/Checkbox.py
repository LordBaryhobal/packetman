#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

from classes.Logger import Logger
from classes.ui.Label import Label

class Checkbox(Label):
    """Togglable checkbox"""

    def __init__(self, text="", callback=lambda *args, **kwargs: None, args=(), halign="center", valign="center", font_size=30, name=None):
        """Initializes a Checkbox instance

        A checkbox can display a label and call a callback when toggled (see `on_release`)

        Keyword Arguments:
            text {str} -- checkbox label (default: {""})
            callback {function} -- function to be called when the button is pressed (default: {nop})
            args {tuple} -- arguments to pass to callback (default: {()})
            halign {str} -- horizontal label alignment, one of: "left", "center", "right" (default: {"center"})
            valign {str} -- vertical label alignment, one of: "top", "center", "bottom" (default: {"center"})
            font_size {int} -- label font size (default: {30})
            name {str} -- component name (default: {None})
        """
        
        super().__init__(text, halign, valign, font_size, name)
        self.callback = callback
        self.args = args
        self.checked = False
    
    def render(self, surface):
        x, y, w, h = self.get_shape()
        h12 = h/12
        
        # Path to draw the X
        pts = [
            (x+3*h12, y+2*h12),
            (x+6*h12, y+5*h12),
            (x+9*h12, y+2*h12),
            (x+10*h12, y+3*h12),
            (x+7*h12, y+6*h12),
            (x+10*h12, y+9*h12),
            (x+9*h12, y+10*h12),
            (x+6*h12, y+7*h12),
            (x+3*h12, y+10*h12),
            (x+2*h12, y+9*h12),
            (x+5*h12, y+6*h12),
            (x+2*h12, y+3*h12)
        ]

        pygame.draw.rect(surface, (100,100,100), [x, y, h, h])
        pygame.draw.rect(surface, (200,200,200), [x+h*0.1, y+h*0.1, h*0.8, h*0.8])

        if self.checked:
            pygame.draw.polygon(surface, (0,0,0), pts)
        
        super().render(surface)
    
    def get_value(self):
        return self.checked

    def set_value(self, value):
        if self.checked != value:
            self.checked = value
            self.set_changed(1)
    
    def on_release(self, event):
        if event.button == 1:
            self.set_value(not self.checked)
            return self.callback(self, *self.args)
        
        return False