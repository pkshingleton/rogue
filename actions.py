'''
Actions are used by the input event handler for returning an outcome (action) based on a detected event.

'Movement' action takes two values. When this action type is returned to the engine, the values become x/y coordinates which offset the position of whatever is supposed to be moving (usually the player sprite).

'Escape' action is used for exiting menus or closing things.
'''


from __future__ import annotations
from typing import TYPE_CHECKING

# Conditional modules
if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity



#_______________________________________________________________________// CLASS
# Base class 
class Action:
    
    # Passes the engine and the entity performing the action 
    def perform(self, engine: Engine, entity: Entity) -> None:
        ''' 
        Perform this action with the objects needed to determine its scope 
        
        'engine' is the scope this action is being performed in.
        'entity' is the object performing the action
        
        This method must be overridden by Action subclasses
        '''

        raise NotImplementedError()


# 'ESC' key to exit the game
class EscapeAction(Action):
    
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


# Movement keys to update palyer's coordinates
class MovementAction(Action):
    
    def __init__(self, dx: int, dy: int):
        super().__init__()

        # Direction of travel. Used to calculate entity's new position after a successful move action.
        # (ie, the return value for 'EventHandler.ev_keydown' event)
        self.dx = dx
        self.dy = dy

    # Checks the entity is landing on a walkable tile and not out of map bounds
    def perform(self, engine: Engine, entity: Entity) -> None:

        # Destination is the entity's current position + direction of travel
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        # Check if entity's next move is out of bounds (True = no move)
        if not engine.game_map.in_bounds(dest_x, dest_y):
            return 

        # Check if entity's next move is on a walkable tile (True = no move)
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return 

        # Otherwise, update entity's position (complete move action).
        entity.move(self.dx, self.dy)

