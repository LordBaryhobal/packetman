from Vec import Vec

class Entity:
    def __init__(self):
        self.pos = Vec()
        self.vel = Vec()
        self.acc = Vec()
    
    def render(self, surface, pos):

