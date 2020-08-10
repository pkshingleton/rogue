'''
Lays out the tiles, which are imported from 'tile_types.py'
Returns a 'map' object that contains the placed tiles and parameters for how the player interacts with them.
'''


#_______________________________________________________________________// MODULES
import numpy as np
from tcod.console import Console

import tile_types



#_______________________________________________________________________// CLASS
class GameMap:

    # Initialize
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")

        self.tiles[30:33, 22] = tile_types.wall


    # Determine map dimensions and tile-fill area
    def in_bounds(self, x: int, y: int) -> bool:
        # Returns true if x and y are withing bounds of the map
        return 0 <= x < self.width and 0 <= y < self.height


    # Place the tiles
    def render(self, console: Console) -> None:
        console.tiles_rgb[0: self.width, 0: self.height] = self.tiles["dark"]
        