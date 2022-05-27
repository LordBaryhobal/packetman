#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Logger import Logger

def import_class(dct, cls):
    """Imports a class from a dict of registered classes

    Arguments:
        dct {dict} -- dictionary of registered classes: {[class]: [module path]}

    Raises:
        KeyError: if the class isn't registered in `dct`

    Returns:
        class -- imported class
    """

    if not cls in dct:
        Logger.error(f"Class {cls} not found")
        raise KeyError(f"Class {cls} not found")
    
    components = dct[cls].split(".")
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    
    return getattr(mod, cls)

