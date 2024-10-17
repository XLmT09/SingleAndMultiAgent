### Week 4
- Added logic so that diamonds are able to respawn when the player collides with them, on top of this I have also added a score counter which increments every time the player collides with a diamond.
- The first algorithm for the agent has been implemented where it will randomly move around the map.
- To implement the random path finding algorithm I have created a seperate thread whose purpose is to randomly calculate the movement of the player and then send it to the player object that is on the main thread.
- I want to keep it so that the player can only move in 4 directions (up, down, left, right), this is because future algorithms I have planned will be easier to implement. I found that if I allow the player to jump then they can peform movements outside of the 4 directions I had intended. So my plan is to remove the jump functionality and replace it with a climb movement instead.
- I have put ladders into the game, where players can climb up and down the ladder. This meant that I also added some climbing sprite animations for the player.
- I created a text class, where I can pass in some text and then in the main function I just call a function defined in the text class to ouput it to the screen. The text class 
- I have also begun to docuement the code, the code which has so far been documented is under world.py and text.py.

### Week 3
- Add collison detection with the chaaracter and the maze.
- Add diamond into the game, when the character collides with the diamond the game will pause.

### Week 2
- I have created the maze for the game, adding different tile types.
- Added charcter animations and movement, the animations I have added are: idle, walk and jump.

### Week 1
- I have been doing research for the project and making a rough plan of what I will be doing this year.
