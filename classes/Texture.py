#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import glob
import os

import pygame

from classes.Copyable import Copyable
from classes.Logger import Logger
from classes.Path import Path
from classes.Vec import Vec

class Texture(Copyable):
    """Tile/Entity texture class"""
    
    _cache = {}

    WIDTH = 32
    HEIGHT = 32
    
    TOTAL = 0
    LOADED = 0

    def __init__(self, name=None, id_=None, width=WIDTH, height=HEIGHT):
        """Initializes a Texture instance

        Keyword Arguments:
            name {str} -- name of the texture (default: {None})
            id_ {int} -- texture id, for connected textures (default: {None})
        """

        self.name = name
        self.id = id_
        self.img, self.h_tiles, self.v_tiles = Texture.get(self.name, self.id) if name else (None, 0, 0)
        self.WIDTH = width
        self.HEIGHT = height

    def load_all(game):
        Texture.TOTAL = len(glob.glob(Path("assets", "textures", "**", "*.png"), recursive=True))
        Texture.LOADED = 0
        Texture.load_walk(game, Path("assets", "textures"))
    
    def load_walk(game, path, name=""):
        content = os.listdir(path)
        tilesize = game.HEIGHT//game.config["number_of_tiles"]

        for f in content:
            p = Path(path, f)

            if os.path.isdir(p):
                n = name
                if n: n += "."
                n += f

                Texture.load_walk(game, p, n)
            
            elif os.path.splitext(f)[1] == ".png":
                n = name
                if n: n += "."
                n += os.path.splitext(f)[0]

                img = pygame.image.load(p).convert_alpha()

                w = img.get_width()/Texture.WIDTH
                h = img.get_height()/Texture.HEIGHT

                img = pygame.transform.scale(img, [
                    int(w*tilesize),
                    int(h*tilesize)
                ])
                Texture._cache[n] = (img, w, h)
                Texture.LOADED += 1

    def get(name, id_):
        """Returns a texture from name and id

        Checks if texture is already loaded in the cache, loads it if not

        Arguments:
            name {str} -- name of the texture
            id_ {int} -- texture id, for connected textures

        Returns:
            pygame.Image -- texture image
        """

        if not name in Texture._cache:
            """
            path_jpg = Path("assets", "textures", name+".jpg")
            path_png = Path("assets", "textures", name+".png")

            if os.path.exists(path_jpg):
                path = path_jpg
            else:
                path = path_png
            
            Texture._cache[name] = pygame.image.load(path).convert_alpha()
            """
            Logger.error(f"Texture {name} not loaded")
        
        return Texture._cache[name]

    def render(self, surface, pos, tilesize, dimensions=Vec(1,1)):
        """Renders the texture

        Arguments:
            surface {pygame.Surface} -- surface to render the texture on
            pos {Vec} -- pixel coordinates where to render on the surface (bottom left corner)
            tilesize {int} -- size of a tile in pixels
            dimensions {Vec} -- dimensions of the texture (default: {Vec(1,1)})
        """
        
        self.img, self.h_tiles, self.v_tiles = Texture.get(self.name, self.id) if self.name else (None, 0, 0)
        tw, th = tilesize*dimensions.x, tilesize*dimensions.y
        w, h = int(self.h_tiles*tw), int(self.v_tiles*th)
        img = self.img

        # dimensions is the size of the object in tiles
        if (w, h) != img.get_size():
            img = pygame.transform.scale(img, (w, h))
        
        x, y = 0, 0
        if not self.id is None:
            x = (self.id % self.h_tiles) * tw
            y = (self.id // self.h_tiles) * th

        surface.blit(img, [pos.x, pos.y-th], [x, y, tw, th])