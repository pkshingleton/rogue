'''
The event handler takes a detected event and assigns a corresponding action "type".

- If a 'KeyDown' event is detected:
    - And the key is a direction:
        > Set the action to 'movement' and include the appropriate coordinate values the class expects. 
    - And the key is 'ESC'
        > Set the action to 'escape' (for closing or backing out of menus) 

- If a 'Quit' event is detected:
    > Close and exit the game
'''


#_______________________________________________________________________// MODULES

from __future__ import annotations
from typing import (Optional, TYPE_CHECKING)

import tcod.event

from actions import (Action, EscapeAction, BumpAction, WaitAction)

if TYPE_CHECKING:
    from engine import Engine



#_______________________________________________________________________// ASSIGNMENTS / DICT (OBJECTS)
# Dictionaries (objects) for storing the possible keypresses. 

# Cardinal direction movement
MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    # Vi keys.
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}

# Wait/skip turn
WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}



#_______________________________________________________________________// CLASSES

class EventHandler(tcod.event.EventDispatch[Action]):
    ''' 
    Inherits/extends 'tcod.event.EventDispatch' class and returns a generic 'action' depending on the event. 
    - The returned Action gets inherited and extended by other classes to define different action types.
    '''

    def __init__(self, engine: Engine):
        self.engine = engine


    def handle_events(self) -> None:
        raise NotImplementedError()


    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()



class MainGameEventHandler(EventHandler):
    '''
    Inherits and extends 'EventHandler' base class to enable primary gameplay controls.
    - Use this class for the main game.
    - KeyDown events call 'EscapeAction' or 'BumpAction' (which determines to perform either 'MoveAction' or 'MeleeAction').
    - 'ev_quit()' is already attached since its defined in the 'EventHandler' base class.
    '''
    
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue
                
            action.perform()

            # Enemies take turns and player FOV is updated before the next action.
            self.engine.handle_enemy_turns()
            self.engine.update_fov()


    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        # Set the default action to 'none' (returned when no key/invalid key is pressed)
        action: Optional[Action] = None

        # Capture the key pressed and grab the 'player' instance from the engine object
        key = event.sym 
        player = self.engine.player

        # Check if keypress matches a valid keypress in the pre-defined Dict objects
        if key in MOVE_KEYS:
           dx, dy = MOVE_KEYS[key]
           action = BumpAction(player, dx, dy)

        elif key in WAIT_KEYS:
            action = WaitAction(player)

        # The 'ESC' key returns an 'escape' action
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(player)

        # Returns the resulting action type (defualt = 'none')
        return action



class GameOverEventHandler(EventHandler):
    '''
    Inherits and extends 'EventHandler' class for limited controls available to the player.
    - Use this class after the player dies where the only valid key should be 'ESC'.
    - Handling is identical to 'MainGameEventHandler.handle_events()' method, but without enemy turns or updating FOV.
    '''

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()


    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        '''
        same as the 'MainGameEventHandler.ev_keydown()' method but only allows for 'ESC' key. Player and Engine objects are omitted.
        '''
        action: Optional[Action] = None

        key = event.SystemExit

        if key == tcod.event.K_ESCAPE:
            action = EscapeAction(self.engine.player)

        # No valud keypress, return a blank object ('None')
        return action

