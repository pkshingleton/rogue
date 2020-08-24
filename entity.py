'''
An 'entity' is any object that populates the game (AKA, the content).
The 'Entity' class takes an x/y position, it's graphic/symbol, and color

Method:
    Entity.move(): Updates entity's x/y position with a new set of coordinates (called after a successful 'move' action)

'''


#_______________________________________________________________________// MODULES

from __future__ import annotations
import copy
from typing import (Optional, Tuple, Type, TypeVar, TYPE_CHECKING)

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.fighter import Fighter
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
            # If this entity has a GameMap associated with it:
            if hasattr(self, "gamemap"):
                self.gamemap.entites.remove(self)

            self.gamemap = gamemap
            gamemap.entities.add(self)


    #_____/ METHOD / .move(dx, dy)
    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy



class Actor(Entity):
    '''
    Inherits all the properties/attributes/methods of the 'Entity' class.
    '''
    
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI],
        fighter: Fighter
    ):

        # Calls the super class '__init__()' function (ie, the parent class / 'Entity' class __init__)
        super().__init__(
            x = x, 
            y = y,
            char = char,
            color = color, 
            name = name, 
            blocks_movement = True      # Always pass in 'True' (since all "actors" will block movement)
        )

        # Assign components (each actor needs the ability to move around and deal/take damage)
        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.entity = self


    @property
    def is_alive(self) -> bool:
        ''' 
        Returns 'True' as long as this actor has an 'ai'. 
        - If the entity's '.die()' method gets called, its 'ai' is replaced with 'None', effectively removing its capacity to perform actions.
        - Calling 'die(). on this entity will also set this property to return 'False'.
        '''
        return bool(self.ai)