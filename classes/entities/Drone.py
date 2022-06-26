#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from math import copysign

from classes.Entity import Entity
from classes.Event import Event, listener, on
from classes.Vec import Vec

@listener
class Drone(Entity):
    """Drone which can be interacted with by the player

    Friendly drone which follows/unfollows the player when interacted with.
    Can be used to keep pressure plates activated.
    """
    
    _ENTITIES = {
        0: "drone",
        1: "drone_pig"
    }
    I18N_KEY = "drone"
    
    SIZE = Vec(0.7,0.7)

    gravity = True
    interactive = True
    speed = 3
    
    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False, world=None):
        super().__init__(pos, vel, acc, type_, highlight, world)
        self.following = False
        self.direction = 1
    
    def handle_events(self, events):
        """Handles events

        Actualizes velocity if following the player

        Arguments:
            events {list[pygame.Event]} -- list of pygame events
        """

        if self.following:
            player = self.world.player
            player_pos = player.pos + player.SIZE/2
            
            current_pos = self.pos + self.SIZE/2
            
            if player_pos.distance_to(current_pos) > 0.2:
                direction = (player_pos-current_pos).normalize()
                self.direction = copysign(1, direction.x)
                self.vel = direction * self.speed
            else:
                self.vel *= 0
    
    @on(Event.INTERACTION)
    def on_interract(self, event):
        if self in event.entities:
            self.update_following(not self.following)
            
    def update_following(self, following):
        """Update following state

        Arguments:
            following {bool} -- new following state
        """

        self.following = following
        if not self.following:
            self.vel = Vec()
            self.gravity = True
        else:
            self.gravity = False
        