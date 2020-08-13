'''
Returns a 'map' object that contains tiles, sent to the console, and rendered.

The default-filled wall tiles are "dug out" by the 'procgen.py' module's dungeon generating functions.

'''


#_______________________________________________________________________// MODULES
import numpy as np
from tcod.console import Console

import tile_types



#_______________________________________________________________________// CLASS
class GameMap:
    ''' Takes width and height values and fills the area with wall tiles. '''

    # Initialize
    def __init__(self, width: int, height: int):
        # Map dimensions
        self.width, self.height = width, height
        # Fill area
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
                                              

    #_____/ METHOD / .in_bounds(x, y)
    # Takes an x/y position and checks if it's within the boundaries of the map (true/false)
    def in_bounds(self, x: int, y: int) -> bool:
        ''' Check if something is inside the map's area '''
        return 0 <= x < self.width and 0 <= y < self.height


    #_____/ METHOD / .render(console)
    # Sends tiles to the console to be drawn (rendered)
    def render(self, console: Console) -> None:
        ''' Renders itself apart from the main console. Gets called in the Engine.render() method. '''
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
    

    