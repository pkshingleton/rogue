'''
Tiles are parts of the map that can be interacted with. They represent doors/pits/entrances, etc. 
Some tiles can't be crossed (ie, walls) while others may do things like damage the player (fire, etc.)

Tiles are placed by the GameMap class and rendered (drawn) by the engine.
'''


#_______________________________________________________________________// MODULES
from typing import Tuple
import numpy as np



#_______________________________________________________________________// DATA (TYPES)
# Structures the datatype for tile graphics (Using Numpy datatypes/dtype)

# This is the 'graphical' representation of the tile. Currently uses Unicode letters (+, <, |, etc.)
graphic_symbol = np.dtype(
    [
        ("ch", np.int32),   # Unicode / symbol for tile
        ("fg", "3B"),       # Reserves 3 unsigned bytes for setting foreground ('fg') RGB values
        ("bg", "3B"),       # Same thing for background ('bg') RGB color
    ]
)


# Tile struct for statically defined tiles 
tile_datatype = np.dtype(
    [
        ("walkable",    np.bool),           # True if this tile can be walked over.
        ("transparent", np.bool),           # True if this tile doesn't block FOV.
        ("dark",        graphic_symbol),    # Symbol, foreground color, background color
    ]
)



#_____________// FUNCTION / CREATE NEW TILE
''' Helper function for defining individual tile types '''
def new_tile(
    *,          # Enforces keyword usage so parameter order doesn't matter
    walkable    : int, 
    transparent : int,
    dark        : Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
    
    return np.array((walkable, transparent, dark), dtype=tile_datatype)


#_______________________________________________________________________// COLOR (TUPLES) / RGB
red         = (158, 75, 58)
brown       = (77, 72, 71)
white       = (255, 255, 255)
light_gray  = (114, 114, 117)
dark_gray   = (62, 62, 62)
black       = (0 ,0, 0)
dark_brown  = (59, 56, 56)
green       = (68, 97, 57)
dark_green  = (56, 69, 52)


#_______________________________________________________________________// DATA (TUPLES) / TILE TYPES
# < walkable: true/false, transparent (no foreground): true/false, dark: unicode symbol, fg, bg > 

grass = new_tile(
    walkable        =True, 
    transparent     =False, 
    dark            =(ord("`"), green, dark_green),
)

dirt = new_tile(
    walkable        =True,
    transparent     =True,
    dark            =(ord("."), green, brown)
)

wall = new_tile(
    walkable        =False, 
    transparent     =False, 
    dark            =(ord(" "), (255, 255, 255), light_gray),
)

#---> EX: New types to add
#
#   Tree (walkable IF {equipment[shoes]})
#   Mountain (walkable IF {equipment[rope]})
#   Entrance-building (trigger)
#   Entrance-dungeon  (trigger + load new map)  
#   Lava (trigger player damage)
#   