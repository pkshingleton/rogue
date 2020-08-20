'''
# root/components/
Defines a component with an engine instance/object as a property
'''


#_______________________________________________________________________// MODULES

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity



#_______________________________________________________________________// CLASS

class BaseComponent:
 
    # References the entity that is invoking this class.
    entity: Entity

    @property
    def engine(self) -> Engine:
        # Grabs the engine instance associated with this entity and sets it as a class property. 
        return self.entity.gamemap.engine

    