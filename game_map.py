'''
Returns a 'map' object that contains tiles, sent to the console, and rendered.

The default-filled wall tiles are "dug out" by the 'procgen.py' module's dungeon generating functions.

'''


#_______________________________________________________________________// MODULES
from __future__ import annotations
from typing import (Iterable, TYPE_CHECKING)
import numpy as np
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entity import Entity

#_______________________________________________________________________// CLASS
class GameMap:
    '''
    Takes width/height values, and fills that area with default wall tiles. 
    Includes properties for 'visible' and 'explored' areas which are referenced in the .render() method to determine the tile states.  
    '''

    # Initialize
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        # Map dimensions
        self.width, self.height = width, height
        # Creates a a Set of Entity class instances (passed in as an iterable object)
        self.entities = set(entities)
        # Fill area with wall tiles by default. 
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        # Different states the tiles can be rendered in
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")
                                              

    #_____/ METHOD / .in_bounds(x, y)
    # Takes an x/y position and checks if it's within the boundaries of the map (true/false)
    def in_bounds(self, x: int, y: int) -> bool:
        ''' 
        Check if something is inside the map's area 
        '''
        return 0 <= x < self.width and 0 <= y < self.height


    #_____/ METHOD / .render(console)
    # Sends tiles to the console to be drawn (rendered)
    def render(self, console: Console) -> None:
        ''' 
        Renders the map (apart from everything else in the main console, like entities). 
        
        If the tile is in the "visible" array, draw it with the 'light' color.
        If it isn't, but it's been 'explored', draw it with the 'dark' color.
        If tile is unexplored, default to "SHROUD".
        '''
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist = [self.visible, self.explored],
            choicelist = [self.tiles["light"], self.tiles["dark"]],
            default = tile_types.SHROUD
        )
        # Iterate through the entities set and set each one to the console state.
        # (Entities will only be set if the map area they're supposed to be contains 'visible' tiles.)
        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(
                    x       = entity.x, 
                    y       = entity.y, 
                    string  = entity.char, 
                    fg      = entity.color
                )
    

    