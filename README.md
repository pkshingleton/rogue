# Rogue
#### A rougelike clone using Python v.3+

I'm using the **[libtcod](https://github.com/libtcod/python-tcod)** library to explore and comprehend basic engine construction. Understanding engine structure will help with development of future projects and ideas.

## ____________________

The main loop controls all event bussing and instantiation. Keyboard/mouse input and tilemaps are handled by modules- the core functions are called from the engine main loop and return dictionaries (objects) to the event bus for parsing. Depending on the output of the event bus, the screen will update (re-draw) with any changes to UI, character position, or text.  



## ____________________

### Progress:

[Current segment](http://rogueliketutorials.com/tutorials/tcod/part-1/) covers setting up input handlers and updating user's position on-screen.



## ____________________

### Setup / Install / Run:

Requirements: (will add later)

### ----------
In CLI or terminal, navigate to root directory of project and enter:

    >> python engine.py 

This will open a new window. Use the arrow keys to move around. 



**'ALT-ENTER'** will go full-screen. 

**'ESC'** will close the window and exit.