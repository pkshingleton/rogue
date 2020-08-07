#----------------------------------------------------------------------// IMPORTS

# Main library
import tcod as libtcod





#----------------------------------------------------------------------// GLOBALS

# Colors
red     = libtcod.red
white   = libtcod.white





#----------------------------------------------------------------------// FUNCTION

def main():
    # Window dimensions/resolution. --> (Move to JSON 'settings' file)
    screen_width = 80
    screen_height = 50

    # Player character screen position
    class PLAYER:
        x   = int(screen_width / 2)
        y   = int(screen_height / 2)


    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # Boolean value sets full-screen or windowed --> (True, False)
    libtcod.console_init_root(screen_width, screen_height, 'Rogue', False)

    # Holds keyboard/mouse input values
    key     = libtcod.Key()
    mouse   = libtcod.Mouse()


    # ***----- Game/main loop -----*** 
    while not libtcod.console_is_window_closed():

        # Pass captured keyboard/mouse input to input event bus 
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        libtcod.console_set_default_foreground(0, white)
        # Draw the 'player' sprite (@) and set starting position --> (console, x, y, player sprite, background)
        libtcod.console_put_char(0, PLAYER.x, PLAYER.y, '@', libtcod.BKGND_NONE)
        libtcod.console_flush()

        key = libtcod.console_check_for_keypress()

        # Set 'ESC' key to break the loop
        if key.vk == libtcod.KEY_ESCAPE:
            return True






#----------------------------------------------------------------------// INIT

# Sets the main() function to call immediately when the script is run
if __name__ == '__main__':
    main()
