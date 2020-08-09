#_______________________________________________________________________// IMPORTS
# Main library
import tcod as libtcod
from input_handlers import handle_keys




#_______________________________________________________________________// GLOBALS
# Colors
red     = libtcod.red
white   = libtcod.white




#_______________________________________________________________________// ENGINE (MAIN)
def main():
   
    # Window dimensions/resolution. --> (Move to JSON 'settings' file)
    screen_width = 80
    screen_height = 50


    # Player character screen position --> (Sets to center of screen)
    class PLAYER:
        x   = int(screen_width / 2)
        y   = int(screen_height / 2)


    # Load.png image for game font (in root directory)
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # Set screen size, title, and full-screen or windowed mode --> (True, False)
    libtcod.console_init_root(screen_width, screen_height, 'Rogue', False)

    # Store keyboard/mouse input values
    key     = libtcod.Key()
    mouse   = libtcod.Mouse()


    '''
    --------------------
    >>> MAIN GAME LOOP  
    --------------------
    ''' 
    while not libtcod.console_is_window_closed():

        #----------|| EVENTS :: INPUT
        # Pass captured keyboard/mouse input to input event bus 
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)


        #----------|| DRAW FUNCTIONS
        libtcod.console_set_default_foreground(0, white)

        # Set target console, 'player' sprite, position, and background
        libtcod.console_put_char(0, PLAYER.x, PLAYER.y, '@', libtcod.BKGND_NONE)

        # Clear console and re-draw
        libtcod.console_flush()


        #----------|| HANDLER :: KEYBOARD
        # Stores the returned dicts of the handler function
        action = handle_keys(key)

        # Get dict key/value and store it
        move        = action.get('move')
        exit        = action.get('exit')
        fullscreen  = action.get('fullscreen')

        if move:
            dx, dy = move
            PLAYER.x += dx
            PLAYER.y += dy

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


