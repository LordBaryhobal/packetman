#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import numpy as np

class World:
    """
    World class holding world tiles and entities. Also processes physics.
    """

    WIDTH = 10
    HEIGHT = 10

    def __init__(self, game):
        self.game = game
        self.tiles = np.zeros([self.WIDTH, self.HEIGHT])
    
    def render(self):
        pass

    def physics(self, delta):
        pass