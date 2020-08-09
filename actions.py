'''
Defines the actions a player's character can make via classes.
Each class represents a different thing the player can do.
'''


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

