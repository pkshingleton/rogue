'''
Actions are used by the input event handler for returning an outcome (action) based on a detected event.

- ActionWithDirection: Adds x/y values to the base Action class for storing directional movement.
- MovementAction: Checks for valid movement conditions and calls the invoking entity's '.move()' method to update its position on a map.
- BumpAction: Determines if the successive Action will be a 'MeleeAction' or a 'MovementAction'
- MeleeAction: Attack an entity on an adjacent tile and handle damage/effects.
- EscapeAction: Terminates the game.
'''


from __future__ import annotations
from typing import TYPE_CHECKING

# Conditional modules
if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity



#_______________________________________________________________________// CLASSES

# Base class 
class Action:
    
    def perform(self, engine:Engine, entity:Entity) -> None:
        ''' 
        Takes two objects (instances of the "Engine" class and "Entity" class)
        
        'engine' is the scope this action is being performed in.
        'entity' is the object performing the action (player, npc, etc).
        
        This method is overridden by other subclasses (EscapeAction, MovementAction, etc.)
        '''
        raise NotImplementedError()



class EscapeAction(Action):
    ''' Close program / quit the game '''
    def perform(self, engine:Engine, entity:Entity) -> None:
        raise SystemExit()



class ActionWithDirection(Action):
    ''' 
    Inherits/extends the 'Action' class by setting values for assessing direction/movement. 

    This yields sub-classes that determine WHAT the direciton/movement invokes.
    '''
    def __init__(self, dx:int, dy:int):
        super().__init__()
        # Direction of travel
        self.dx = dx
        self.dy = dy

    def perform(self, engine:Engine, entity:Entity) -> None:
        raise NotImplementedError()



class MeleeAction(ActionWithDirection):
    '''
    Extends the 'ActionWithDirection' class to damage an entity in an adjacent tile (ie, 'melee attack').

    Takes the direction of travel (dx/dy) and attacks an entity in the way (if an entity occupies the destination tile).
    '''
    def perform(self, engine:Engine, entity:Entity) -> None:
        # Current position + direction of travel = destination x/y
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        # Store the returned entity object (if any)
        target = engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)

        # If return was 'None' (no entity found matching the function's criteria), no attack happens.
        if not target:
            return

        print(f"You kick the {target.name}! *POW*")



class MovementAction(ActionWithDirection):
    ''' 
    Extends 'ActionWithDirection' class for updating an entity's position on the map. 

    Checks the entity is landing on a walkable tile, not out of map bounds, and not being blocked by another entity. 
    If so, call the entity's .move() method (which calculates the new tile to move to).
    '''
    def perform(self, engine:Engine, entity:Entity) -> None:
        # Current position + direction of travel = destination x/y
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        # Check if entity's next move is out of bounds:
        if not engine.game_map.in_bounds(dest_x, dest_y):
            return 
        # Check if entity's next move is NOT on a walkable tile:
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return 
        # Pass this entity's destination x/y to a function that checks no other entities are occupying the target space.
        # If an entity is returned (found matching criteria), set the entity at the destination coordinates (block player)
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return 

        # If everything checks ok, call the entity's '.move()' method
        entity.move(self.dx, self.dy)



class BumpAction(ActionWithDirection):
    '''
    Extends 'ActionWithDirection' class to determine which action occurs next: 'MovementAction' or 'MeleeAction
    '''
    def perform(self, engine:Engine, entity:Entity) -> None:
        # Current position + direction of travel = destination x/y
        dest_x = entity.x + self.dx 
        dest_y = entity.y + self.dy

        # Calls a GameMap method to check if the entity is being blocked by another.
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)

        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)