'''
An 'entity' is any object that populates the game (AKA, the content).
The 'Entity' class takes an x/y position, it's graphic/symbol, and color

Method:
    Entity.move(): Updates entity's x/y position with a new set of coordinates (called after a successful 'move' action)

'''


#_______________________________________________________________________// MODULES

from __future__ import annotations
import copy
from typing import (Optional, Tuple, TypeVar, TYPE_CHECKING)

if TYPE_CHECKING:
    from game_map import GameMap



#_______________________________________________________________________// DECLARATION

# The 'Troll' enemy
T = TypeVar("T", bound="Entity")



#_______________________________________________________________________// CLASSES

# The generic object that represents players, enemies, items, etc.
class Entity:

    # Initialization
    def __init__(
        # Set initial values
        self, 
        gamemap: Optional[GameMap] = None,
        x: int = 0,                                     # x/y   - entity's position
        y: int = 0,     
        char: str = "?",                                # char  - its symbol/sprite
        color: Tuple[int, int, int] = (255, 255, 255),  # color - an RGB color value
        name: str = "<Unnamed>",                        # name  - references the entity
        blocks_movement: bool = False,                  # Walkable or not (enemies aren't, items and NPCs are)
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

        if gamemap:
            # If a gamemap isn't provided now then it will be set later.
            self.gamemap = gamemap
            gamemap.entities.add(self)


    #_____/ METHOD / .spawn(self, gamemap, x, y)
    def spawn(self: T, gamemap: GameMap, x: int, y:int) -> T:
        ''' 
        Spawns a copy of this entity instance at a given location. 
        '''
        clone = copy.deepcopy(self)

        clone.x = x
        clone.y = y

        clone.gamemap = gamemap
        gamemap.entities.add(clone)

        return clone

    
    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        ''' Place this entity at a new location (handles moving between GameMaps). '''
        self.x = x
        self.y = y

        if gamemap:

            if hasattr(self, "gamemap"):    # Possibly hasn't been initialized
                self.gamemap.entites.remove(self)

            self.gamemap = gamemap
            
            gamemap.entities.add(self)


    #_____/ METHOD / .move(dx, dy)
    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy
