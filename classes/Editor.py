#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame
from .Vec import Vec
from .Rect import Rect
from .Hud import Hud

class Editor():
    """
    Class that handles edition mode
    """
    
    def __init__(self,game):
       self.game = game
       self.startmove = None
       self.moving = False
       self.placing = False
       self.selecting = False
       self.selection = None
       self.boundingbox = Rect()
       
       self.selected_tiles = []
       self.moveselection = False
       self.hud = Hud(self.game)
    
    def handle_events(self,events):
        
        
        if self.moving:
            newpos = Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
            self.game.camera.pos += (self.startmove-newpos)*Vec(1,-1)
            self.startmove = newpos
            self.game.camera.update_visible_tiles()
            
        if self.placing and self.selection is None:
            self.game.world.set_tile(self.game.camera.screen_to_world(Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])),self.hud.get_type())
            self.game.camera.update_visible_tiles()
        
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1:
                    self.placing = True
                    if self.selection is not None and self.selecting == False:
                        self.moveselection = True
                        
                        v1 = Vec(min(self.selection[0].x,self.selection[1].x),max(self.selection[0].y,self.selection[1].y))
                        v2 = Vec(max(self.selection[0].x,self.selection[1].x),min(self.selection[0].y,self.selection[1].y))
                        
                        self.selected_tiles = self.game.world.get_tiles_in_rect(v1,v2).copy()
                        self.modify_selection(0)
                        
                        self.start_selection_pos = self.game.camera.screen_to_world(Vec(*pygame.mouse.get_pos()))
                
                elif event.button == 2:
                    self.startmove = Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                    self.moving = True
                    self.hud.show_scrollbars()

                elif event.button == 3:
                    self.selection = [self.game.camera.screen_to_world(Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]))]
                    self.selecting = True
                
                elif event.button == 4:
                    self.hud.slot -= 1
                    self.hud.slot %= 9
                
                elif event.button == 5:
                    self.hud.slot += 1
                    self.hud.slot %= 9
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.placing = False
                    if self.selection is not None and self.selecting == False:
                        
                        #calculate displacement of the selection
                        displacement = self.game.camera.screen_to_world(Vec(*pygame.mouse.get_pos()))-self.start_selection_pos
                        
                        #place selection at the new position
                        ctr_pressed = pygame.key.get_pressed()[pygame.K_LCTRL]
                        self.place_selection(displacement,place_empty=ctr_pressed)
                        
                        #modify selection to the final destination
                        self.selection[0],self.selection[1] = (self.selection[0]+displacement).max(Vec()),(self.selection[1]+displacement).max(Vec())
                        
                        self.moveselection = False
                        self.selected_tiles = None
                    
                elif event.button == 2:
                    self.moving = False
                    self.hud.hide_scrollbars()
                
                elif event.button == 3:
                    self.selection.append(self.game.camera.screen_to_world(Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])))
                    if self.selection[0] == self.selection[1]:
                        self.selection = None
                    else:
                        v1 = self.selection[0].min(self.selection[1])
                        v2 = self.selection[0].max(self.selection[1])
                        self.selection = [v1,v2]
                    self.selecting = False
            
            elif event.type == pygame.KEYDOWN:
                if pygame.K_0 <= event.key <= pygame.K_9:
                    self.hud.set_hotbar(event.key-pygame.K_0)
                
                elif event.key == pygame.K_f:
                    if self.selection is not None:
                        self.modify_selection(self.hud.get_type())
                
                elif event.key == pygame.K_BACKSPACE:
                    if self.selection is not None and self.selecting == False:
                        self.modify_selection(0)
                
                elif event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                    path = input("Save level as: ")
                    self.game.world.save(path)
                
                elif event.key == pygame.K_l and event.mod & pygame.KMOD_CTRL:
                    path = input("Open level: ")
                    self.game.world.load(path)
                    self.game.camera.update_visible_tiles()
                    self.game.camera.update_visible_entities()
    
    def modify_selection(self,type):
        for x in range(self.selection[0].x,self.selection[1].x+1):
            for y in range(self.selection[0].y,self.selection[1].y+1):
                self.game.world.set_tile(Vec(x,y),type)
        self.game.camera.update_visible_tiles()
            
    def render(self, hud_surf, editor_surf):
        hud_surf.fill((0,0,0,0))
        editor_surf.fill((0,0,0,0))

        self.hud.render(hud_surf)

        if self.selecting:
            mousepos = self.game.camera.screen_to_world(Vec(*pygame.mouse.get_pos()))
            v1,v2 = self.game.camera.world_to_screen(self.selection[0]), self.game.camera.world_to_screen(mousepos)
            v1,v2 = v1.min(v2),v1.max(v2)
            
            self.boundingbox.from_vectors(v1-Vec(0,self.game.camera.tilesize),v2+Vec(self.game.camera.tilesize,0))
            self.boundingbox.render(editor_surf,(100,100,100),5)
            
        
        elif self.selection is not None:
            displacement = Vec()
            
            if self.moveselection:
                displacement = self.game.camera.screen_to_world(Vec(*pygame.mouse.get_pos()))-self.start_selection_pos
                for tile in self.selected_tiles.flatten():
                    tile.render(editor_surf, self.game.camera.world_to_screen(tile.pos+displacement),self.game.camera.tilesize)
            
            v1,v2 = self.game.camera.world_to_screen(self.selection[0]+displacement), self.game.camera.world_to_screen(self.selection[1]+displacement)
            v1,v2 = v1.min(v2),v1.max(v2)
            
            self.boundingbox.from_vectors(v1-Vec(0,self.game.camera.tilesize),v2+Vec(self.game.camera.tilesize,0))
            self.boundingbox.render(editor_surf,(100,100,100),5)
    
    def place_selection(self,displacement,place_empty=False):
        pos = self.selection[0]+displacement
        self.game.world.place_selection(self.selected_tiles,pos,place_empty)
        self.game.camera.update_visible_tiles()