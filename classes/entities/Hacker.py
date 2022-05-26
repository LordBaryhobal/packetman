import pygame
from classes.Entity import Entity
from classes.Vec import Vec
from .Bullet import Bullet
from time import time

class Hacker(Entity):
    
    _entity = {
        0:"hacker"
    }
    
    SIZE = Vec(1,1)
    
    RELOAD_TIME = 1
    BULLET_SPEED = 10
    
    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False):
        super().__init__(pos, vel, acc, type_, highlight)
        self.lastbulletshot = time()
    
    def handle_events(self, events):
        if time() - self.lastbulletshot > self.RELOAD_TIME:
            self.lastbulletshot = time()
            self.shoot()
        
    def shoot(self):
        player = self.world.player
        player_pos = player.pos + player.SIZE/2
        bullet_pos = self.pos + self.SIZE/2
        bullet_vel = (player_pos - bullet_pos).normalize() * self.BULLET_SPEED
        self.world.add_entity(Bullet(bullet_pos, bullet_vel))
    
    