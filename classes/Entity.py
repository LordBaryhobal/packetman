#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from Vec import Vec

class Entity:
    def __init__(self):
        self.pos = Vec()
        self.vel = Vec()
        self.acc = Vec()
    
    def render(self, surface, pos):

