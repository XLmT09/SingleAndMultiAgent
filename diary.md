### Week 22
<ins>**New Algorithms**</ins>
- The Expectimax algorithm has now been implemented.
- The Alpha-Beta algorithm has now been implemented.

<ins>**CLI Updates**</ins>
- I have implemented an `explain` flag for every algorithm. This briefly explains how each algorithm works to give the user some context.

<ins>**Updates on Game**</ins>
- I have implemented non-dead filled mazes for the medium and large-sized mazes.

<ins>**Refactor**</ins>
- `Minimax`, `Expectimax`, and `Alpha-Beta` are all extended from the `CompetitiveComputer` class. While they share most of their underlying logic, each implements its own version of the minimax function. It behaves slightly differently based on the algorithm's specific behavior. This led to a significant amount of duplicated code. To address this, I refactored the structure to combine the shared logic.

### Week 21
<ins>**Updates on Algorithm**</ins>
- The `minimax` algorithm can now work with more than one enemy. However, the game can only take up to three enemies. This is because the game gets too laggy.

<ins>**Updates on Game**</ins>
- Instead of jumping down a ladder, the player will climb for competitive algorithms. I'm doing this to ensure constant speed on all movements and avoid confusion for the `minimax` algorithm.

<ins>**Final Report**</ins>
- The professional issues section of the report is now complete.

### Week 19 - 20
<ins>**IMPORTANT NOTE**</ins>
- I spent these two weeks ( plus week 18) trying to implement the minimax algorithm. I managed to do it in the end, but I ran into many errors, which took me significant time to solve.

- I will not go over all the different approaches I took. However, I will mention how I solved the problem.

- The culprit was this piece of code here:
```python
        if (pos[1] - 1 > 1 and
            self._walkable_maze_matrix[pos[0]][pos[1] - 1] !=
            C.NON_WALKABLE_GRID):
            legal_movements.append("LEFT")
```
- I should have used `>=` instead of `>`. By using > 1, I unintentionally excluded valid walkable areas, which caused the algorithm to behave incorrectly. Although it was a minor fix, the program's complexity made it difficult to identify the root cause.

<ins>**Updates on Algorithm**</ins>
- The `minimax` algorithm is still causing problems, though I have made some new modifications. 
- First, instead of calculating the manhattan distance to diamonds and other players, it will do a BFS search instead. I believe this is the right choice to make because the Manhattan distance does not consider the walls, floors and ceilings, but BFS does.

- I also changed when the depth should be decremented. Instead of decreasing on each player, it will decrease after a round is complete; in other words, all players have made one move.

<ins>**Updates on Game**</ins>
- I noticed that the current small maze isn't very good for the minimax algorithm, as there are dead ends. So, once the minimax algo works appropriately, the enemy agent will have a significant advantage. I implemented a special small maze for competitive algorithms with no dead ends to fix this.


### Week 18
<ins>**New Algorithm**</ins>
- Implementation of the minimax algorithm has begun. Although many issues arose, I had to fix them this week. The algorithm is incomplete as there are still many bugs.
- **This minimax algorithm is not complete.**

<ins>**CLI Logic**</ins>
- The user now has the option to use the minimax algorithm. If the minimax algorithm is passed with no enemy count, it will throw an error.

### Week 17
<ins>**Updates on Algorithm**</ins>
- When the agent encounters an enemy which is at most 3 blocks away, it will move away and re-calculate a new path to the diamond.

### Week 16
<ins>**Updates on Game**</ins>
- Add enemy agents to the game.
- The enemy agent will move around the map randomly.
- If the main player collides with an enemy, then the game ends.
- The cli takes a flag `enemy_count`, which is the number of enemies to produce in the game. By default no enemies are generated if the flag is not passed.

<ins>**Refactoring**</ins>
- The character file, is now split into 3 files:
  - `character.py` - attributes and functions all character types share are in here.
  - `enemy_character.py`
  - `main_character.py`

### Week 15
<ins>**Updates on Algorithm**</ins>

- Implemented A star-filled algorithm; it uses the min spanning tree as a heuristic to calculate the path to collect all the diamonds.

<ins>**Refactoring**</ins>
- There are now two classes for A star: 
    - `AstarComputer`
    - `AstarFilledComputer`

<ins>**Updates on Game**</ins>
- Based on user input, I added CLI logic to determine whether to use `AStar` or the `AstarFilled` algorithm.

### Week 14

<ins>**No development had an idea..... It didn't work.....**</ins>

I thought about how to model the A star-filled maze algorithm. More specifically, I was thinking about how to model the heuristic function.

The formula is:

`F_cost = G_cost + H_cost`

The `G_cost` is straightforward; it's just the cost from the player to the diamond.
The `H_cost` (the heuristic function) is more interesting here. This heuristic will help determine the agent's path to visit all the diamonds.

At first, I thought the traveling sales problem (TSP) approach would work; after all, it does find the globally optimal solution. However, the deeper I got, the more impractical I found this solution to be. This is because TSP is an NP-HARD problem, so it won't find the globally optimal path in a reasonable time. Therefore, I scraped this idea and had to think of something else.

If you look at the project plan, I had another idea: to use the MST (Minimum Spanning Tree) as the heuristic. So, I knew using TSP would most likely not work, but I still wanted to try it.

