# type: ignore

class Tile:
    

class Chunk:
    x = ...
    y = ...
    tiles_floor = np.array([
        [None, None, Tile, Tile, None],
        [Tile, None, None, Tile, None],
        [Tile, Tile, Tile, None, None],
        ...
    ])
    tiles = np.array([
        [None, None, Tile, Tile, None],
        [Tile, None, None, Tile, None],
        [Tile, Tile, Tile, None, None],
        ...
    ])

    def get_tiles_in_rect(self, topleft, bottomright)
    def render()

class World:
    chunks = {
        (2,5): Chunk,
        (6,3): Chunk,
    }

    def get_tile(self, pos):
        chunk = get_chunk()
        return chunk.get_tile(rel_pos)

    def set_tile(self, pos):
        chunk = get_chunk()
        chunk.set_tile(rel_pos)
    
    def get_tiles_in_rect(self, topleft, bottomright):
        chunks = get_chunk_in_rect()
        tiles = []
        rect = Rect(topleft, bottomright)
        for chunk in chunks:
            tiles += chunk.get_tiles_in_rect(rect.overlap(chunk.rect))
        return tiles