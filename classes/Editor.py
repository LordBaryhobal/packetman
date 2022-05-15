import pygame
from .Vec import Vec
from .Rect import Rect

class Editor():
    """
    class that handle what to do when in edition mode
    """
    
    def __init__(self,game):
       self.game = game
       self.current_type = 0
       self.startmove = None
       self.moving = False
       self.placing = False
       self.selecting = False
       self.selection = None
       self.boundingbox = Rect()
       
       self.selected_tiles = []
       self.moveselection = False
       
    
    def handle_events(self,events):
        
        
        if self.moving:
            newpos = Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
            self.game.camera.pos += (self.startmove-newpos)*Vec(1,-1)
            self.startmove = newpos
            self.game.camera.update_visible_tiles()
            
        if self.placing and self.selection is None:
            self.game.world.set_tile(self.game.camera.screen_to_world(Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])),self.current_type)
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
                
                if event.button == 2:
                    self.startmove = Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                    self.moving = True

                if event.button == 3:
                    self.selection = [self.game.camera.screen_to_world(Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]))]
                    self.selecting = True
            
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
                if event.key in (pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9):
                    self.current_type = event.key-48
                
                elif event.key == pygame.K_f:
                    if self.selection is not None:
                        self.modify_selection(self.current_type)
                
                elif event.key == pygame.K_BACKSPACE:
                    if self.selection is not None:
                        self.modify_selection(0)
                
                elif event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                    path = input("Save level as: ")
                    self.game.world.save(path)
    
    def modify_selection(self,type):
        for x in range(self.selection[0].x,self.selection[1].x+1):
            for y in range(self.selection[0].y,self.selection[1].y+1):
                self.game.world.set_tile(Vec(x,y),type)
        self.game.camera.update_visible_tiles()
            
    def render(self,surface):
        if self.selecting:
            mousepos = self.game.camera.screen_to_world(Vec(*pygame.mouse.get_pos()))
            v1,v2 = self.game.camera.world_to_screen(self.selection[0]), self.game.camera.world_to_screen(mousepos)
            v1,v2 = v1.min(v2),v1.max(v2)
            
            self.boundingbox.from_vectors(v1-Vec(0,self.game.camera.tilesize),v2+Vec(self.game.camera.tilesize,0))
            self.boundingbox.render(surface,(100,100,100),5)
            
        
        elif self.selection is not None:
            displacement = Vec()
            
            if self.moveselection:
                displacement = self.game.camera.screen_to_world(Vec(*pygame.mouse.get_pos()))-self.start_selection_pos
                for tile in self.selected_tiles.flatten():
                    tile.render(surface, self.game.camera.world_to_screen(tile.pos+displacement),self.game.camera.tilesize)
            
            v1,v2 = self.game.camera.world_to_screen(self.selection[0]+displacement), self.game.camera.world_to_screen(self.selection[1]+displacement)
            v1,v2 = v1.min(v2),v1.max(v2)
            
            self.boundingbox.from_vectors(v1-Vec(0,self.game.camera.tilesize),v2+Vec(self.game.camera.tilesize,0))
            self.boundingbox.render(surface,(100,100,100),5)
    
    def place_selection(self,displacement,place_empty=False):
        pos = self.selection[0]+displacement
        self.game.world.place_selection(self.selected_tiles,pos,place_empty)
        self.game.camera.update_visible_tiles()