'''
The engine instantiates the window/console and main game loop.
Drawing/rendering occurs by updating the state of the console, and then printing it to the screen.

'''


#_______________________________________________________________________// MODULES
import tcod 

from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from procgen import (generate_dungeon, generate_house)



#_______________________________________________________________________// FUNCTION
def main() -> None:

    # Set default window screen size in tiles (will move into JSON 'settings' file later)
    screen_width    = 80
    screen_height   = 50

    map_width       = 80
    map_height      = 45    # Leaves a 5-tile gap between bottom of map and bottom of screen (for text)


    # Use the root-level included font sprite sheet for characters
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # Sets instance of the 'EventHandler' class - receives and processes events
    event_handler = EventHandler()


    #_____________// DATA (TUPLES) - ENTITIES
    # (entities require: x/y coordinates, symbol, and color)
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

    # Place the entities into a set so they can be passed into the engine
    entities = {npc, player}


    #_____________// INSTANCE - MAPS
    # Set the map/entity drawing areas
    OUTDOOR_GARDEN = generate_dungeon(map_width, map_height)
    INDOOR_HOUSE = generate_house(map_width, map_height)


    #_____________// INSTANCE - ENGINE
    # Engine class returns actions from events, takes a map of tiles, and prints them to the console along with the player and other entities.
    engine = Engine(
        entities        = entities, 
        event_handler   = event_handler, 
        game_map        = OUTDOOR_GARDEN, 
        player          = player
    )


    #_____________// CANVAS (CONSOLE RENDER AREA)
    with tcod.context.new_terminal(

        screen_width,
        screen_height,
        tileset  = tileset,
        title    = "Rogue",
        vsync    = True,

    ) as context:

        # (Numpy array default is [y/x] - 'F' reverses the read order to [x/y] which is more conventional)
        root_console = tcod.Console(screen_width, screen_height, order="F")

        '''
        >>> _____________// LOOP - MAIN GAME
        '''
        while True:

            # Get context for the console, draw it to the screen, and clear it
            engine.render(console=root_console, context=context)

            # Await user input/event and store it
            events = tcod.event.wait()
            # Pass stored event to the engine's event handler
            engine.handle_events(events)

 