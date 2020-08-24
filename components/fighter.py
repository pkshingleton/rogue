'''
# root/components/
Defines a component for attaching combat attributes to an entity by extending the BaseComponent class.
'''


#_______________________________________________________________________// MODULES

from __future__ import annotations
from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor



#_______________________________________________________________________// CLASS

class Fighter(BaseComponent):
    '''
    Extends the BaseComponent class to add health, power, and defense to an entity. 
    Health becomes a property ('_hp') 
    - A setter function prevents damage and healing from setting hp below 0 or above max_hp
    '''

    entity: Actor

    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp            # Total available health
        self._hp = hp               # Entity's current health
        self.defense = defense      # Value used for reducing damage
        self.power = power          # Entity's attack power / damage dealt

    
    @property
    def hp(self) -> int:
        # Getter: returns the hp value of this entity
        return self._hp


    @hp.setter
    def hp(self, value: int) -> None:
        # Setter: keeps hp from going outside the min/max possible health
        self._hp = max(0, min(value, self.max_hp))

        if self._hp == 0 and self.entity.ai:
            self.die()

    
    def die(self) -> None:
        '''
        Calling this method on the entity will set its attributes to a 'dead' entity.  
        - Its 'ai' is removed so its 'is_alive' property will return 'False' when called. 
        - The player can now walk over it.
        '''
        if self.engine.player is self.entity:
            death_message = "You died!"
        else:
            death_message = f"{self.entity.name} is dead!"

        # Set entity's new attributes:
        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f"The twisted corpse of {self.entity.name}."

        print(death_message)