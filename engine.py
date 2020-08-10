'''
Controls rendering, creating, reading, updating, and removing entities.
Structures when content is generated and placed.
Sources event handlers and routes values to entities based on those events.
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
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):

        self.entities       = entities
        self.event_handler  = event_handler
        self.game_map       = game_map
        self.player         = player


    #-----| Event handler
    def handle_events(self, events: Iterable[Any]) -> None:

        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

        if isinstance(action, MovementAction):
            if self.game_map.tiles["walkable"][self.player.x + action.dx, self.player.y + action.dy]:
                self.player.move(dx=action.dx, dy=action.dy)

        elif isinstance(action, EscapeAction):
            raise SystemExit()


    #-----| Rendering
    def render(self, console: Console, context: Context) -> None:

        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)
        console.clear()
    
