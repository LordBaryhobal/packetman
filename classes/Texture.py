#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

class Texture:
    _cache = {}

    WIDTH, HEIGHT = 32, 32

    def __init__(self, name, id_=None):
        """Initializes a Texture instance

        Arguments:
            name {str} -- name of the texture

        Keyword Arguments:
            id_ {int} -- texture id, for connected textures (default: {None})
        """

        self.name = name
        self.id = id_
        self.img = Texture.get(self.name, self.id)
    
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
            Texture._cache[name] = pygame.image.load(f"./assets/textures/{name}.png")
        
        return Texture._cache[name]

    def render(self, surface, pos, size):
        """Renders the texture

        Arguments:
            surface {pygame.Surface} -- surface to render the texture on
            pos {Vec} -- pixel coordinates where to render on the surface
            size {int} -- size of a tile in pixels
        """
        
        if self.id is None:
            img = pygame.transform.scale(self.img, (size, size))
        else:
            img = pygame.transform.scale(self.img, (int(size*4), int(size*4)))
        
        x, y = 0, 0
        if not self.id is None:
            x = (self.id%4)*size
            y = (self.id//4)*size

        surface.blit(img, [pos.x, pos.y-size], [x, y, size, size])
        #surface.blit(img, [pos.x, pos.y])