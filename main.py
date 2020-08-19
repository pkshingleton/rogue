'''
The engine instantiates the window/console and main game loop.
Drawing/rendering occurs by updating the state of the console, and then printing it to the screen.

'''


#_______________________________________________________________________// MODULES

import tcod 
import copy

from engine import Engine
import entity_factories
from procgen import (generate_static_dungeon, generate_random_dungeon)



#_______________________________________________________________________// FUNCTION

def main() -> None:

    # Starting / default values
    screen_width    = 80
    screen_height   = 50

    map_width       = 80
    map_height      = 45    # -5 for a space between bottom of map and screen (for text area)

    room_max_size   = 10    # Largest tile-size a room can be
    room_min_size   = 6     # Smallest tile-size a room will be
    max_rooms       = 30    # Total rooms that can occupy a single map

    max_enemies    = 2     # The most monsters/enemies that can appear in a single room


    # Use the root-level included font sprite sheet for characters
    tileset = tcod.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)


    # Instance of the 'player' entity
    player = copy.deepcopy(entity_factories.player)
    # Instantiate the Engine class
    engine = Engine(player = player)
    # Auto-generated map
    engine.game_map = generate_random_dungeon(
        max_rooms       = max_rooms,         
        room_min_size   = room_min_size,     
        room_max_size   = room_max_size,    
        map_width       = map_width,         
        map_height      = map_height,
        max_enemies     = max_enemies,
        engine          = engine
    )

    # Recalculates tile visibility around the player ('explored', 'visible', or 'SHROUD')
    engine.update_fov()


    # Terminal/canvas: main state that gets continually updated and re-drawn. 
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
        >>> MAIN - GAME LOOP
        '''
        while True:

            # Get context for the console, draw it to the screen, and clear it
            engine.render(console=root_console, context=context)

            # Await user input/event and store it
            engine.event_handler.handle_events()

 