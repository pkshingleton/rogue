'''
Lays out the tiles, which are imported from 'tile_types.py'
Returns a 'map' object that contains the placed tiles and parameters for how the player interacts with them.

Use this class to create different variations of tile collections (aka "level maps"). 
The player can visit different maps with event triggers. Add the level maps to a set to create a "world".
'''


#_______________________________________________________________________// MODULES
import numpy as np
from tcod.console import Console

import tile_types



#_______________________________________________________________________// CLASS
class GameMap:

    # Initialize
    # (Expects width and height integers to determine how many tiles to place)
    def __init__(self, width: int, height: int):
        # Map dimensions
        self.width, self.height = width, height
        # Fill area
        self.tiles = np.full((width, height), fill_value=tile_types.grass, order="F")
        # Misc tiles 
        self.tiles[30:33, 40] = tile_types.wall
        self.tiles[25:35, 20] = tile_types.dirt                                          


    # Takes an x/y position and checks if it's within the boundaries of the map (true/false)
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height


    # Sends tiles to the console to be drawn (rendered)
    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
    

    