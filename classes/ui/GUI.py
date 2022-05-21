#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Component import Component
from .Constraints import *

class GUI(Component):
    def __init__(self, game, name=None):
        self.game = game
        super().__init__(name)
        self.cm.set_x(Absolute(0))
        self.cm.set_y(Absolute(0))
        self.cm.set_w(Absolute(self.game.WIDTH))
        self.cm.set_h(Absolute(self.game.HEIGHT))

    def render(self, surface):
        for child in self.children:
            child.render(surface)
    
    def handle_events(self, events):
        for event in events:
            if self.handle_event(event):
                event.handled = True
            