#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Component import Component
from .Constraints import *

class Menu(Component):
    def __init__(self, game, name=None):
        self.game = game
        super().__init__(name)
        self.cm.set_x(Absolute(0))
        self.cm.set_y(Absolute(0))
        self.cm.set_w(Absolute(self.game.WIDTH))
        self.cm.set_h(Absolute(self.game.HEIGHT))
        
        self.visible = False
        self.bg_color = (0,0,0)
    
    def on_click(self, event):
        return True
    
    def on_release(self, event):
        return True
    
    def on_mouse_down(self, event):
        return True
    
    def on_mouse_up(self, event):
        return True