The MST doesn't give the globally optimal path, but it's accurate enough and outputs almost instantly. So I went ahead with this idea.

### Week 13

<ins>**Updates on Algorithms**</ins>

- I have implemented the greedy search algorithm, this is the first algorithm compatible with a filled maze environment.
- This algorithm only uses the Manhattan distance to find the next diamond to visit, so no `g_cost`is considered here.

<ins>**Updates to Game**</ins>

- I have added medium and large filled mazes to the game.
- The cli will also deny any algorithms that do not work for a filled maze.
- Although the diamonds were filled it didn't regenerate once they were all collected, so I made sure there was regeneration when this condition was met.


### Christmas Break

<ins>**Updates on Algorithms**</ins>

- Implemented the A star algorithm
- For the heuristics I used the existing Manhattan function, but also a weighted one too. The weighted Manhattan function has more of a influence about the path decision making.

<ins>**Updates on Game**</ins>

- A new game mode has been implemented. In this game mode the user has the option to be in a maze environment where every cell is filled with diamonds. Currently this only works for small mazes.
- The cli now also takes a_star as an option, and also a weighted flag for heuristic option.

<ins>**Refactoring**</ins>

- I split the computer class into three files. 
  - `Computer.py` which contains the parent computer class.
  - `UninformedComputer.py` which contains the `UniformedComputer` class where the uniformed computers inherit from
  - `InformedComputer.py` which contains the `InformedComputer` class where the informed computers inherit from.

### Week 12

<ins>**Interim Report**</ins>

- This week I spent time finishing my interim report.

### Week 11

<ins>**Updates on the Game**</ins>

- I have added a highlighter function which will highlight the explored nodes from the currently in use algorithm colored in red and then the final path generated coloured in blue.
- I have also added CLI logic to my application where it take different flags like: size, algo and highlight.
- I have developed some analysis "tools", which will output the time it took for a certain algo to run, the nodes visited and final node distance from the start to the goal state.

<ins>**Problems and Fixes**<ins>

- The small and medium mazes had a lot of empty space surrounding them. When I tried to reduce the matrix size (i.e. get rid of all the unnecessary 1's causing the unwanted space), it would throw an out of index error.
- The reason for this error is because of the I set the pygame screen's width and height to be compatible with the large maze. To fix this problem I added some conditional statements to adjust the screen size based on the maze size.

<ins>Testing</ins>

- I have added tests for the CLI, a new test file was needed for this called <code>test_cli.py</code>.
- I was also able to understand how GUI testing works a new test file was also created for this called <code>test_find_path_gui.py</code>. However, there isn't much time now for this term to do more gui testing, I will either how to continue during christmas break or second term with this.

### Week 10

<ins>**Interim Report**</ins>

- For background and theory I have added information about BFS.

<ins>**GitLab Pipeline**</ins>

- I have included a checkstyle stage onto the pipeline where the code must follow python flake8 style.

<ins>**Problems and Fixes**</ins>

- The algos were crashing after it reaches the diamond, so it wasn't automatically finding a path for the new generated diamond. This is because when refactoring my code to follow the flake8 style, i removed a line on accident. You can see more on this [commit](d09757cfdb4e5c57ff652103cdb8817c6e1d04c6).

<ins>**Testing**</ins>

- I have written a test to check if the algorithms can produce a path when the start state is a goal state.

### Week 9

<ins>**Interim Report**</ins>

- I have written the project spec and overview.
- I have written aims and objectives.
- I have written background knowledge for dfs.

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

<ins>**Problems/ Potential Issues**</ins>

- Right now the BFS algorithm **first** finds a path, once a path is found the character is able to move. I'm not sure if this going to cause problems or not, but for now this is how I have implemented it.
- When <code>BFSComputer</code> is running, the game is lagging. I'm pretty sure this is an issue related with the thread that had been generated to do the path finding. Also, when <code>RandomComputer</code> is running there is no noticeable lag.

### Week 4

- Added logic so that diamonds are able to respawn when the player collides with them, on top of this I have also added a score counter which increments every time the player collides with a diamond.
- The first algorithm for the agent has been implemented where it will randomly move around the map.
- To implement the random path finding algorithm I have created a separate thread whose purpose is to randomly calculate the movement of the player and then send it to the player object that is on the main thread.
- I want to keep it so that the player can only move in 4 directions (up, down, left, right), this is because future algorithms I have planned will be easier to implement. I found that if I allow the player to jump then they can perform movements outside of the 4 directions I had intended. So my plan is to remove the jump functionality and replace it with a climb movement instead.
- I have put ladders into the game, where players can climb up and down the ladder. This meant that I also added some climbing sprite animations for the player.
- I created a text class, where I can pass in some text and then in the main function I just call a function defined in the text class to output it to the screen. The text class
- I have also begun to document the code, the code which has so far been documented is under world.py and text.py.

### Week 3

- Add collision detection with the character and the maze.
- Add diamond into the game, when the character collides with the diamond the game will pause.

### Week 2

- I have created the maze for the game, adding different tile types.
- Added character animations and movement, the animations I have added are: idle, walk and jump.

### Week 1

- I have been doing research for the project and making a rough plan of what I will be doing this year.
