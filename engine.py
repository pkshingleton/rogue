#------------------------------------------------------------// IMPORTS
import tcod as libtcod





#------------------------------------------------------------// FUNCTION
def main():

    # Window dimensions/resolution. --> (Move to JSON 'settings' file)
    screen_width = 80
    screen_height = 50

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # Boolean value 'True' for full-screen, 'False' for windowed
    libtcod.console_init_root(screen_width, screen_height, 'Rogue', False)


    # Draw the 'character' (@) and set 'ESC' key to break the loop
    while not libtcod.console_is_window_closed():
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_put_char(0, 1, 1, '@', libtcod.BKGND_NONE)

        libtcod.console_flush()

        key = libtcod.console_check_for_keypress()

        if key.vk == libtcod.KEY_ESCAPE:
            return True






#------------------------------------------------------------// INIT
# Sets the main() function to call immediately when the script is run
if __name__ == '__main__':
    main()
