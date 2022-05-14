import pygame
from .Vec import Vec

class Editor():
    """
    class that handle what to do when in edition mode
    """
    
    def __init__(self,game):
       self.game = game
       self.startmove = None
       self.moving = False
       self.current_type = 0
       
    
    def handle_events(self,events):
        if self.moving:
            newpos = Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
            self.game.camera.coo += (self.startmove-newpos)*Vec(1,-1)
            self.startmove = newpos
            self.game.camera.uptade_visible_tiles()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    self.startmove = Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                    self.moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    self.moving = False
                    
                 