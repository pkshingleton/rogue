'''
An 'entity' is any object that populates the game (AKA, the content).
This module defines how the entity fits into the world and what sub-classes it spawns.  
'''



#_______________________________________________________________________// MODULES
from typing import Tuple



#_______________________________________________________________________// CLASS
# The generic object that represents players, enemies, items, etc.
class Entity:

    # Initialization
    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        # x/y - entity's position
        # char - its symbol/sprite
        # color - an RGB color value
        self.x = x
        self.y = y
        self.char = char
        self.color = color


    # How the entity moves
    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy
