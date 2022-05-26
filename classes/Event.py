#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

listeners = {}

def listener(type_):
    """Decorator to create an event listener

    Arguments:
        type_ {int} -- Type of event to listen

    Returns:
        func -- decorator
    """
    
    global listeners
    
    if not type_ in listeners.keys():
        listeners[type_] = []
    
    def deco(func):
        global listeners
        
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        
        listeners[type_].append(wrapper)
        
        return wrapper
    return deco

class Event:
    """
    Event class for managing physical and graphical events such as
    collisions or user interactions
    """

    NONE = 0
    COLLISION_WORLD = 1
    COLLISION_ENTITY = 2
    ANIMATION_FINISH = 3
    CAMERA_MOVE = 4

    def __init__(self, type_):
        """Initializes an Event instance

        Arguments:
            type_ {int} -- event type
        """
        
        self.type = type_
    
    def dispatch(self):
        """Dispatches this event to potential event listeners"""

        if self.type in listeners.keys():
            for f in listeners[self.type]:
                f(self)