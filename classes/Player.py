#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from Entity import Entity

class Player(Entity):
    """
    Player class, extends Entity. Holds player-specific information
    and manages interactions
    """

    def __init__(self):
        super().__init__()