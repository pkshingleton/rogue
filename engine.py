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

from actions import (EscapeAction, MovementAction)
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


    #_____________// FUNCTION / EVENT-HANDLER
    # (Continuously loops through the events passed in by 'EventHandler' class from the 'input_handlers.py' module)
    def handle_events(self, events: Iterable[Any]) -> None:

        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
        
        # 'Movement' action was returned
        if isinstance(action, MovementAction):
            # Check if tile can be walked on
            if self.game_map.tiles["walkable"][self.player.x + action.dx, self.player.y + action.dy]:
                self.player.move(dx=action.dx, dy=action.dy)

        # 'Escape' action was returned
        elif isinstance(action, EscapeAction):
            raise SystemExit()


    #_____________// FUNCTION / RENDER
    def render(self, console: Console, context: Context) -> None:

        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)
        console.clear()
    
