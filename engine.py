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

from typing import (Set, Iterable, Any)

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler



#_______________________________________________________________________// CLASS

class Engine:

    # Initialize
    # (Expects a set of entities, an event handler, a map, and a separate reference to the player entity)
    def __init__(self, event_handler: EventHandler, game_map: GameMap, player: Entity):
        # The engine listens for events and updates the game map and player state (location and FOV) accordingly.
        self.event_handler  = event_handler
        self.game_map       = game_map
        self.player         = player
        self.update_fov() 


    def handle_enemy_turns(self)-> None:
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} when it will get to take a turn...')


    # (Continuously loops through the events passed in by 'EventHandler' class from the 'input_handlers.py' module)
    def handle_events(self, events: Iterable[Any]) -> None:
        ''' 
        Takes an event from 'tcod.event', EventHandler returns an 'action',
        Then the '.perform()' method is called to execute it.
        '''
        for event in events:
            action = self.event_handler.dispatch(event)

            # If no action is returned (or invalid action), do nothing
            if action is None:
                continue
        
            action.perform(self, self.player)
            self.handle_enemy_turns()
            self.update_fov()               # Updates player's FOV before their next action


    def update_fov(self) -> None:
        ''' Recompute the visible area based on the player's point of view. '''
        # Sets visibility of a tile based on tcod library's 'map.compute_fov()' method
        #   "transparency"- uses a 2D numpy array where any non-zero values are considered transparent.  
        #   "player.x, player.y" - the player's x/y point (character's POV)
        #   "radius" - how far the FOV extends (in tiled spaces)
        #   (https://python-tcod.readthedocs.io/en/latest/tcod/map.html#tcod.map.compute_fov)
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
    
