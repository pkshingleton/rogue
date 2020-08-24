'''
'RenderOrder' class is used to tell the console when to draw things to important elements aren't hidden underneath others.
- 'enum': a set of named values that won't change. Good for static assets and properties. 
- "auto': assigns incrementing integer values automatically. No need to retype if adding more later. 
'''

from enum import (auto, Enum)



class RenderOrder(Enum):
    '''
    Sets the order in which certain entities are rendered/drawn to the console. (aka, the "Z-index"). 
    - Lower values are rendered first, higher values rendered after.
    - If two things are on the same tile, whatever gets rendered last is what the player will see.
    '''

    # Primary entities
    CORPSE  = auto()        # Set when an entitiy dies
    ITEM    = auto()        # Dropped Gold, etc.
    ACTOR   = auto()        # Includes Player

    # Merchants, shopkeepers, etc.
    NPC     = auto()
    # 'holes' in the floor should swallow up entities, so it will always appear on top.
    PIT     = auto()        
    # Flames set tiles to 'light'(2-tile radius) and replenish equipped lamp/torch items. 
    FIRE    = auto()        
