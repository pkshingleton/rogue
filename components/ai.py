'''
# root/components/

Uses Pathfinding tools from the TCOD library to control how entities move around on the map.

"cost" refers to how costly (time consuming) it is for the entity to reach its target. This way, enemies take the most efficient/economical path to reach the player.

EX: If a piece of terrain takes longer to traverse- whether because the tile inhibits movement, or another blocking entity is occupying another tile on the path- the 'cost' will be higher (adds '10' to the array). This encourages the entity to move around obstacles by identifying them as more costly.

(More on TCOD Pathfinding: https://python-tcod.readthedocs.io/en/latest/tcod/path.html)
'''


#_______________________________________________________________________// MODULES

from __future__ import annotations
from typing import (List, Tuple, TYPE_CHECKING)

import numpy as np                  # type: ignore
import tcod

from actions import (Action, MeleeAction, MovementAction, WaitAction)
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor



#_______________________________________________________________________// CLASS

class BaseAI(Action, BaseComponent):
    '''
    Extends the 'BaseComponent' class. Gives the entity a method for pathfinding
    '''
    # Reference all the 'Actor' class attributes
    entity: Actor

    
    def perform(self) -> None:
        raise NotImplementedError()


    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        '''
        Compute and return a path to the target position. If there's no valid path, return an empty list.
        '''
        # Copy the walkable array
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        # Loop through any entities registered on the given map
        for entity in self.entity.gamemap.entities:
            # Check that an entity blocks movement and the cost isn't zero (blocking)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position
                # A lower number means more enemies will crowd behind each other in hallways.
                # A higher number means enemies will take longer paths in order to surround the player.
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))     # (Start position)

        # Compute the path to the destination and remove the starting point
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]]
        return [(index[0], index[1]) for index in path]


    
class HostileEnemy(BaseAI):
    '''
    Extends 'BaseAI' component/class to add decision making for enemies. 
    Enemy will either attack, move toward the player, or wait for its next turn.
    '''
    
    def __init__(self, entity: Actor):
        super().__init__(entity)
        # Initialize and set a List (array) for the enemy's path
        self.path: List[Tuple[int, int]] = []

    
    def perform(self) -> None:
        '''
        - If not in the player's vision, wait until next turn.
        - If the player is right next to the enemy, attack the player.
        - If the player sees the enemy, but the enemy is too far away to attack, move closer to the player.
        '''
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))    # "Chevyshev" distance

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()

            # Update the enemy's path to chase after the player
            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(self.entity, dest_x - self.entity.x, dest_y - self.entity.y).perform()

        # Wait until the next turn
        return WaitAction(self.entity).perform()
