#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Component import Component
from .Constraints import *

class GUI(Component):
    def __init__(self, game):
        self.game = game
        super().__init__(
            ConstantConstraint(0),
            ConstantConstraint(0),
            ConstantConstraint(self.game.WIDTH),
            ConstantConstraint(self.game.HEIGHT)
        )

    def render(self, surface):
        for child in self.children:
            child.render(surface, child.x, child.y, child.w, child.h)
    
    def handle_events(self, events):
        for event in events:
            if self.handle_event(event):
                event.handled = True
            