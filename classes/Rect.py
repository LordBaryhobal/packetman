#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

class Rect:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def overlaps(self, r2):
        hor = not (r2.x >= self.x+self.w or self.x >= r2.x+r2.w)
        ver = not (r2.y >= self.y+self.h or self.y >= r2.y+r2.h)

        return hor and ver
    
    def from_vectors(self, topleft,bottomright):
        self.x = topleft.x
        self.y = topleft.y
        self.w = bottomright.x - topleft.x
        self.h = bottomright.y - topleft.y
    
    def render(self,surface,color,thickness=0):
        pygame.draw.rect(surface,color,(self.x,self.y,self.w,self.h),thickness)