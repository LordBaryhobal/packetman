#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

from classes.Copyable import Copyable
from classes.Path import Path
from classes.Vec import Vec

class Texture(Copyable):
    """Tile/Entity texture class"""
    
    _cache = {}

    def __init__(self, name=None, id_=None, width=32, height=32):
        """Initializes a Texture instance

        Keyword Arguments:
            name {str} -- name of the texture (default: {None})
            id_ {int} -- texture id, for connected textures (default: {None})
        """

        self.name = name
        self.id = id_
        self.img = Texture.get(self.name, self.id) if name else None
        self.WIDTH = width
        self.HEIGHT = height
    
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
            path = Path("assets", "textures", name+".png")
            Texture._cache[name] = pygame.image.load(path)
        
        return Texture._cache[name]

    def render(self, surface, pos, tilesize, dimensions=Vec(1,1)):
        """Renders the texture

        Arguments:
            surface {pygame.Surface} -- surface to render the texture on
            pos {Vec} -- pixel coordinates where to render on the surface (bottom left corner)
            tilesize {int} -- size of a tile in pixels
            dimensions {Vec} -- dimensions of the texture (default: {Vec(1,1)})
        """
        
        width = self.img.get_width()/self.WIDTH
        height = self.img.get_height()/self.HEIGHT
        tw, th = tilesize*dimensions.x, tilesize*dimensions.y

        # dimensions is the size of the object in tiles
        img = pygame.transform.scale(self.img, (int(width*tw), int(height*th)))
        
        x, y = 0, 0
        if not self.id is None:
            x = (self.id % width) * tw
            y = (self.id // width) * th

        surface.blit(img, [pos.x, pos.y-th], [x, y, tw, th])