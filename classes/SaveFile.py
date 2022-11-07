#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import struct

import numpy as np

from lib import staff
from classes.Chunk import Chunk
from classes.Entity import Entity
from classes.Logger import Logger
from classes.Tile import Tile
from classes.Vec import Vec

class SaveFile:
    SAVE_FORMAT = 3

    def __init__(self, path, world):
        self.path = path
        self.world = world
        self.handle = None
    
    def load(self):
        with open(self.path, "rb") as self.handle:
            self._load()
    
    def _load(self):
        f = self.handle
        save_format = struct.unpack(">I", f.read(4))[0]

        if save_format != self.SAVE_FORMAT:
            Logger.error("This level was not saved in the current format. It may not properly or crash the game.")
        
        Logger.info("Loading header")
        size_chunk_header = struct.unpack(">I", f.read(4))[0]
        size_palette = struct.unpack(">I", f.read(4))[0]
        size_entities = struct.unpack(">I", f.read(4))[0]

        nchunks = size_chunk_header // 8
        
        Logger.info("Loading chunk header")
        self.chunk_offsets = {}
        for i in range(nchunks):
            x = struct.unpack(">h", f.read(2))[0]
            y = struct.unpack(">h", f.read(2))[0]
            offset = struct.unpack(">I", f.read(4))[0]
            self.chunk_offsets[(x,y)] = offset
        
        Logger.info("Loading palette")
        palette = []
        while f.tell() < size_palette + size_chunk_header + 16:
            size = struct.unpack(">H", f.read(2))[0]
            type_ = struct.unpack(">H", f.read(2))[0]

            cls = b""

            while True:
                c = f.read(1)
                if c == b"\0": break
                cls += c

            attrs = staff.loads(f.read(size - len(cls) - 3))

            cls = str(cls, "utf-8")
            tile = Tile.get_cls(cls)(x, y, type_, self.world)
            for k, v in attrs.items():
                setattr(tile, k, v)
            
            palette.append(tile)
        
        Logger.info("Loading default ground tile")
        default_i = struct.unpack(">H", f.read(2))[0]
        self.world.default_ground_tile = palette[default_i]
        
        Logger.info("Loading chunks")
        self.world.chunks = {}
        for [cx, cy], offset in self.chunk_offsets.items():
            chunk = Chunk(cx, cy)
            
            n = struct.unpack(">I", b"\x00"+f.read(3))[0]
            ntiles = n & 0x1ff
            nground = (n >> 9) & 0x1ff
            
            for i in range(nground):
                id_ = struct.unpack(">H", f.read(2))[0]
                pos = struct.unpack("B", f.read(1))[0]
                x = pos >> 4
                y = pos & 0xf
                tile = palette[id_].copy()
                tile.pos.x = cx*16+x
                tile.pos.y = cy*16+y
                chunk.ground_tiles[y, x] = tile
            
            for i in range(ntiles):
                id_ = struct.unpack(">H", f.read(2))[0]
                pos = struct.unpack("B", f.read(1))[0]
                x = pos >> 4
                y = pos & 0xf
                tile = palette[id_].copy()
                tile.pos.x = cx*16+x
                tile.pos.y = cy*16+y
                chunk.tiles[y, x] = tile

            self.world.chunks[(cx, cy)] = chunk
        
        self.world.entities = []
        
        Logger.info("Loading entities")
        cur_pos = f.tell()
        while f.tell() < size_entities + cur_pos:
            size = struct.unpack(">H", f.read(2))[0]
            type_ = struct.unpack(">H", f.read(2))[0]
            x = struct.unpack(">f", f.read(4))[0]
            y = struct.unpack(">f", f.read(4))[0]

            cls = b""

            while True:
                c = f.read(1)
                if c == b"\0": break
                cls += c
            
            attrs = staff.loads(f.read(size - len(cls) - 11))

            cls = str(cls, "utf-8")
            entity = Entity.get_cls(cls)(pos=Vec(x,y), type_=type_)

            for k, v in attrs.items():
                setattr(entity, k, v)
            
            self.world.add_entity(entity)
            if cls == "Player":
                self.world.player = entity
    
    def save(self):
        with open(self.path, "wb") as self.handle:
            self.save_()
    
    def save_(self):
        f = self.handle
        
        buf_chunk_header = bytearray()
        buf_palette = bytearray()
        buf_entities = bytearray()
        buf_chunks = bytearray()
        
        palette = []
        
        default_tile = self.tile_to_dict(self.world.default_ground_tile)
        if default_tile in palette:
            default_i = palette.index(default_tile)
        else:
            default_i = len(palette)
            palette.append(default_tile)
        
        Logger.info("Saving chunks")
        for [cx, cy], chunk in self.world.chunks.items():
            buf_chunk_header.extend(struct.pack(">h", cx))
            buf_chunk_header.extend(struct.pack(">h", cy))
            buf_chunk_header.extend(struct.pack(">I", len(buf_chunks)))
            
            ground = list(chunk.ground_tiles[chunk.ground_tiles != np.array(None)])
            tiles = list(chunk.tiles[chunk.tiles != np.array(None)])
            
            nground, ntiles = len(ground), len(tiles)
            n = (nground << 9) | ntiles
            buf_chunks.extend(struct.pack(">I", n)[-3:])
            for tile in ground+tiles:
                t = self.tile_to_dict(tile)
                
                if t in palette:
                    i = palette.index(t)
                    
                else:
                    i = len(palette)
                    palette.append(t)
                
                x, y = tile.pos % 16
                pos = (x << 4) | y
                
                buf_chunks.extend(struct.pack(">H", i))
                buf_chunks.extend(struct.pack("B", pos))
        
        Logger.info("Saving palette")
        for tile in palette:
            buf_tile = bytearray()
            buf_tile.extend(struct.pack(">H", tile["type"]))
            buf_tile.extend(bytearray(tile["class"], "utf-8"))
            buf_tile.append(0)
            
            attrs = staff.dumps(tile["attrs"])
            buf_tile.extend(attrs)

            buf_palette.extend(struct.pack(">H", len(buf_tile)))
            buf_palette += buf_tile
        
        entities = self.world.entities

        Logger.info("Saving entities")
        for entity in entities:
            buf_entity = bytearray()
            buf_entity.extend(struct.pack(">H", entity.type))
            buf_entity.extend(struct.pack(">f", entity.pos.x))
            buf_entity.extend(struct.pack(">f", entity.pos.y))
            buf_entity.extend(bytearray(entity.__class__.__name__, "utf-8"))
            buf_entity.append(0)
            attrs = {}

            if hasattr(entity, "_save"):
                for a in entity._save:
                    if hasattr(entity, a):
                        attrs[a] = getattr(entity, a)
            
            attrs = staff.dumps(attrs)
            buf_entity.extend(attrs)

            buf_entities.extend(struct.pack(">H", len(buf_entity)))
            buf_entities += buf_entity
        
        Logger.info("Writing to file")

        f.write(struct.pack(">I", self.SAVE_FORMAT))
        f.write(struct.pack(">I", len(buf_chunk_header) ))
        f.write(struct.pack(">I", len(buf_palette) ))
        f.write(struct.pack(">I", len(buf_entities) ))
        f.write(buf_chunk_header)
        f.write(buf_palette)
        f.write(struct.pack(">H", default_i))
        f.write(buf_chunks)
        f.write(buf_entities)
    
    def tile_to_dict(self, tile):
        t = {
            "type": tile.type,
            "class": tile.__class__.__name__,
            "attrs": {}
        }
        
        if hasattr(tile, "_save"):
            for a in tile._save:
                if hasattr(tile, a):
                    # TODO: Remove later
                    if a != "neighbors" or tile.CONNECTED:
                        t["attrs"][a] = getattr(tile, a)
        
        return t