#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Entity import Entity
from math import copysign
from .Vec import Vec

class Player(Entity):
    """
    Player class, extends Entity. Holds player-specific information
    and manages interactions
    """

    SPEED = 3
    JUMP_SPEED = 7
    
    _entity = {
        0: "player"
    }
    
    def jump(self):
        """Makes the player jump if on the ground"""

        if self.on_ground:
            self.vel.y = self.JUMP_SPEED
    
    def move(self, direction):
        """Moves the player horizontally

        Arguments:
            direction {int} -- negative if moving left, positive if moving right
        """

        self.vel.x = copysign(self.SPEED, direction)