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
            self.game.camera.update_visible_tiles()
        
        for event in events:
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    self.startmove = Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                    self.moving = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    self.moving = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9):
                    self.current_type = event.key-48
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.game.world.set_tile(self.game.camera.screen_to_world(Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])),self.current_type)
                self.game.camera.update_visible_tiles()
            
                    
                 