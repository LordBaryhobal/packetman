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
    
    def __init__(self, game):
        """Initializes an Editor instance

        Arguments:
            game {Game} -- Game instance
        """

        self.game = game
        self.move = [0, None] #0 = not moving, 1 = moving camera
        self.placing = 0 #0 = not placing, 1 = placing tiles, 2 = placing pasted tiles
        self.selection = [0, None, None] #0 = nothing selected, 1 = selecting, 2 = selected | selection[1 and 2] are the 2 corners of the selection
        self.boundingbox = Rect()
        
        self.moveselection = 0 #0 = not moving selection, 1 = moving selection
        self.selected_tiles = []
        self.copied_tiles = []
        
        self.select_entities = 0
        self.selected_entities = []
        self.move_selected_entity = 0
        self.selected_entity = None # None = no entity selected | Entity = entity selected
        self.copied_entities = []
        self.hud = Hud(self.game)
    
    def handle_events(self, events):
        """Handles events

        Arguments:
            events {list[pygame.Event]} -- list of pygame events
        """
        #moving camera
        if self.move[0] == 1:
            newpos = self.get_mousepos()
            mvec = Vec(1,-1)
            
            #if shift is pressed, move 5x faster
            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                mvec *= 5
            
            self.game.camera.pos += (self.move[1]-newpos)*mvec
            self.move[1] = newpos
            self.game.camera.update_visible_tiles()
            
        #placing == 1 --> placing tiles
        if self.placing == 1 and self.selection[0] != 2:
            pos = self.game.camera.screen_to_world(self.get_mousepos())
            tile = Tile(pos.x, pos.y, self.hud.get_type())
            self.game.world.set_tile(tile, pos)
            self.game.camera.update_visible_tiles()
        
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1:
                    #move camera
                    if  pygame.key.get_pressed()[pygame.K_LCTRL]:
                        self.move = [1, self.get_mousepos()]
                        self.hud.show_scrollbars()
                    
                    #select a single entity
                    elif pygame.key.get_pressed()[pygame.K_LALT]:
                        #unselect all tiles and entities
                        self.selection = [0,None,None]
                        self.highlight_entities(self.selected_entities, False)
                        self.selected_entities = []
                        
                        #unhighlight old entity
                        if self.selected_entity is not None:
                            self.selected_entity.highlight = False
                        
                        pos = self.game.camera.screen_to_world(self.get_mousepos())
                        entity = self.game.world.get_entities_in_rect(pos+Vec(0,1), pos+Vec(1,0))
                        
                        if len(entity) != 0:
                            self.selected_entity = entity[0]
                            self.selected_entity.highlight = True
                        else:
                            self.selected_entity = None
                    
                    #move entity if one is selected
                    elif self.selected_entity is not None:
                        self.move_selected_entity = 1
                    
                    #place the pasted tiles
                    elif self.placing == 2:
                        #no more placing pasted tiles
                        self.placing = 0
                        
                        #place selection at the new position
                        shift_pressed = pygame.key.get_pressed()[pygame.K_LSHIFT]
                        pos = self.game.camera.screen_to_world(self.get_mousepos())
                        self.game.world.place_selection(self.copied_tiles, pos, place_empty=shift_pressed)
                        for y,row in enumerate(self.copied_tiles):
                            for x,tile in enumerate(row):
                                self.copied_tiles[y,x] = tile.copy()
                        
                        self.game.camera.update_visible_tiles()
                        
                        #copy entity and add them to world.entities
                        if len(self.copied_entities) != 0:
                            for entity in self.copied_entities:
                                newentity = entity.copy()
                                newentity.pos = pos+entity.pos
                                newentity.update()
                                self.game.world.entities.append(newentity)
                                self.selected_entities.append(newentity)
                                self.game.camera.update_visible_entities()
                        
                        #set selection at the placement location:
                        otherpos = pos + Vec(len(self.copied_tiles[0])-1, len(self.copied_tiles)-1)
                        self.selection = [2, pos.max(Vec()), otherpos.max(Vec())]
                    
                    #start moving the selected tiles/entities
                    else:
                        self.placing = 1
                        if self.selection[0]==2:
                            self.moveselection = 1
                            
                            tl,br = self.selection[1].get_tl_br_corners(self.selection[2])
                            
                            self.selected_tiles = self.game.world.get_tiles_in_rect(tl,br).copy()
                            self.modify_selection(0)
                            
                            self.start_move_pos = self.game.camera.screen_to_world(self.get_mousepos())
                            if self.select_entities:
                                self.entity_start_move_pos = []
                                for entity in self.selected_entities:
                                    self.entity_start_move_pos.append(entity.pos)
                        
                
                #start moving camera
                if event.button == 2:
                    self.move = [1, self.get_mousepos()]
                    self.hud.show_scrollbars()
                
                #start selecting an area
                elif event.button == 3:
                    if self.placing == 0 and self.moveselection == 0 and self.move_selected_entity == 0:
                        self.selection = [1, self.game.camera.screen_to_world(self.get_mousepos()), None]
                        self.select_entities = pygame.key.get_pressed()[pygame.K_LALT]
                        
                        if self.selected_entity is not None:
                            self.selected_entity.highlight = False
                            self.selected_entity = None
                        
                        self.highlight_entities(self.selected_entities, highlight=False)
                        
                            
                elif event.button == 4:
                    self.hud.slot -= 1
                    self.hud.slot %= 9
                
                elif event.button == 5:
                    self.hud.slot += 1
                    self.hud.slot %= 9
            
            
            elif event.type == pygame.MOUSEBUTTONUP:
                
                
                if event.button == 1:
                    #if we are moving an entity, stop moving it
                    if self.move_selected_entity == 1:
                        self.move_selected_entity = 0
                    
                    #if we are moving the camera, stop moving it
                    if self.move[0] == 1:
                        self.move[0] = 0
                        self.hud.hide_scrollbars()
                    
                    #stop placing tiles
                    self.placing = 0
                    
                    #if we are moving the selection, place it and stop moving it
                    if self.selection[0]==2 and self.moveselection==1:
                        
                        #calculate displacement of the selection
                        displacement = self.game.camera.screen_to_world(self.get_mousepos())-self.start_move_pos
                        
                        #place selection at the new position
                        shift_pressed = pygame.key.get_pressed()[pygame.K_LSHIFT]
                        self.game.world.place_selection(self.selected_tiles, self.selection[1]+displacement, place_empty=shift_pressed)
                        self.game.camera.update_visible_tiles()
                        
                        #modify selection to the final destination
                        self.selection[1], self.selection[2] = (self.selection[1]+displacement).max(Vec()),(self.selection[2]+displacement).max(Vec())
                        
                        self.moveselection = 0
                        self.selected_tiles = []
                
                #stop moving the camera
                elif event.button == 2:
                    self.move[0] = 0
                    self.hud.hide_scrollbars()
                
                
                elif event.button == 3:
                    
                    #if we are selecting an area, finish selection with the 2nd point
                    if self.placing == 0 and self.moveselection == 0 and self.selection[0] == 1:
                        
                        self.select_entities = pygame.key.get_pressed()[pygame.K_LALT]
                        
                        self.selection[2] = self.game.camera.screen_to_world(self.get_mousepos())
                        
                        #if the mouse didn't change postion, don't select anything
                        if self.selection[1] == self.selection[2]:
                            self.selection = [0, None, None]
                            self.select_entities = 0
                            self.highlight_entities(self.selected_entities, highlight=False)
                            
                        else:
                            bl,tr = self.selection[1].get_bl_tr_corners(self.selection[2])
                            self.selection = [2, bl, tr]
                            
                            if self.select_entities:
                                #get the top left and bottom right corners of the selection
                                tl,br = self.selection[1].get_tl_br_corners(self.selection[2])
                                tl += Vec(0,1)
                                br += Vec(1,0)
                                self.selected_entities = self.game.world.get_entities_in_rect(tl,br)
                                self.highlight_entities(self.selected_entities, highlight=True)
                                
            
            elif event.type == pygame.KEYDOWN:
                #change the hotbar
                if pygame.K_0 <= event.key <= pygame.K_9:
                    self.hud.set_hotbar(event.key-pygame.K_0)
                
                #fill selection with tile of the current type
                elif event.key == pygame.K_f:
                    if self.selection[0] == 2:
                        self.modify_selection(self.hud.get_type())
                
                elif event.key == pygame.K_BACKSPACE:
                    #remove the selected entity
                    if self.selected_entity is not None:
                        self.game.world.remove_entity(self.selected_entity)
                        self.game.camera.update_visible_entities()
                        self.selected_entity = None
                    
                    #remove the tiles in the selection
                    if self.selection[0] == 2:
                        self.modify_selection(0)
                    
                    #stop placing the pasted tiles/entities
                    if self.placing == 2:
                        self.placing = 0
                        self.selection = [0, None, None]
                    
                    #remove all the entities (except the player) in the selection
                    if event.mod & pygame.KMOD_ALT:
                        tl,br = self.selection[1].get_tl_br_corners(self.selection[2])
                        tl += Vec(0,1)
                        br += Vec(1,0)
                        entities = self.game.world.get_entities_in_rect(tl,br)
                        for entity in entities:
                            if not isinstance(entity, Player):
                                self.game.world.remove_entity(entity)
                        self.game.camera.update_visible_entities()
                            
                #save the world
                elif event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                    path = input("Save level as: ")
                    self.game.world.save(path)
                
                #load world
                elif event.key == pygame.K_l and event.mod & pygame.KMOD_CTRL:
                    path = input("Open level: ")
                    self.game.world.load(path)
                    self.game.camera.update_visible_tiles()
                    self.game.camera.update_visible_entities()
                
                #copy the selection
                elif event.key == pygame.K_c and event.mod & pygame.KMOD_CTRL and self.selection[0] ==2 and self.placing == 0:
                    v1,v2 = self.selection[1].get_tl_br_corners(self.selection[2])
                        
                    self.copied_tiles = self.game.world.get_tiles_in_rect(v1,v2).copy()
                    for y,row in enumerate(self.copied_tiles):
                        for x,tile in enumerate(row):
                            self.copied_tiles[y][x] = tile.copy()
                    
                    #remove the copied entities from last time
                    self.copied_entities = []
                    
                    #copy the entities(except the player) if some are selected
                    if len(self.selected_entities) != 0:
                        for entity in self.selected_entities:
                            if not isinstance(entity, Player):
                                self.copied_entities.append(entity.copy())
                        
                        #change the postion of the copied tiles to be relative to the bottom left corner of the selection
                        for entity in self.copied_entities:
                            entity.pos = entity.pos-self.selection[1]
                
                #start placing the copied tiles/entities
                elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL and self.placing == 0:
                    if len(self.copied_tiles) != 0 or len(self.copied_entities) != 0:
                        self.placing = 2
                        #unselect old selection
                        self.selection = [0, None, None]
                        
                        #unselect old selected entities
                        self.select_entities = 0
                        self.highlight_entities(self.selected_entities, highlight=False)
                        self.selected_entities = []
                
                #duplicate the selected entity
                elif event.key == pygame.K_d and self.selected_entity is not None:
                    #verify its not the player
                    if not isinstance(self.selected_entity, Player):
                        self.selected_entity.highlight = False
                        self.selected_entity = self.selected_entity.copy()
                        self.selected_entity.highlight = True
                        self.game.world.entities.append(self.selected_entity)
                        self.game.camera.update_visible_entities()
                
                #open the entity menu
                elif event.key == pygame.K_m:
                    if self.selected_entity is not None and not isinstance(self.selected_entity, Player):
                        self.game.open_entity_settings()
                        print(self.selected_entity.vel)
                    

    
    def modify_selection(self, type):
        """Fills selection with certain tile type

        Arguments:
            type {int} -- tile type to fill
        """

        for x in range(self.selection[1].x, self.selection[2].x+1):
            for y in range(self.selection[1].y, self.selection[2].y+1):
                pos = Vec(x, y)
                tile = Tile(x, y, type)
                self.game.world.set_tile(tile, pos)
        self.game.camera.update_visible_tiles()
            
    def render(self, hud_surf, editor_surf):
        """Renders the editor

        Arguments:
            hud_surf {pygame.Surface} -- surface to render the hud on
            editor_surf {pygame.Surface} -- surface to render the selections on
        """
        
        hud_surf.fill((0,0,0,0))
        editor_surf.fill((0,0,0,0))

        self.hud.render(hud_surf)
        
        #render the selection with 1 point and the mouse position
        if self.selection[0] == 1:
            mousepos = self.game.camera.screen_to_world(self.get_mousepos())
            v1, v2 = self.game.camera.world_to_screen(self.selection[1]), self.game.camera.world_to_screen(mousepos)
            bl, tr = v1.get_bl_tr_corners(v2)
            
            self.boundingbox.from_vectors(bl-Vec(0, self.game.camera.tilesize), tr+Vec(self.game.camera.tilesize,0))
            self.boundingbox.render(editor_surf,(100,100,100),5)
            
        #render the selection when the 2 points are defined
        elif self.selection[0] == 2:
            displacement = Vec()
            
            #if we are moving the selection we need to displace the selection(only visually)
            if self.moveselection:
                
                displacement = self.game.camera.screen_to_world(self.get_mousepos())-self.start_move_pos
                
                #render moving tiles
                for tile in self.selected_tiles.flatten():
                    tile.render(editor_surf, self.game.camera.world_to_screen(tile.pos+displacement),self.game.camera.tilesize)
                
                #render moving entities
                if self.select_entities: #TODO fix entity rendering layer
                    for entity,start_pos in zip(self.selected_entities,self.entity_start_move_pos):
                        entity.pos = start_pos + displacement
                        entity.update()
            
            #render the selection
            v1, v2 = self.game.camera.world_to_screen(self.selection[1]+displacement), self.game.camera.world_to_screen(self.selection[2]+displacement)
            bl, tr = v1.get_bl_tr_corners(v2)
            
            self.boundingbox.from_vectors(bl-Vec(0, self.game.camera.tilesize), tr+Vec(self.game.camera.tilesize,0))
            self.boundingbox.render(editor_surf,(100,100,100),5)
        
        #render the pasted tiles
        if self.placing == 2:
            pos = self.game.camera.screen_to_world(self.get_mousepos())
            for y,row in enumerate(self.copied_tiles):
                for x,tile in enumerate(row):
                    tile.render(editor_surf, self.game.camera.world_to_screen(pos+Vec(x, y)), self.game.camera.tilesize)

            
            v1, v2 = self.game.camera.world_to_screen(pos), self.game.camera.world_to_screen(pos+Vec(len(self.copied_tiles[0])-1, len(self.copied_tiles)-1))
            bl, tr = v1.get_bl_tr_corners(v2)
            
            self.boundingbox.from_vectors(bl-Vec(0, self.game.camera.tilesize), tr+Vec(self.game.camera.tilesize,0))
            self.boundingbox.render(editor_surf,(100,100,100),5)
            
            #render entities if there are any
            if len(self.copied_entities) != 0:
                for entity in self.copied_entities:
                    #entity.pos is relative to the bottom left corner of the selection
                    entity.render(editor_surf, self.game.camera.world_to_screen(pos+entity.pos), self.game.camera.tilesize)
        
        #modify the selected entity position to the mouse position
        if self.move_selected_entity:
            pos = self.game.camera.screen_to_world(self.get_mousepos(), round_=False)
            self.selected_entity.pos = pos
            self.selected_entity.update()
        
        

    def get_mousepos(self):
        """Gets the mouse position as a Vec

        Returns:
            Vec -- mouse position
        """

        return Vec(*pygame.mouse.get_pos())

    def highlight_entities(self, entities, highlight):
        """Sets the highlight state of a list of entities

        Arguments:
            entities {list[Entity]} -- list of entities to modify
            highlight {bool} -- new highlight state
        """

        for entity in entities:
            entity.highlight = highlight
