'''
Stores all the entities that can be placed on a map as instances of the 'Actor' class. 
Includes player, NPCs (shopkeepers, etc.) enemies, and more!
'''


#_______________________________________________________________________// MODULES

from entity import Actor
from components.ai import HostileEnemy
from components.fighter import Fighter

from colors import *



#_______________________________________________________________________// DATA (TUPLES) - ENTITIES

# Player
player = Actor(
    char       = "@",
    color      = yellow,
    name       = "Player",
    ai_cls     = HostileEnemy,
    fighter     = Fighter(hp=30, defense=2, power=5)
)

#Enemies
# TODO: Set enemy's 'Fighter' stats to derive from player's stats (so difficulty will scale up)

orc = Actor(
    char       = "O",
    color      = red,
    name       = "Orc",
    ai_cls     = HostileEnemy,
    fighter     = Fighter(hp=10, defense=0, power=3)
)

troll = Actor(
    char       = "T",
    color      = red,
    name       = "Troll",
    ai_cls     = HostileEnemy,
    fighter     = Fighter(hp=16, defense=1, power=4)
)
