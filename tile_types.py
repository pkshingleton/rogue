'''
Tiles are parts of the map that can be interacted with. They represent doors/pits/entrances, etc. 
- Additional tile properties can be added for other effects ('does_damage = bool', etc.)
- Tiles are generated with the 'procgen.py' module and passed to the GameMap class to be rendered by the engine.
'''


#_______________________________________________________________________// MODULES
from typing import Tuple
import numpy as np



#_______________________________________________________________________// DATA (TYPES)
# Structures the datatype for tile graphics (Using Numpy datatypes/dtype)

# This is for the "dark" property of the of the tile_datatype
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



#_______________________________________________________________________// FUNCTION
# Pass in values to return an array - renders as a tile on the game map
def new_tile(
    *,                          # Enforces keyword usage so parameter order doesn't matter
    walkable    : int,          # Can pass through (True/False)
    transparent : int,          # Display background color or not (True/False)
    dark        : Tuple[        # Symbol and color ("Graphic")
        int,                        #- Unicode character number
        Tuple[int, int, int],       #- Foreground RGB values
        Tuple[int, int, int]        #- Background RGB values
    ]
) -> np.ndarray:
    ''' Helper function for defining individual tile types '''
    return np.array((walkable, transparent, dark), dtype=tile_datatype)



#_______________________________________________________________________// VARIABLES (TUPLES)
# Colors for tiles (make this part of an external 'tile library')
white       = (255, 255, 255)   # Absolute white
dark_blue   = (50, 50, 150)
green       = (68, 97, 57)
dark_green  = (56, 69, 52)
light_tan   = (130, 110, 50)
brown       = (77, 72, 71)
dark_brown  = (59, 56, 56)
red         = (158, 75, 58)
light_gray  = (114, 114, 117)
gray        = (100, 100, 100)
dark_gray   = (62, 62, 62)
black       = (0 ,0, 0)         # Absolute black

# --> (TO-DO: Create a tool to set colors, pick a symbol, and save as new tile) <--



#_______________________________________________________________________// DATA (TUPLES) - TILES
# < walkable: true/false, transparent (no foreground): true/false, dark: unicode symbol, fg, bg > 

grass = new_tile(
    walkable        =True, 
    transparent     =True, 
    dark            =(ord("`"), green, dark_green),
)

dirt = new_tile(
    walkable        =True,
    transparent     =True,
    dark            =(ord("."), green, brown)
)

floor_wood = new_tile(
    walkable        =True, 
    transparent     =False, 
    dark            =(ord("="), brown, light_tan),
)

wall = new_tile(
    walkable        =False, 
    transparent     =False, 
    dark            =(ord(" "), (255, 255, 255), gray),
)


# TO ADD:
#-----------------
#   Tree (walkable IF {equipment[shoes]})
#   Mountain (walkable IF {equipment[rope]})
#   Entrance-building (trigger)
#   Entrance-dungeon  (trigger + load new map)  
#   Lava (trigger player damage)
#   Etc.