#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Event import Event, listener, on
from classes.tiles.Components import *
from classes.Vec import Vec

@listener
class Circuit:
    """class to manage how to power propagates trough the world"""
    
    def __init__(self, world):
        self.world = world
    
    @on(Event.CIRCUIT_CHANGE)
    def on_circuit_change(self, event):
        """Updates circuit when circuit change event is triggered"""
        self.current_circuit = set()
        self.input = event.input
        # events.tiles are tuple containing the tiles and the direction from where they are connected
        for tile in event.tiles:
            self.power_tiles(tile[1], tile[0], power=event.power)
    
    def power_tiles(self, tile, connected_from, power=True):
        """Powers tile and propagates power to connected tiles
        
        Arguments:
            tile {Tile} -- tile to power
            connected_from {int} -- direction from where the tile is connected(0-3)
        
        Keyword Arguments:
            power {bool} -- power state
        """
        if not tile:
            return
        if tile in self.current_circuit:
            return
        self.current_circuit.add(tile)
        
        if isinstance(tile, Output):
            event = Event(event.GATE_INPUT)
            event.tile = tile
            event.power = power
            event.input = self.input
            event.connected_from = (connected_from+2)%2
            self.world.game.events.append(event)
            return

        if isinstance(tile, Input):
            return
            
        if power:
            tile.powered_by.append(self.input)
        else:
            tile.powered_by.remove(self.input)
        tile.update_power()

        
        if tile.neighbors & 1:
            self.power_tiles(self.world.get_tile(tile.pos + Vec(0,1)), 0, power)
        
        if tile.neighbors & 2:
            self.power_tiles(self.world.get_tile(tile.pos + Vec(1,0)), 1, power)
        
        if tile.neighbors & 4:
            self.power_tiles(self.world.get_tile(tile.pos + Vec(0,-1)), 2, power)
        
        if tile.neighbors & 8:
            self.power_tiles(self.world.get_tile(tile.pos + Vec(-1,0)), 3, power)