'''
Actions are used by the input event handler for returning an outcome (action) based on a detected event.

- ActionWithDirection: Adds x/y values to the base Action class for storing directional movement.
- MovementAction: Checks for valid movement conditions and calls the invoking entity's '.move()' method to update its position on a map.
- BumpAction: Determines if the successive Action will be a 'MeleeAction' or a 'MovementAction'
- MeleeAction: Attack an entity on an adjacent tile and handle damage/effects.
- EscapeAction: Terminates the game.
'''


#_______________________________________________________________________// MODULES

from __future__ import annotations
from typing import (Optional, Tuple, TYPE_CHECKING)

# Conditional modules
if TYPE_CHECKING:
    from engine import Engine
    from entity import (Actor, Entity)



#_______________________________________________________________________// CLASSES

# Base class 
class Action:

    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity


    @property
    def engine(self) -> Engine:
        '''
        Returns the engine instance this action belongs to (set in 'entity.gamemap.engine'), and sets the engine as a property.
        '''
        return self.entity.gamemap.engine

    
    def perform(self) -> None:
        ''' 
        Takes two objects (instances of the "Engine" class and "Entity" class)
        
        'self.engine' is the scope this action is being performed in.
        'self.entity' is the object performing the action (player, npc, etc).
        
        This method is overridden by other subclasses (EscapeAction, MovementAction, etc.)
        '''
        raise NotImplementedError()



class EscapeAction(Action):
    ''' Close program / quit the game '''

    def perform(self) -> None:
        raise SystemExit()



class WaitAction(Action):
    def perform(self) -> None:
        pass



class ActionWithDirection(Action):
    ''' 
    Inherits/extends the 'Action' class by setting values for assessing direction/movement. 

    This yields sub-classes that determine WHAT the direciton/movement invokes.
    '''

    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)
        # Direction of travel
        self.dx = dx
        self.dy = dy


    @property
    def dest_xy(self) -> Tuple[int, int]:
        ''' 
        Returns this actions destination as a property. 
        '''
        return self.entity.x + self.dx, self.entity.y + self.dy


    @property
    def blocking_entity(self) -> Optional[Entity]:
        '''
        Returns an entity blocking the player at this actions destination, and sets that entity as a property.
        '''
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)


    @property
    def target_actor(self) -> Optional[Actor]:
        ''' 
        Returns whatever actor is at the destination of this action
        '''
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)


    def perform(self) -> None:
        raise NotImplementedError()



class MeleeAction(ActionWithDirection):
    '''
    Extends the 'ActionWithDirection' class to damage an entity in an adjacent tile (ie, 'melee attack').

    Takes the direction of travel (dx/dy) and attacks an entity in the way (if an entity occupies the destination tile).
    '''

    def perform(self) -> None:
        ''' 
        Uses the inherited 'target_actor' property (defined in 'ActionWithDirection' class) to receive the attack. 
        '''
        target = self.target_actor
        # If return was 'None' (no entity found matching the function's criteria), no attack happens.
        if not target:
            return

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"

        if damage > 0:
            print (f"{attack_desc} for {damage} HP!")
            target.fighter.hp -= damage

        else:
            print (f"{attack_desc}... but does no damage.")



class MovementAction(ActionWithDirection):
    ''' 
    Extends 'ActionWithDirection' class for updating an entity's position on the map. 

    Checks the entity is landing on a walkable tile, not out of map bounds, and not being blocked by another entity. 
    If so, call the entity's .move() method (which calculates the new tile to move to).
    '''

    def perform(self) -> None:
        ''' 
        Commit this entity's movement to a destination by calling its own '.move()' method.
        '''
        dest_x, dest_y = self.dest_xy
        # Check if entity's next move is out of bounds:
        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return 
        # Check if entity's next move is NOT on a walkable tile:
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return 
        # Check if a 'blocking_entity' is in the destination tile:
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return 

        self.entity.move(self.dx, self.dy)



class BumpAction(ActionWithDirection):
    '''
    Extends 'ActionWithDirection' class to determine which action occurs next: 'MovementAction' or 'MeleeAction'
    '''

    def perform(self) -> None:
        '''
        Commit a 'MeleeAction' or a 'MovementAction' depending on whether a 'target_actor' is at this entity's destination.
        '''
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()