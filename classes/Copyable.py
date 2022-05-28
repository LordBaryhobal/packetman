#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

class Copyable:
    """Abstract class to make subclass copyable

    Any subclass of this class will have a copy() function to create deepcopies
    of existing instances, keeping the class and copying its properties
    recursively if possible
    """

    __no_copy__ = []

    def copy(self):
        """Creates a new copy of this object. Keeps class and all properties
        
        Any property listed in self.__no_copy__ will not be copied

        Returns:
            object -- deepcopy of this instance
        """

        cls = self.__class__
        new = cls()
        for k,v in self.__dict__.items():
            if not k in self.__no_copy__:
                if hasattr(v, "copy"):
                    v = v.copy()
                setattr(new, k, v)
        
        return new