import tcod as libtcod


# Checks input key and returns a corresponding value to adjust whatever needs moved
def handle_keys(key):

    # Keyboard (UP, DOWN, LEFT, RIGHT):
    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}

    elif key.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1)}

    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}

    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}


    # 'ALT+ENTER' to toggle full-screen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    # 'ESC' key exits the game
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    # No key pressed, return nothing 
    return {}