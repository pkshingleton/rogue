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
from typing import Optional
import tcod.event
from actions import (Action, EscapeAction, MovementAction)



#_______________________________________________________________________// CLASS
# (extends the tcod 'EventDispatch' class)
class EventHandler(tcod.event.EventDispatch[Action]):

    # 'QUIT' event
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()


    # KEY-PRESS event
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:

        # Set the default action to 'none' (returned when no key/invalid key is pressed)
        action: Optional[Action] = None

        # Set instance of whatever key press is detected by the system
        key = event.sym 


        # A direction key (up, down, left, right) sets the returned action as a 'movement'
        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)

        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)

        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)

        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)


        # The 'ESC' key returns an 'escape' action
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()


        # Returns the resulting action type (defualt = 'none')
        return action