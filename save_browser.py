#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import numpy as np
import pickle
import pygame
import struct

from classes.Entity import Entity
from classes.Logger import Logger
from classes.Player import Player
from classes.Tile import Tile
from classes.Vec import Vec

def to_value(val):
    base = type(val)
    
    if not base in [int, str, float, list, dict]:
        class Value:
            def __init__(self, v):
                self._v = v
            
            def __bool__(self):
                return bool(self._v)
            
            def __instancecheck__(self, __instance):
                return isinstance(self._v, __instance)
            
            @property
            def __class__(self):
                return self._v.__class__
            
            @property
            def __dict__(self):
                return self._v.__dict__.update(super().__dict__)
            
            def __repr__(self):
                return self._v.__repr__()
            
            def __getattribute__(self, attr):
                if attr in ["_v","_collapsed","_x","_y","_w","_h"]:
                    return super().__getattribute__(attr)
                
                return self._v.__getattribute__(attr)

            def __setattr__(self, attr, val):
                if attr in ["_v","_collapsed","_x","_y","_w","_h"]:
                    super().__setattr__(attr, val)
                
                else:
                    self._v.__setattr__(attr, val)
            
    else:
        class Value(base):
            pass
    
    val = Value(val)
    val._collapsed = False
    val._x, val._y, val._w, val._h = 0,0,0,0
    return val

class SaveFile:
    def __init__(self, path):
        self._path = path
        self.open()
        self.read()
    
    def open(self):
        self._file = open(self._path, "rb+")
    
    def close(self):
        self._file.close()
    
    def read(self):
        f = self._file
        f.seek(0)

        Logger.info(f"Loading level '{self._path}'")

        size_tiles = struct.unpack(">I", f.read(4))[0]
        size_entities = struct.unpack(">I", f.read(4))[0]
        self.WIDTH = struct.unpack(">H", f.read(2))[0]
        self.HEIGHT = struct.unpack(">H", f.read(2))[0]
        
        self.tiles = np.empty([self.HEIGHT, self.WIDTH], dtype='object')
        self.entities = []

        Logger.info("Loading tiles")
        while f.tell() < size_tiles+12:
            size = struct.unpack(">H", f.read(2))[0]
            type_ = struct.unpack(">H", f.read(2))[0]
            x = struct.unpack(">H", f.read(2))[0]
            y = struct.unpack(">H", f.read(2))[0]

            cls = b""

            while True:
                c = f.read(1)
                if c == b"\0": break
                cls += c

            attrs = pickle.loads(f.read(size - len(cls) - 7))

            cls = globals()[str(cls, "utf-8")]
            tile = cls(x, y, type_)
            for k, v in attrs.items():
                setattr(tile, k, v)
            
            self.tiles[y, x] = tile
        
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.tiles[y, x] is None:
                    self.tiles[y, x] = Tile(x, y)
        
        Logger.info("Loading entities")
        while f.tell() < size_entities+size_tiles+12:
            size = struct.unpack(">H", f.read(2))[0]
            type_ = struct.unpack(">H", f.read(2))[0]
            x = struct.unpack(">f", f.read(4))[0]
            y = struct.unpack(">f", f.read(4))[0]
            vx = struct.unpack(">f", f.read(4))[0]
            vy = struct.unpack(">f", f.read(4))[0]

            cls = b""

            while True:
                c = f.read(1)
                if c == b"\0": break
                cls += c
            
            attrs = pickle.loads(f.read(size - len(cls) - 19))

            cls = globals()[str(cls, "utf-8")]
            entity = cls(pos=Vec(x, y), vel=Vec(vx, vy), type_=type_)

            for k, v in attrs.items():
                setattr(entity, k, v)
            
            self.entities.append(entity)
            #if cls == Player:
            #    self.player = entity
        
        Logger.info("Level loaded successfully (maybe)")

        self.__dict__ = to_value(self.__dict__)
        SaveFile.convert(self.__dict__)
    
    def convert(obj):
        if isinstance(obj, list):
            items = list(map(lambda v: (None, v), obj))
        else:
            items = obj.items()

        l = []

        for k,v in items:
            if not k is None:
                if isinstance(k, str) and k.startswith("_"):
                    continue
            
            if isinstance(v, (int, float, str, bool)):
                v = to_value(v)
            
            elif isinstance(v, (list, np.ndarray)):
                if isinstance(v, np.ndarray):
                    v = list(v.flatten())

                v = to_value(SaveFile.convert(v))
                
            elif isinstance(v, dict):
                SaveFile.convert(v)
                v = to_value(v)
            
            elif hasattr(v, "__dict__"):
                SaveFile.convert(v.__dict__)
                v = to_value(v)
            
            else:
                v = to_value(v)
            
            if isinstance(obj, dict):
                obj[k] = v
            else:
                l.append(v)
        
        if isinstance(obj, list):
            return l

