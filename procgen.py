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

from __future__ import annotations
from typing import (Iterator, Tuple, List, TYPE_CHECKING)
import random
import tcod

import entity_factories
from game_map import GameMap
import tile_types

# Conditional module
if TYPE_CHECKING:
    from entity import Entity



#_______________________________________________________________________// CLASSES

class RectangularRoom:
    ''' 
    Defines an area on a map to be filled with tiles. 
    ''' 

    # Initialization
    def __init__(self, x: int, y: int, width: int, height: int):
        # Top-left corner point
        self.x1 = x
        self.y1 = y
        # Bottom-right corner point
        self.x2 = x + width
        self.y2 = y + height

    
    @property
    def center(self) -> Tuple[int, int]:
        ''' 
        Returns the center location of this room as a Tuple (x, y). 
        '''
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    
    @property
    def inner(self) -> Tuple[slice, slice]:
        ''' 
        Returns inner area of this room as a 2D array index (a set of two coordinates) [(x1 + 1, x2), (y1 + 1, y2)] 
        '''
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)


    #_____/ METHOD / .intersects(RectangularRoom)
    def intersects(self, other: RectangularRoom) -> bool:
        '''
        Pass in another 'RectangularRoom' instance and returns 'True' if this room overlaps it 
        '''
        # Evaluate an expression to determine if 'True' or 'False' will be returned
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )



#_______________________________________________________________________// FUNCTIONS

def place_entities(
    room:           RectangularRoom,
    dungeon:        GameMap,
    max_enemies:    int
) -> None:
    '''
    Takes a room, a map, and total enemies allowed per room, then sets a random number of enemies down in the given room.
    '''
    # Take the most enemies allowed in one room at a time and set a random number of them
    number_of_enemies = random.randint(0, max_enemies)

    for i in range(number_of_enemies):
        # Give the enemy random starting coordinates
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        # Check for any other enemies at that coordinate location (prevents getting a stack of enemies)
        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                # 80% chance of spawning an Orc
                entity_factories.orc.spawn(dungeon, x, y)
            else:
                # 20% chance of spawning a Troll
                entity_factories.troll.spawn(dungeon, x, y)



def tunnel_between(start: Tuple[int, int], end: Tuple [int, int]) -> Iterator[Tuple[int, int]]:
    ''' 
    Return a List of coordinates (making an L-shaped "tunnel") between two given points. 
    '''
    x1, y1 = start
    x2, y2 = end
    
    # Randomly set where the 'L-bend' appears (50% chance)
    if random.random() < 0.5:   
        # Horizontally, then vertically
        corner_x, corner_y = x2, y1
    else:
        # Vertically, then horizontally
        corner_x, corner_y = x1, y2

    # Generate coordinates for the tunnel tiles as a [List] 
    # (uses 'yield' to remember previous list values rather than recalculate on each iteration - more CPU efficient)
    for x, y, in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y, in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y



def generate_static_dungeon(map_width, map_height, variation) -> GameMap:
    ''' 
    Generates a static pre-set dungeon map. Takes desired size and type. 
    '''
    # Rooms in the dungeon (as GameMap instances)
    dungeon = GameMap(map_width, map_height)
    house = GameMap(map_width, map_height)
    # Some pre-made rooms 
    ROOM_SM = RectangularRoom(x=10, y=15, width=10, height=10)
    ROOM_MD = RectangularRoom(x=25, y=15, width=20, height=20)
    ROOM_LG = RectangularRoom(x=20, y=5, width=30, height=25)

    # Use 'inner()' method to get area of a room and set the tile type to fill it with
    dungeon.tiles[ROOM_SM.inner] = tile_types.grass
    dungeon.tiles[ROOM_MD.inner] = tile_types.dirt
    house.tiles[ROOM_LG.inner] = tile_types.floor_wood

    # Take given points (from room center) and use [x/y] lists from 'tunnel_between' function to connect them.
    for x, y in tunnel_between(ROOM_SM.center, ROOM_MD.center):
        dungeon.tiles[x, y] = tile_types.dirt

    if variation == 'dungeon': return dungeon
    if variation == 'house': return house
    


def generate_random_dungeon(
    max_rooms:      int,         
    room_min_size:  int,     
    room_max_size:  int,    
    map_width:      int,         
    map_height:     int,
    max_enemies:    int,
    player:         Entity,
) -> GameMap:
    ''' 
    Generates a procedurally-built dungeon map. 
    '''
    # Get the map width/height passed into the function and set a map instance with those dimensions.
    dungeon = GameMap(map_width, map_height, entities=[player])

    # Set a typed List to hold all the generated room instances (reference/key is 'rooms')
    rooms: List[RectangularRoom] = []

    for room in range(max_rooms):
        # Set random room width/height
        room_width  = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)
        # Set random coordinates to place the room
        x = random.randint(0, dungeon.width - room_width - 1)       
        y = random.randint(0, dungeon.height - room_height - 1)

        # Create a room (class instance) using the random values
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Iterate through other rooms in the List to determine if it overlaps (True or False)
        if any(new_room.intersects(other_room) for other_room in rooms):
            # If 'True', scrap the room and start the loop again to create a new one
            continue

        # When '.intersects()' does return 'False' (room doesn't overlap), the room is valid and can be tiled
        # (Set tiles to replace the default inner wall tiles initialized by the GameMap class)
        dungeon.tiles[new_room.inner] = tile_types.grass

        # Set player's starting position in the first room (from Tuple returned by room's '.center()' method)
        if len(rooms) == 0:
            player.x, player.y = new_room.center

        else:
            # Connect the centers of the previous room and the current one (tunnel)
            # ('rooms[-1]' goes backward in the rooms array by one item)
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                # Set the tiling for the tunnel
                dungeon.tiles[x, y] = tile_types.dirt

        place_entities(new_room, dungeon, max_enemies)
            
        # Add the new room to the list of other rooms
        rooms.append(new_room)

    return dungeon


