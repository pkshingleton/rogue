'''
Stores all the entities that can be placed on a map. Includes player, NPCs (shopkeepers, etc.) and enemies.
'''


#_______________________________________________________________________// MODULES

from entity import Entity



#_______________________________________________________________________// DATA (TUPLES) - ENTITIES

# Player
player = Entity(
    char                = "@",
    color               = (255, 255, 255),
    name                = "Player",
    blocks_movement     = True  
)

#Enemies
orc = Entity(
    char                = "o",
    color               = (63, 127, 63),
    name                = "Orc",
    blocks_movement     = True  
)

troll = Entity(
    char                = "T",
    color               = (0, 127, 0),
    name                = "Troll",
    blocks_movement     = True  
)