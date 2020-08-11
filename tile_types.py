'''
Tiles are parts of the map that can be interacted with. They represent doors/pits/entrances, etc. 
Some tiles can't be crossed (ie, walls) while others may do things like damage the player (fire, etc.)

Tiles are placed by the GameMap class and rendered (drawn) by the engine.
'''


#_______________________________________________________________________// MODULES
from typing import Tuple
import numpy as np



#_______________________________________________________________________// DATA (TYPES)
# Structure the datatype for tile graphics (Using Numpy datatypes/dtype)

# This is the 'graphical' representation of the tile. Currently uses Unicode letters (+, <, |, etc.)
graphic_datatype = np.dtype(
    [
        ("ch", np.int32),   # Unicode
        ("fg", "3B"),       # Reserves 3 unsigned bytes for setting foreground ('fg') RGB values
        ("bg", "3B"),       # Same thing for background ('bg') color
    ]
)


# Tile struct for statically defined tiles 
tile_datatype = np.dtype(
    [
        ("walkable", np.bool),      # True if this tile can be walked over.
        ("transparent", np.bool),   # True if this tile doesn't block FOV.
        ("dark", graphic_datatype), # Graphics for when this tile is not in FOV.
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



#_______________________________________________________________________// DATA (TUPLES)
# Common floor tile  (walkable, doesn't block view)
floor = new_tile(
    walkable      =True, 
    transparent   =True, 
    dark          =(ord(" "), (255, 255, 255), (50, 50, 150)),
)

# Wall tiles (can't walk over, blocks view)
wall = new_tile(
    walkable      =False, 
    transparent   =False, 
    dark          =(ord(" "), (255, 255, 2555), (0, 0, 100)),
)