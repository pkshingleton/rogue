'''
Controls rendering, creating, reading, updating, and removing entities, tiles, and events.

To instantiate an engine, it will need:
    - a set of entities (enemies, player, other NPCs)
    - an event handler (to check for input and return corresponding 'actions')
    - a map (sets of tiles structured by the GameMap class)
    - a Player entity (a separate reference to one the entities passed in via the first expected argument)

The engine "render" function in sequence:
    - Passes the received map (collection of tiles) to the console
    - Loops through the received 'entities' set and sends each to the console with a location, symbol, and color
    - Prints the console to the screen (and clears it to start all over again).

'''


#_______________________________________________________________________// MODULES

from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import EventHandler

if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap



#_______________________________________________________________________// CLASS

class Engine:

    game_map: GameMap

    # Initialize
    # (Expects a set of entities, an event handler, a map, and a separate reference to the player entity)
    def __init__(self, player: Entity):
        # The engine listens for events and updates the game map and player state (location and FOV) accordingly.
        self.event_handler: EventHandler = EventHandler(self)
        self.player = player


    def handle_enemy_turns(self)-> None:
        # Go through all actors on a given game map (minus the player actor)
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()


    def update_fov(self) -> None:
        '''  
        * Sets visibility of a tile based on tcod library's 'map.compute_fov()' method
        - "transparency"- uses a 2D numpy array where any non-zero values are considered transparent.  
        - "player.x, player.y" - the player's x/y point (character's POV)
        - "radius" - how far the FOV extends (in tiled spaces) 
        > (https://python-tcod.readthedocs.io/en/latest/tcod/map.html#tcod.map.compute_fov)
        '''
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius = 8
        )
        # If a tile is "visible", it must have been "explored" (so add the 'visible' array to the 'explored' array)
        self.game_map.explored |= self.game_map.visible


    def render(self, console: Console, context: Context) -> None:
        ''' 
        GameMap instance renders independently using its own .render() method. 
        Then 'tcod.context' displays the console to the screen. 
        '''
        self.game_map.render(console)
        context.present(console)
        console.clear()
    
