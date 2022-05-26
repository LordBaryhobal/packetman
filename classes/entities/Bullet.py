from classes.Entity import Entity
from classes.Vec import Vec


class Bullet(Entity):
    """
        simple bullet object that moves in a straight line
    """
    
    GRAVITY = False
    
    _entity = {
        0: "bullet"
        
    }
    SIZE = Vec(0.2,0.2)