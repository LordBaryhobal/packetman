#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from time import time

class Animation:
    """Class used to animate attribute values of a particular object.
    
    Examples of use:
    - camera movement
    - color transition
    - tile movements
    """

    FLOAT = 0
    INT = 1

    FORWARDS = 0
    ALTERNATE = 1

    ANIMATIONS = []

    def __init__(self, obj, attr_, val_a, val_b, duration, start=True, loop=None, type_=FLOAT):
        """Initializes an Animation instance

        Arguments:
            obj {object} -- object to animate
            attr_ {str} -- name of the attribute to animate
            val_a {float} -- value at the start of the animation
            val_b {float} -- value at the end of the animation
            duration {float} -- duration in seconds of the animation

        Keyword Arguments:
            start {bool} -- True if animation should start automatically (default: {True})
            loop {int} -- type of looping (default: {None})
                          One of: None, Animation.FORWARDS, Animation.ALTERNATE
            type_ {int} -- type of the animated value (default: {FLOAT})
                           One of: Animation.FLOAT, Animation.INT
        """

        self.obj = obj
        self.attr = attr_
        self.val_a = val_a
        self.val_b = val_b
        self.duration = duration
        self.loop = loop
        self.type = type_
        self.start_time = None
        self.pause_time = None
        self.finished = False

        if start:
            self.start()
        
        Animation.ANIMATIONS.append(self)
    
    def start(self):
        """Starts the animation.

        Returns:
            bool -- True if successful, False otherwise
        """

        if self.start_time is None:
            self.finished = False
            self.start_time = time()
            return True
        
        return False
    
    def update(self): 
        """Updates the value at the current time

        Stops the animation if completed
        """

        t = time()
        ratio = (t-self.start_time)/self.duration

        if ratio > 1:
            if self.loop is None:
                self.finished = True
                ratio = 1
            
            elif self.loop == Animation.FORWARDS:
                ratio %= 1
            
            elif self.loop == Animation.ALTERNATE:
                ratio = 1 - abs((ratio%2) - 1)
        
        val = ratio

        if self.type == Animation.FLOAT:
            val = ratio*(self.val_b - self.val_a) + self.val_a

        elif self.type == Animation.INT:
            val = int( ratio*(self.val_b - self.val_a) + self.val_a)
        
        setattr(self.obj, self.attr, val)

    def pause_all():
        for anim in Animation.ANIMATIONS:
            anim.pause_time = time()
    
    def resume_all():
        t = time()
        for anim in Animation.ANIMATIONS:
            if anim.start_time and anim.pause_time:
                anim.start_time += t-anim.pause_time
            
            anim.pause_time = None