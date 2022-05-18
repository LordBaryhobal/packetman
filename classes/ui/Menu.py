#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Component import Component
from .Constraints import *

class Menu(Component):
    def __init__(self, game):
        self.game = game
        super().__init__(
            ConstantConstraint(0),
            ConstantConstraint(0),
            ConstantConstraint(self.game.WIDTH),
            ConstantConstraint(self.game.HEIGHT)
        )
        
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