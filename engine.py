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

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler



#_______________________________________________________________________// CLASS
class Engine:

    # Initialize
    # (Expects a set of entities, an event handler, a map, and a separate reference to the player entity)
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities       = entities
        self.event_handler  = event_handler
        self.game_map       = game_map
        self.player         = player


    #_____/ METHOD / .handle_events(events)
    # (Continuously loops through the events passed in by 'EventHandler' class from the 'input_handlers.py' module)
    def handle_events(self, events: Iterable[Any]) -> None:
        ''' Takes an event from 'tcod.event', EventHandler returns an 'action', then the '.perform()' method is called to execute it.'''
        for event in events:
            action = self.event_handler.dispatch(event)

            # If no action is returned (or invalid action), do nothing
            if action is None:
                continue
        
            action.perform(self, self.player)


    #_____/ METHOD / .render(console. context)
    def render(self, console: Console, context: Context) -> None:
        ''' GameMap instance renders independently using its own .render() method. 

            Then A given set of entities is looped through and each one is added to the console. 
            
            Then 'tcod.context' displays the console to the screen. '''
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)
        console.clear()
    
