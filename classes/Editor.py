#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame
from .Vec import Vec
from .Rect import Rect
from .Hud import Hud
from .Tile import Tile
from .Player import Player

class Editor():
    """
    Class that handles edition mode
    """
    
    def __init__(self,game):
        self.game = game
        self.move = [0,None] #0 = not moving, 1 = moving camera
        self.placing = 0 #0 = not placing, 1 = placing tiles, 2 = placing pasted tiles
        self.selection = [0,None,None] #0 = nothing selected, 1 = selecting, 2 = selected | selection[1 and 2] are the 2 corners of the selection
        self.boundingbox = Rect()
        
        self.moveselection = 0 #0 = not moving selection, 1 = moving selection
        self.selected_tiles = []
        self.copied_tiles = []
        
        self.select_entities = 0
        self.selected_entities = []
        self.move_selected_entity = 0
        self.selected_entity = None
        self.copied_entities = []
        self.hud = Hud(self.game)
    
    def handle_events(self,events):
        
        
        if self.move[0] == 1:
            newpos = self.get_mousepos()
            mvec = Vec(1,-1)
            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                mvec *= 5
            self.game.camera.pos += (self.move[1]-newpos)*mvec
            self.move[1] = newpos
            self.game.camera.update_visible_tiles()
            
        if self.placing == 1 and self.selection[0] != 2:
            pos = self.game.camera.screen_to_world(Vec(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]))
            tile = Tile(pos.x, pos.y, self.hud.get_type())
            self.game.world.set_tile(tile, pos)
            self.game.camera.update_visible_tiles()
        
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1:
                    if  pygame.key.get_pressed()[pygame.K_LCTRL]:
                        self.move = [1,self.get_mousepos()]
                        self.hud.show_scrollbars()
                    
                    elif pygame.key.get_pressed()[pygame.K_LALT]:
                        if self.selected_entity is not None:
                            self.selected_entity.highlight = False
                        pos = self.game.camera.screen_to_world(self.get_mousepos())
                        entity = self.game.world.get_entities_in_rect(pos+Vec(0,1),pos+Vec(1,0))
                        if len(entity) != 0:
                            self.selected_entity = entity[0]
                            self.selected_entity.highlight = True
                        else:
                            self.selected_entity = None
                    
                    elif self.selected_entity is not None:
                        self.move_selected_entity = 1

                    elif self.placing == 2:
                        self.placing = 0
                        #place selection at the new position
                        shift_pressed = pygame.key.get_pressed()[pygame.K_LSHIFT]
                        pos = self.game.camera.screen_to_world(self.get_mousepos())
                        self.game.world.place_selection(self.copied_tiles,pos,place_empty=shift_pressed)
                        for y,row in enumerate(self.copied_tiles):
                            for x,tile in enumerate(row):
                                self.copied_tiles[y][x] = tile.copy()
                        
                        self.game.camera.update_visible_tiles()

                        if len(self.copied_entities) != 0:
                            for entity in self.copied_entities:
                                newentity = entity.copy()
                                newentity.pos = pos+entity.pos
                                newentity.update()
                                self.game.world.entities.append(newentity)
                                self.selected_entities.append(newentity)
                                self.game.camera.update_visible_entities()
                        
                        

                        #set selection at the placement location:
                        otherpos = pos + Vec(len(self.copied_tiles[0])-1,len(self.copied_tiles)-1)
                        self.selection = [2,pos.max(Vec()),otherpos.max(Vec())]
                    else:
                        self.placing = 1
                        if self.selection[0]==2:
                            self.moveselection = 1
                            
                            v1 = Vec(min(self.selection[1].x,self.selection[2].x),max(self.selection[1].y,self.selection[2].y))
                            v2 = Vec(max(self.selection[1].x,self.selection[2].x),min(self.selection[1].y,self.selection[2].y))
                            
                            self.selected_tiles = self.game.world.get_tiles_in_rect(v1,v2).copy()
                            self.modify_selection(0)
                            
                            self.start_move_pos = self.game.camera.screen_to_world(self.get_mousepos())
                            if self.select_entities:
                                self.entity_start_move_pos = []
                                for entity in self.selected_entities:
                                    self.entity_start_move_pos.append(entity.pos)
                        
                

                if event.button == 2:
                    self.move = [1,self.get_mousepos()]
                    self.hud.show_scrollbars()

                elif event.button == 3:
                    if self.placing == 0 and self.moveselection == 0 and self.move_selected_entity == 0:
                        self.selection = [1,self.game.camera.screen_to_world(self.get_mousepos()),None]
                        self.select_entities = pygame.key.get_pressed()[pygame.K_LALT]
                        self.selected_entity = None
                        
                        self.highlight_entities(self.selected_entities,hightlight=False)
                            
                elif event.button == 4:
                    self.hud.slot -= 1
                    self.hud.slot %= 9
                
                elif event.button == 5:
                    self.hud.slot += 1
                    self.hud.slot %= 9
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.move_selected_entity == 1:
                        self.move_selected_entity = 0
                    
                    if self.move[0] == 1:
                        self.move[0] = 0
                        self.hud.hide_scrollbars()
                    
                    
                    self.placing = 0
                    if self.selection[0]==2 and self.moveselection==1:
                        
                        #calculate displacement of the selection
                        displacement = self.game.camera.screen_to_world(self.get_mousepos())-self.start_move_pos
                        
                        #place selection at the new position
                        shift_pressed = pygame.key.get_pressed()[pygame.K_LSHIFT]
                        self.game.world.place_selection(self.selected_tiles,self.selection[1]+displacement,place_empty=shift_pressed)
                        self.game.camera.update_visible_tiles()
                        
                        #modify selection to the final destination
                        self.selection[1],self.selection[2] = (self.selection[1]+displacement).max(Vec()),(self.selection[2]+displacement).max(Vec())
                        
                        self.moveselection = 0
                        self.selected_tiles = []
                    
                elif event.button == 2:
                    self.move[0] = 0
                    self.hud.hide_scrollbars()
                
                elif event.button == 3:
                    if self.placing == 0 and self.moveselection == 0 and self.selection[0] == 1:
                        
                        self.select_entities = pygame.key.get_pressed()[pygame.K_LALT]
                        
                        self.selection[2] = self.game.camera.screen_to_world(self.get_mousepos())
                        if self.selection[1] == self.selection[2]:
                            self.selection = [0,None,None]
                            self.select_entities = 0
                            self.highlight_entities(self.selected_entities,hightlight=False)
                            
                        else:
                            v1 = self.selection[1].min(self.selection[2])
                            v2 = self.selection[1].max(self.selection[2])
                            self.selection = [2,v1,v2]
                            
                            if self.select_entities:
                                #get the top left and bottom right corners of the selection
                                v1 = Vec(min(self.selection[1].x,self.selection[2].x),max(self.selection[1].y,self.selection[2].y)+1)
                                v2 = Vec(max(self.selection[1].x,self.selection[2].x)+1,min(self.selection[1].y,self.selection[2].y))
                                self.selected_entities = self.game.world.get_entities_in_rect(v1,v2)
                                self.highlight_entities(self.selected_entities,hightlight=True)
                                
            
            elif event.type == pygame.KEYDOWN:
                if pygame.K_0 <= event.key <= pygame.K_9:
                    self.hud.set_hotbar(event.key-pygame.K_0)
                
                elif event.key == pygame.K_f:
                    if self.selection[0] == 2:
                        self.modify_selection(self.hud.get_type())
                
                elif event.key == pygame.K_BACKSPACE:
                    if self.selected_entity is not None:
                        self.game.world.remove_entity(self.selected_entity)
                        self.game.camera.update_visible_entities()
                        self.selected_entity = None
                    
                    if self.selection[0] == 2:
                        self.modify_selection(0)
                    
                    if self.placing == 2:
                        self.placing = 0
                        self.selection = [0,None,None]
                    
                    if event.mod & pygame.KMOD_ALT:
                        v1 = Vec(min(self.selection[1].x,self.selection[2].x),max(self.selection[1].y,self.selection[2].y)+1)
                        v2 = Vec(max(self.selection[1].x,self.selection[2].x)+1,min(self.selection[1].y,self.selection[2].y))
                        entities = self.game.world.get_entities_in_rect(v1,v2)
                        for entity in entities:
                            if not isinstance(entity,Player):
                                self.game.world.remove_entity(entity)
                        self.game.camera.update_visible_entities()
                            
                
                elif event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                    path = input("Save level as: ")
                    self.game.world.save(path)
                
                elif event.key == pygame.K_l and event.mod & pygame.KMOD_CTRL:
                    path = input("Open level: ")
                    self.game.world.load(path)
                    self.game.camera.update_visible_tiles()
                    self.game.camera.update_visible_entities()
                
                elif event.key == pygame.K_c and event.mod & pygame.KMOD_CTRL and self.selection[0] ==2 and self.placing == 0:
                    v1 = Vec(min(self.selection[1].x,self.selection[2].x),max(self.selection[1].y,self.selection[2].y))
                    v2 = Vec(max(self.selection[1].x,self.selection[2].x),min(self.selection[1].y,self.selection[2].y))
                        
                    self.copied_tiles = self.game.world.get_tiles_in_rect(v1,v2).copy()
                    for y,row in enumerate(self.copied_tiles):
                        for x,tile in enumerate(row):
                            self.copied_tiles[y][x] = tile.copy()
                    
                    self.copied_entities = []
                    if len(self.selected_entities) != 0:
                        for entity in self.selected_entities:
                            if not isinstance(entity,Player):
                                self.copied_entities.append(entity.copy())
                        
                        for entity in self.copied_entities:
                            entity.pos = entity.pos-self.selection[1]
                
                elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL and self.placing == 0:
                    if len(self.copied_tiles) != 0 or len(self.copied_entities) != 0:
                        self.placing = 2
                        self.selection = [0,None,None]
                        self.select_entities = 0
                        self.highlight_entities(self.selected_entities,hightlight=False)
                        self.selected_entities = []
                    
                    
                    
                    
    
    def modify_selection(self,type):
        for x in range(self.selection[1].x,self.selection[2].x+1):
            for y in range(self.selection[1].y,self.selection[2].y+1):
                pos = Vec(x,y)
                tile = Tile(x, y, type)
                self.game.world.set_tile(tile, pos)
        self.game.camera.update_visible_tiles()
            
    def render(self, hud_surf, editor_surf):
        hud_surf.fill((0,0,0,0))
        editor_surf.fill((0,0,0,0))

        self.hud.render(hud_surf)

        if self.selection[0] == 1:
            mousepos = self.game.camera.screen_to_world(self.get_mousepos())
            v1,v2 = self.game.camera.world_to_screen(self.selection[1]), self.game.camera.world_to_screen(mousepos)
            v1,v2 = v1.min(v2),v1.max(v2)
            
            self.boundingbox.from_vectors(v1-Vec(0,self.game.camera.tilesize),v2+Vec(self.game.camera.tilesize,0))
            self.boundingbox.render(editor_surf,(100,100,100),5)
            
        
        elif self.selection[0] == 2:
            displacement = Vec()
            
            if self.moveselection:
                displacement = self.game.camera.screen_to_world(self.get_mousepos())-self.start_move_pos
                for tile in self.selected_tiles.flatten():
                    tile.render(editor_surf, self.game.camera.world_to_screen(tile.pos+displacement),self.game.camera.tilesize)
                
                if self.select_entities: #TODO fix entity rendering layer
                    for entity,start_pos in zip(self.selected_entities,self.entity_start_move_pos):
                        entity.pos = start_pos + displacement
                        entity.update()
                    
                
            
            v1,v2 = self.game.camera.world_to_screen(self.selection[1]+displacement), self.game.camera.world_to_screen(self.selection[2]+displacement)
            v1,v2 = v1.min(v2),v1.max(v2)
            
            self.boundingbox.from_vectors(v1-Vec(0,self.game.camera.tilesize),v2+Vec(self.game.camera.tilesize,0))
            self.boundingbox.render(editor_surf,(100,100,100),5)

        if self.placing == 2:
            pos = self.game.camera.screen_to_world(self.get_mousepos())
            for y,row in enumerate(self.copied_tiles):
                for x,tile in enumerate(row):
                    tile.render(editor_surf,self.game.camera.world_to_screen(pos+Vec(x,y)),self.game.camera.tilesize)

            
            v1,v2 = self.game.camera.world_to_screen(pos), self.game.camera.world_to_screen(pos+Vec(len(self.copied_tiles[0])-1,len(self.copied_tiles)-1))
            v1,v2 = v1.min(v2),v1.max(v2)
            
            self.boundingbox.from_vectors(v1-Vec(0,self.game.camera.tilesize),v2+Vec(self.game.camera.tilesize,0))
            self.boundingbox.render(editor_surf,(100,100,100),5)
            
            if len(self.copied_entities) != 0:
                for entity in self.copied_entities:
                    entity.render(editor_surf,self.game.camera.world_to_screen(pos+entity.pos),self.game.camera.tilesize)
        if self.move_selected_entity:
            pos = self.game.camera.screen_to_world(self.get_mousepos(),round_=False)
            self.selected_entity.pos = pos
            self.selected_entity.update()
        
        

    def get_mousepos(self):
        return Vec(*pygame.mouse.get_pos())

    def highlight_entities(self,entities,hightlight):
        for entity in entities:
            entity.highlight = hightlight
