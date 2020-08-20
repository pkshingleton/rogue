'''
# root/components/
Defines a component for attaching combat attributes to an entity by extending the BaseComponent class.
'''


#_______________________________________________________________________// MODULES

from components.base_component import BaseComponent



#_______________________________________________________________________// CLASS

class Fighter(BaseComponent):
    '''
    Extends the BaseComponent class to add health, power, and defense to an entity. 
    Health becomes a property ('_hp') 
    - A setter function prevents damage and healing from setting hp below 0 or above max_hp
    '''

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

