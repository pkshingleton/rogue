'''
Actions are used by the input event handler for returning an outcome (action) based on a detected event.

'Movement' action takes two values. When this action type is returned to the engine, the values become x/y coordinates which offset the position of whatever is supposed to be moving (usually the player sprite).

'Escape' action is used for exiting menus or closing things.
'''


#_______________________________________________________________________// CLASS
# Base class 
class Action:
    pass


# 'ESC' key to exit the game
class EscapeAction(Action):
    pass


# Movement keys to update palyer's coordinates
class MovementAction(Action):
    
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

