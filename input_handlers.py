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

from actions import (Action, EscapeAction, BumpAction)

if TYPE_CHECKING:
    from engine import Engine



#_______________________________________________________________________// CLASSES

# (Extends the tcod 'EventDispatch' class - Listens for pre-set events and return an 'action')
class EventHandler(tcod.event.EventDispatch[Action]):
    ''' 
    Takes 'tcod.event.EventDispatch'event and returns an 'action' depending on the event. 
    KeyDown events call 'EscapeAction' (for ESC keypress) or 'BumpAction' (which determines if the player moves or attacks).
    '''

    def __init__(self, engine: Engine):
        self.engine = engine


    #_____/ METHOD / .handle_events()
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue
                
            action.perform()

            # Enemies take turns and player FOV is updated before the next action.
            self.engine.handle_enemy_turns()
            self.engine.update_fov()

    
    #_____/ METHOD / .ev_quit(tcod.event.Quit)
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()


    #_____/ METHOD / .ev_keydown(tcpd.event.KeyDown)
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:

        # Set the default action to 'none' (returned when no key/invalid key is pressed)
        action: Optional[Action] = None

        # Capture the key pressed
        key = event.sym 

        player = self.engine.player

        # A direction key (up, down, left, right) sets the returned action as a 'movement'
        if key == tcod.event.K_UP:
            action = BumpAction(player, dx=0, dy=-1)

        elif key == tcod.event.K_DOWN:
            action = BumpAction(player, dx=0, dy=1)

        elif key == tcod.event.K_LEFT:
            action = BumpAction(player, dx=-1, dy=0)

        elif key == tcod.event.K_RIGHT:
            action = BumpAction(player, dx=1, dy=0)

        # The 'ESC' key returns an 'escape' action
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(player)

        # Returns the resulting action type (defualt = 'none')
        return action