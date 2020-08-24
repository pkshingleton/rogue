'''
Returns a 'map' object that contains tiles, sent to the console, and rendered.

The default-filled wall tiles are "dug out" by the 'procgen.py' module's dungeon generating functions.

'''


#_______________________________________________________________________// MODULES

from __future__ import annotations
from typing import (Iterable, Iterator, Optional, TYPE_CHECKING)

import numpy as np
from tcod.console import Console

from entity import Actor
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity



#_______________________________________________________________________// CLASS

class GameMap:
    '''
    Takes width/height values, and fills that area with default wall tiles. 
    Includes properties for 'visible' and 'explored' areas which are referenced in the .render() method to determine the tile states.  
    '''

    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()):
        '''
        Takes an Engine instance, values for width/height, and an entities instance. 
        Defines arrays for this map's tile types - 'visible' and/or 'explored'.
        '''
        self.engine = engine
        self.width, self.height = width, height
        # Creates a a Set of Entity class instances (passed in as an iterable object)
        self.entities = set(entities)
        # Fill area of given dimensions with default wall tiles. 
        self.tiles = np.full(
            (width, height), 
            fill_value=tile_types.wall, 
            order="F"
        )
        # Area of map with a 'visible' tiles ('Light' color mode and in player FOV)
        self.visible = np.full(
            (width, height), 
            fill_value=False, 
            order="F"
        )
        # Area of map with 'explored' tiles ('Dark' color mode and not in player FOV, but was visible at some point)
        self.explored = np.full(
            (width, height), 
            fill_value=False, 
            order="F"
        )


    @property
    def actors(self) -> Iterator[Actor]:
        '''
        Iterates over this maps living/alive actors and returns ('yields') any that are still alive. 
        '''
        yield from(
            entity 
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )


    def get_blocking_entity_at_location(self, location_x:int, location_y:int) -> Optional[Entity]:
        '''
        Iterates through map's entities set, finds one occupying the given location (and has "blocks_movement = True"), and returns it.
        '''
        for entity in self.entities:
            if (
                entity.blocks_movement 
                and entity.x == location_x 
                and entity.y == location_y
            ):
                # If an entity meets the criteria, return it
                return entity
        # If not, return an empty object.
        return None


    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        '''
        Return an Actor instance if the given location matches the actor's set coordinates (ie, actor is at given location)
        '''
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        # Otherwise return an empty object
        return None


    def in_bounds(self, x: int, y: int) -> bool:
        ''' 
        Check if something is inside the map's dimensions/area using given x/y and returns True or False.
        '''
        return 0 <= x < self.width and 0 <= y < self.height


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
        console.tiles_rgb[0: self.width, 0: self.height] = np.select(
            # Lists to determine tile appearance
            condlist    = [self.visible, self.explored],                
            choicelist  = [self.tiles["light"], self.tiles["dark"]],    
            default     = tile_types.SHROUD                             
        )

        # Determine in what order to render entities:
        entities_sorted_for_rendering = sorted(
            self.entities,                              # The Set of entities to sort
            key = lambda x: x.render_order.value        # A custom key for sorting by (using 'render_order' module)
        )

        # Iterate through entities and add one to the console if it exists in a 'visible' area of the map.
        for entities in entities_sorted_for_rendering:
            if self.visible[entity.x, entity.y]:
                console.print(
                    x = entity.x, y = entity.y, string = entity.char,  fg = entity.color
                )
    



    