class Browser:
    WIDTH, HEIGHT = 800, 600
    INDENT = 30
    SCROLL_SPEED = 40

    def __init__(self):
        self.save_file = None
        self.running = True

        pygame.init()
        self.w = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.scroll = 0
    
    def close_file(self):
        if self.save_file:
            self.save_file.close()
        
        self.save_file = None

    def loop(self):
        events = pygame.event.get()

        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_file()
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and event.mod & pygame.KMOD_CTRL:
                    self.close_file()
                
                elif event.key == pygame.K_o and event.mod & pygame.KMOD_CTRL:
                    path = input("File path: ")
                    if path:
                        self.save_file = SaveFile(path)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.scroll -= self.SCROLL_SPEED
                
                elif event.button == 5:
                    self.scroll += self.SCROLL_SPEED
                
                elif event.button == 1:
                    self.click(event.pos, recursive=keys[pygame.K_LSHIFT], modify=keys[pygame.K_LCTRL])
    
    def txt(self, txt):
        return self.font.render(txt, True, (255,255,255))

    def render(self):
        pygame.display.set_caption(f"Save Browser - {self.clock.get_fps():.2f}fps")
        self.w.fill(0)

        if self.save_file:
            self.render_obj(self.save_file.__dict__, 1, -self.scroll)

        pygame.display.update()

        self.clock.tick(30)
    
    def render_obj(self, obj, lvl=0, y=0):
        if y > self.HEIGHT:
            return y

        X = lvl * self.INDENT
        
        if isinstance(obj, list):
            items = [(None, v) for v in obj]
        else:
            items = obj.items()

        for k,v in items:

            X2 = X
            if not k is None:
                if isinstance(k, str) and k.startswith("_"):
                    continue
                
                key = self.txt(f"{k}: ")

                self.w.blit(key, [X, y])
                X2 += key.get_width()
            
            if isinstance(v, (int, float, str, bool)):
                val = self.txt(str(v))
                self.w.blit(val, [X2, y])

                v._x, v._y = X, y
                v._w, v._h = X2-X+val.get_width(), val.get_height()

                y += val.get_height()
            
            elif isinstance(v, (list, np.ndarray)):
                t = self.txt("[")
                self.w.blit(t, [X2, y])
                
                v._x, v._y = X, y
                v._w, v._h = X2-X+t.get_width(), t.get_height()

                y += t.get_height()

                if isinstance(v, np.ndarray):
                    v = list(v.flatten())

                if not v._collapsed:
                    y = self.render_obj(v, lvl+1, y)
                
                t = self.txt("]")
                self.w.blit(t, [X, y])
                y += t.get_height()
                
            elif isinstance(v, dict):
                t = self.txt("{")
                self.w.blit(t, [X2, y])

                v._x, v._y = X, y
                v._w, v._h = X2-X+t.get_width(), t.get_height()
                
                y += t.get_height()

                if not v._collapsed:
                    y = self.render_obj(v, lvl+1, y)
                
                t = self.txt("}")
                self.w.blit(t, [X, y])
                y += t.get_height()
            
            elif hasattr(v, "__dict__"):
                t = self.txt(f"<{v.__class__.__name__}> {{")
                self.w.blit(t, [X2, y])

                v._x, v._y = X, y
                v._w, v._h = X2-X+t.get_width(), t.get_height()

                y += t.get_height()
                
                if not v._collapsed:
                    y = self.render_obj(v.__dict__, lvl+1, y)
                
                t = self.txt("}")
                self.w.blit(t, [X, y])
                y += t.get_height()
            
            else:
                t = self.txt(f"<{v.__class__.__name__}>")
                self.w.blit(t, [X2, y])

                v._x, v._y = X, y
                v._w, v._h = X2-X+t.get_width(), t.get_height()

                y += t.get_height()
        
            if (k is None or not k.startswith("_")) and v._collapsed:
                pygame.draw.circle(self.w, (100,0,0), [v._x+v._w+20, v._y+v._h/2], 5)
            
        return y
    
    def click(self, pos, recursive=False, modify=False):
        if recursive: modify = False

        if self.save_file:
            clicked = Browser.check_click(self.save_file.__dict__, pos, recursive)
            if not clicked is None:
                if modify:
                    print(f"Clicked {clicked}")
                    if isinstance(clicked, (str, int, float)):
                        pass
        
    def check_click(obj, pos, recursive=False, c=None):
        return_val = None

        if recursive and not c is None:
            obj._collapsed = c
        
        if obj._x <= pos[0] < obj._x+obj._w:
            if obj._y <= pos[1] < obj._y+obj._h:
                obj._collapsed = not obj._collapsed
                return_val = obj
                
                if recursive:
                    c = obj._collapsed
                else:
                    return return_val

        if not obj._collapsed or recursive:
            if isinstance(obj, (list, np.ndarray)):
                for n in obj:
                    r = Browser.check_click(n, pos, recursive, c)
                    if not r is None:
                        if not recursive:
                            return r
            
            elif isinstance(obj, dict):
                for k,v in obj.items():
                    if not k.startswith("_"):
                        r = Browser.check_click(v, pos, recursive, c)
                        if not r is None:
                            if not recursive:
                                return r
            
            elif hasattr(obj, "__dict__"):
                for k,v in obj.__dict__.items():
                    if not k.startswith("_"):
                        r = Browser.check_click(v, pos, recursive, c)
                        if not r is None:
                            if not recursive:
                                return r
        return return_val

if __name__ == "__main__":
    #s = SaveFile("./levels/level4.dat")
    b = Browser()

    while b.running:
        b.loop()
        b.render()