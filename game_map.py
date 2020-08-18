'''
Returns a 'map' object that contains tiles, sent to the console, and rendered.

The default-filled wall tiles are "dug out" by the 'procgen.py' module's dungeon generating functions.

'''


#_______________________________________________________________________// MODULES

from __future__ import annotations
from typing import (Iterable, Optional, TYPE_CHECKING)

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


    #_____/ METHOD / .get_blocking_enemy_at_location(x, y)
    def get_blocking_entity_at_location(self, location_x:int, location_y:int) -> Optional[Entity]:
        # Iterate through all entities to find one occupying the given location AND has "blocks_movement = True"
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                # If an entity meets the criteria, return it
                return entity
        return None


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
        Sets tiles and entities to the map. 
        
        - If the tile is in the "visible" array, draw it with the 'light' color.
        - If it isn't, but it's been 'explored', draw it with the 'dark' color.
        - If tile is unexplored, default to "SHROUD".

        Tiles are sorted into Lists:
            - 'condlist': Tiles can be both visible AND explored, so they make up a parent list of conditional states.
            - 'choicelist': Tiles in either of the two color states (sorted depending on FOV calculations).
            - 'default': Any tiles not in the above lists are effectively unexplored. They will render as 'SHROUD' 
        '''
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            # Lists to determine tile appearance
            condlist    = [self.visible, self.explored],                
            choicelist  = [self.tiles["light"], self.tiles["dark"]],    
            default     = tile_types.SHROUD                             
        )
        # Iterate through the Set of entities and add each one to the console if it exists in a 'visible' area of the map.
        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(
                    x       = entity.x, 
                    y       = entity.y, 
                    string  = entity.char, 
                    fg      = entity.color
                )
    



    