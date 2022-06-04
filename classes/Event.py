#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

listener_classes = {}

def on(type_):
    """Decorator to create an event listener callback

    Arguments:
        type_ {int} -- Type of event to listen

    Returns:
        func -- decorator
    """
    
    def deco(func):
        func._is_listener = True
        func._listener_type = type_
        
        return func
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
    INTERACTION = 5
    ENTER_TILE = 6
    EXIT_TILE = 7
    WORLD_SAVED = 8
    WORLD_LOADED = 9
    CIRCUIT_CHANGE = 10
    GATE_INPUT = 11
    

    def __init__(self, type_):
        """Initializes an Event instance

        Arguments:
            type_ {int} -- event type
        """
        
        self.type = type_
    
    def dispatch(self):
        """Dispatches this event to potential event listeners"""

        if self.type in listener_classes.keys():
            for cls in listener_classes[self.type]:  # for all classes with a listener function for this type
                for f in cls._listeners[self.type]:  # for all listeners for this type
                    for i in cls._instances:         # for all instances of this class
                        f(i, self)
    
    def __repr__(self):
        return f"Event({self.type})"


def listener(cls):
    """Class decorator to indicate that a class has event listener callback methods

    Returns:
        class -- the class
    """
    
    cls._listeners = {}
    cls._instances = []

    for k,v in cls.__dict__.items():
        if hasattr(v, "_is_listener") and v._is_listener:
            type_ = v._listener_type

            if not type_ in cls._listeners.keys():
                cls._listeners[type_] = []
            
            if not type_ in listener_classes.keys():
                listener_classes[type_] = []
            
            if not cls in listener_classes[type_]:
                listener_classes[type_].append(cls)
            
            cls._listeners[type_].append(v)
    
    old_init = cls.__init__
    def init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        cls._instances.append(self)
    cls.__init__ = init
    
    old_del = cls.__del__ if hasattr(cls, "__del__") else lambda *a, **kwa: None
    def del_(self, *args, **kwargs):
        old_del(self, *args, **kwargs)
        if self in cls._instances:
            cls._instances.remove(self)
    cls.__del__ = del_

    return cls