'''
An 'entity' is any object that populates the game (AKA, the content).
The 'Entity' class takes an x/y position, it's graphic/symbol, and color

Method:
    move(): Updates entity's x/y position with a new coordinates.
    
'''


#_______________________________________________________________________// MODULES
from typing import Tuple



#_______________________________________________________________________// CLASSES
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


    #_____/ METHOD / .move(dx, dy)
    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy
