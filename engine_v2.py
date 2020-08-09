'''
The engine instantiates the window/console and main game loop.
Drawing/rendering occurs by updating the state of the console, and then printing it to the screen.
'''



import tcod 
from actions import (EscapeAction, MovementAction)
from input_handlers import EventHandler



#_______________________________________________________________________// ENGINE - MAIN
def main() -> None:

    # Set default window screen size (will move into JSON 'settings' file later)
    screen_width    = 80
    screen_height   = 50

    # Track player coordinates
    player_x    = int(screen_width / 2)
    player_y    = int(screen_height / 2)


    # Use the root-level included font sprite sheet for characters
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # Sets instance of the 'EventHandler' class
    event_handler = EventHandler()

    # Set/Draw terminal area
    with tcod.context.new_terminal(
        # Pass in screen size
        screen_width,
        screen_height,

        tileset     = tileset,
        title       = "Rogue",
        vsync       = True,

    ) as context:

        # Pass in screen size and coordinate order - (Numpy array default is [y/x] - 'F' reverses the read order to [x/y])
        root_console = tcod.Console(screen_width, screen_height, order="F")


        '''
        ---------------------->>
        >>>  MAIN GAME LOOP
        <<----------------------
        '''
        while True:

            # Send the player 'sprite' and location to the console
            root_console.print(x=player_x, y=player_y, string="@")

            # Draw/output the current state of the console (primary render function / each re-draw is a 'frame')
            context.present(root_console)

            # Loop until user input is detected
            for event in tcod.event.wait():

                action = event_handler.dispatch(event)

                if action is None:
                    continue
                
                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy

                elif isinstance(action, EscapeAction):
                    raise SystemExit()
