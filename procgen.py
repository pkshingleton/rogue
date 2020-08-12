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
from typing import Tuple

from game_map import GameMap
import tile_types



#_______________________________________________________________________// CLASSES
class RectangularRoom:

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



#_______________________________________________________________________// PRE-SET (STATIC) ROOMS 
room_A = RectangularRoom(x=20, y=15, width=10, height=15)
room_B = RectangularRoom(x=35, y=15, width=10, height=15)
room_C = RectangularRoom(x=5, y=5, width=10, height=10)



#_______________________________________________________________________// FUNCTION
# Defines a tile area and returns a 'GameMap' class instance 
# (a dungeon, forest, house, shop, etc.)

def generate_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    dungeon.tiles[room_A.inner] = tile_types.grass
    dungeon.tiles[room_B.inner] = tile_types.dirt

    return dungeon


# Creates a small room
def generate_house(map_width, map_height) -> GameMap:
    house = GameMap(map_width, map_height)

    house.tiles[room_C.inner] = tile_types.floor

    return house



# TO ADD:
#-----------------
#   Shop
#   Mansion (multiple rooms)
#   Forest maze
#   Marketplace (groups of shops)  
#   Etc. 