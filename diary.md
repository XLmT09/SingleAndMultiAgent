### Week 10

<ins>**Interim Report**</ins>
- For background and theory I have added information about BFS.

<ins>**GitLab Pipeline**</ins>
- I have included a checkstyle stage onto the pipeline where the code must follow python flake8 style.

<ins>**Problems and Fixes**</ins>
- The algos were crashing after it reaches the diamond, so it wasent automatically finding a path for the new generated diamond. This is because when refactoring my code to follow the flake8 style, i removed a line on accident. You can see more on this [commit](d09757cfdb4e5c57ff652103cdb8817c6e1d04c6).

<ins>**Testing**</ins>
- I have written a test to check if the algorithms can produce a path when the start state is a goal state.

### Week 9

<ins>**Interim Report**</ins>
- I have written the poject spec and overview.
- I have written aims and objectives.
- I have written background knowladge for dfs.

<ins>**GitLab Pipeline**</ins>
- I have setup a pipeline on gitlab which contains a build and testing stage.

### Week 8

<ins>**Interim Report**</ins>
- I have begun writing mmy interim report. I have written the abstract for now.

<ins>**Updates on Game**</ins>
- I have created a large maze, the game window how to shrink a little to make the game look better as there were some empty gaps around the maze.

<ins>**Problems and Fixes**</ins>
- Because the array size for the large maze was larger than the others, the position of the player was outside the maze (not in the game window). I just needed to re position the start coord of the player to fix this.

<ins>**Testing**</ins>
- I have written tests for BFS, DFS nad UCS to see if it can generate a path in a large maze.
- I wrote another test for UCS to see if it will actually choose the faster path over a slower one.

### Week 7
<ins>**Updates on Algorithm**</ins>
- Now that the game has slow tiles, different paths will have different costs. This means a new algorithm is needed to consider these factors, and the one I have implemented is Uniform Cost Search.

<ins>**Problems and Fixes**</ins>
- There were problems, though; first of all, my uniform cost search algorithm was not working as intended because it was not finding the most optimal path. I know this because I deliberately made a really slow path and a fast one, and it will always go for the slow one because it was shorter in distance. The reason for this is that this whole time, the algorithm was checking the tiles over it and not under it. Everything had been working fine before because the tile values were all 1, but now that I had added slow tiles with a value of 2, I was able to spot this mistake.

<ins>**Updates on Game**</ins>
- I also created a medium-sized maze.

<ins>**Testing**</ins>
- I have written test cases for the medium-size maze, testing the three path algorithms that have been written so far and seeing if they generate the expected path.
### Week 6

<ins>**Updates to Game**</ins>

- I have added slow blocks to the game; these are tiles the user can walk on top of but will slow down their movement speed from 1 to 0.5.
- I added slow blocks to prove that path-finding algorithms like BFS/DFS can find the shortest path but not the fastest one. It gives the motivation to work on a new path-finding algorithm.

<ins>**Problems and Fixes**</ins>

- When I put the slow tiles into the game, there were a lot of bugs which had to be resolved this week.

- Firstly, the computer search algorithms were throwing errors after adding the slow blocks.
  This is because the walkable maze function was not generated properly, as it did not consider the addition of the slow blocks, leaving gaps (zeros) in the matrix. So, in most cases, finding a path was impossible.
  I added an if statement to check for the slow blocks during generation to fix this.
- Then, the next issue I encountered was that I could not lower the movement from 1 to something like 0.5. This is because pygame.rect.x and pygame.rect.y do not take in float values. If we pass them float values, it will just convert them into integers, meaning the player will stop (rounds down to 0) or continue working at normal speed (rounds up to 1).
  I found a "hacky" solution on StackOverflow to resolve this issue. Instead of changing the x/y values of a rect, I can update its centre coordinates, allowing for decimal input.
  But then this caused issues with collisions, and it felt like the player was walking through the maze. This is because I also had to change and update the hitbox rect and manipulate its centre values.

### Week 5

- I have implemented the first real algorithm (BFS) the character will use to get to a diamond.
- There was an issue with threading because after i close the main application a child thread that was doing path finding kept running. To solve this I added a function into computer.py and when called it should terminate any threads that it had called.
- When the diamond re-spawns, I have made sure the BFS algorithm will automatically start finding a path to the new diamond location.
- I have split the computer class up with child classes, these child classes will represent its own algorithm. For example, <code>BFSComputer</code> and <code>RandomComputer</code>.

<ins>**Testing**</ins>

- I have written two test cases, one which checks if there is a diamond in the maze.
- The other test checks if the BFS algo generates the expected path to the target.

<ins>**Problems/ Potenial Issues**</ins>

- Right now the BFS algorithm **first** finds a path, once a path is found the character is able to move. I'm not sure if this going to cause problems or not, but for now this is how I have implemented it.
- When <code>BFSComputer</code> is running, the game is lagging. I'm pretty sure this is an issue related with the thread that had been generated to do the path finding. Also, when <code>RandomComputer</code> is running there is no noticable lag.

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
