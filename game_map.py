'''
Returns a 'map' object that contains tiles, sent to the console, and rendered.

Takes desired dimensions and fills an area with 'wall' tiles. 
A separate module ('procgen.py') replaces some wall areas with other tiles, and returns a contained "room".  

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
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
                                              

    #_____/ METHOD / .in_bounds(x, y)
    # Takes an x/y position and checks if it's within the boundaries of the map (true/false)
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height


    #_____/ METHOD / .render(console)
    # Sends tiles to the console to be drawn (rendered)
    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
    

    