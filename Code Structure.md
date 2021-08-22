# Code Structure
A basic outline of how the code will be structured to interact with the system

## Parts
A list of parts that we will need for the bot
- Discord Handler
- Game Manager
- Main Program

### Discord Handler
Will act as communication between the players and the game.
- Parse player orders and send them to the game manager
- Parse player requests for game info
- Track timers and send an advance game state either when the timer finishes or when ordered

### Game Manager
Runs the game, tracking locations of armies and fleets and control of territories and power centers
- When sent a list of orders and a command to advance the game state, will calculate results.
- When sent a map request, will build current map and send it to the main
- After each change in game state, will save state in case of crash

### Main Program
In charge of facilitating everything
- Turns everything on
- in case of crash, this will restart system
- Sends save data back and forth to game