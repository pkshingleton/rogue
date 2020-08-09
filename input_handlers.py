'''
Manages what happens when certain keys are pressed.
An event handler takes the input and sets values using one of the classes defined in 'actions.py'.
The value is returned to the engine, where the console is updated and re-drawn.
'''



from typing import Optional
import tcod.event
from actions import (Action, EscapeAction, MovementAction)



#-----|| INPUT EVENT HANDLER :: SUBCLASS -- (Extends the tcod 'EventDispatch' class)
class EventHandler(tcod.event.EventDispatch[Action]):


    # Receive a 'QUIT' event (user clicks 'x' in window)
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()


    # Receive a KEY-PRESS event
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:

        # Set the default action to 'none' (returned when no key/invalid key is pressed)
        action: Optional[Action] = None
        
        # Set instance of whatever key press is detected by the system
        key = event.sym 


        #----- DIRECTION key / movement (up, down, left, right)
        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)

        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)

        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)

        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)

        #----- 'ESC' keypress
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        #----- Any other keypress (invalid)
        return action