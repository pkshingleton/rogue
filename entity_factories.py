'''
Stores all the entities that can be placed on a map. Includes player, NPCs (shopkeepers, etc.) and enemies.
'''


#_______________________________________________________________________// MODULES

from entity import Entity
from colors import *



#_______________________________________________________________________// DATA (TUPLES) - ENTITIES

# Player
player = Entity(
    char                = "@",
    color               = yellow,
    name                = "Player",
    blocks_movement     = True  
)

#Enemies
orc = Entity(
    char                = "o",
    color               = red,
    name                = "Orc",
    blocks_movement     = True  
)

troll = Entity(
    char                = "T",
    color               = red,
    name                = "Troll",
    blocks_movement     = True  
)