#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

class GUI:
    def __init__(self, children=None):
        if children is None:
            children = []
        
        self.children = children

    def render(self, surface):
        for child in self.children:
            child.render(surface, child.x, child.y, child.w, child.h)
    
    def add(self, child):
        self.children.append(child)