'''
The engine instantiates the window/console and main game loop.
Drawing/rendering occurs by updating the state of the console, and then printing it to the screen.
'''



#_______________________________________________________________________// MODULES
import tcod 
from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler



#_______________________________________________________________________// MAIN FUNCTION
def main() -> None:

    # Set default window screen size (will move into JSON 'settings' file later)
    screen_width    = 80
    screen_height   = 50

    map_width       = 80
    map_height      = 45


    # Use the root-level included font sprite sheet for characters
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # Sets instance of the 'EventHandler' class - receives and processes events
    event_handler = EventHandler()


    #-----| ENTITIES
    # (entities require: x, y, symbol, and color)
    player  = Entity(
        int(screen_width / 2), 
        int(screen_height / 2), 
        "@", (255,255,255)
    )
    npc     = Entity(
        int(screen_width / 2-5), 
        int(screen_height / 2), 
        "@", (255,255,0)
    )

    # Place the entities into a container object (dict)
    entities = {npc, player}


    #-----| MAP
    # Set the map/entity drawing area
    game_map = GameMap(map_width, map_height)

    # Instantiate the engine
    engine = Engine(
        entities        = entities, 
        event_handler   = event_handler, 
        game_map        = game_map, 
        player          = player
    )


    #-----| CANVAS / DRAW
    with tcod.context.new_terminal(
        
        screen_width,
        screen_height,
        tileset  = tileset,
        title    = "Rogue",
        vsync    = True,

    ) as context:

        # Pass in screen size and coordinate order - (Numpy array default is [y/x] - 'F' reverses the read order to [x/y])
        root_console = tcod.Console(screen_width, screen_height, order="F")

        '''
        >>> MAIN GAME LOOP
        '''
        while True:

            # Get context for the console, draw it to the screen, and clear it
            engine.render(console=root_console, context=context)

            # Await user input/event
            events = tcod.event.wait()

            # Pass event to the event handler to determine an action
            engine.handle_events(events)

 