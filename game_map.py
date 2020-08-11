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

        self.width            = width,
        self.height           = height,
        self.tiles            = np.full((width, height), fill_value=tile_types.floor, order="F")    # Fills map with floor tiles
        self.tiles[30:33, 22] = tile_types.wall                                                     # Set some of the tiles to wall tiles


    # Determine map dimensions and tile-fill area
    def in_bounds(self, x: int, y: int) -> bool:
        # Returns true if x and y are withing bounds of the map
        return 0 <= x < self.width and 0 <= y < self.height


    # Sends tiles to the console to be drawn (rendered) and sets them to start as 'dark' (out of view) until they're explored
    def render(self, console: Console) -> None:
        console.tiles_rgb[0: self.width, 0: self.height] = self.tiles["dark"]
        