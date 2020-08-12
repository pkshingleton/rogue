'''
Procedural generation builds tiled areas for the engine to render on the game map.

The class takes starting and ending coordinates and defines a "room" area for tiles to be placed on a map. 

Methods:
    center(): return a centered x/y position of a given area
    inner(x, y, width, height): returns two x/y pairs (start and end coordinates), aka an area. 

Function:
    generate_dungeon(map_width, map_height): takes game map size and places an area of tiles inside it.

'''


#_______________________________________________________________________// MODULES
from typing import (Iterator, Tuple)
import random
import tcod

from game_map import GameMap
import tile_types



#_______________________________________________________________________// CLASSES
class RectangularRoom:

    # Initialization
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    
    @property
    def inner(self) -> Tuple[slice, slice]:
        ''' Returns inner area of this room as a 2D array index '''
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)



#_______________________________________________________________________// PRE-SET ROOMS
# (start x, start y, tiles wide, tiles tall)
ROOM_SM     = RectangularRoom(x=10, y=10, width=10, height=10)
ROOM_MD     = RectangularRoom(x=40, y=15, width=20, height=20)
ROOM_LG     = RectangularRoom(x=20, y=5, width=30, height=25)



#_______________________________________________________________________// FUNCTIONS

#_____/ CONNECTS ROOMS /_____
# Takes a point on the first room (start) x/y, and second room (end). Returns x/y values for every point between.
def tunnel_between(start: Tuple[int, int], end: Tuple [int, int]) -> Iterator[Tuple[int, int]]:
    ''' Return an L-shaped tunnel between two points '''
    x1, y1 = start
    x2, y2 = end
    
    # Randomly set where the 'L-bend' appears (50% chance)
    if random.random() < 0.5:   
        # Horizontally, then vertically
        corner_x, corner_y = x2, y1
    else:
        # Vertically, then horizontally
        corner_x, corner_y = x1, y2

    # Generate coordinates for the tunnel as a list. 
    # (uses 'yield' to remember previous list values rather than recalculate each iteration - more CPU efficient)
    for x, y, in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y, in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


#_____/ BUILDS ROOMS /_____
# Defines two separate tile areas (returns a 'GameMap' class instance) 
def generate_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    # Use 'inner()' method to get area of a room and set the tile type to fill it with
    dungeon.tiles[ROOM_SM.inner] = tile_types.grass
    dungeon.tiles[ROOM_MD.inner] = tile_types.dirt
    dungeon.tiles[ROOM_LG.inner] = tile_types.grass

    # Take given points (from room center) and use [x/y] lists from 'tunnel_between' function to connect them.
    for x, y in tunnel_between(ROOM_SM.center, ROOM_LG.center):
        dungeon.tiles[x, y] = tile_types.dirt

    return dungeon


# Creates a small room
def generate_house(map_width, map_height) -> GameMap:
    house = GameMap(map_width, map_height)

    house.tiles[ROOM_LG.inner] = tile_types.floor_wood

    return house


# --> (TO-DO: Make a separate point/click tool for building rooms) <--

# TO ADD:
#-----------------
#   Shop
#   Mansion (multiple rooms)
#   Forest maze
#   Marketplace (groups of shops)  
#   Etc. 