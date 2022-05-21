#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

class Event:
    """
    Event class for managing physical and graphical events such as
    collisions or user interactions
    """

    NONE = 0

    def __init__(self, type_):
        """Initializes an Event instance

        Arguments:
            type_ {int} -- event type
        """
        
        self.type = type_