import random
import time

from agent.computer import Computer
from collections import deque


class RandomComputer(Computer):
    """ This class will randomly move the character around the map. """
    def __init__(self, character, walkable_maze, **kwargs):
        super().__init__(
            character,
            walkable_maze,
            **kwargs
        )
        self.moves = ["LEFT", "RIGHT"]

    def perform_path_find(self) -> None:
        """ This function will use the random library to randomly select a
        movement for the character to do, it does this by randomly updating
        self.requested_movement.
        """
        # Use this flag to allow the player to descend down a ladder instead
        # of always climbing it
        climbing = False

        while not self.stop_thread:
            # player position
            pos = self.character.get_player_grid_coordinates()

            # Once the player reaches the top of a ladder they can exit by
            # holding the up and right key at the same time if right side free
            if (self._walkable_maze_matrix[pos[0] - 1][pos[1]] == 0 and
                self._walkable_maze_matrix[pos[0]][pos[1] + 1] == 1 and
                    climbing):
                if (random.randint(0, 1) == 0):
                    self.requested_movement = "UP RIGHT"
                    climbing = False
            # Once the player reaches the top of a ladder they can exit by
            # holding the up and left key at the same time if left side free
            elif (self._walkable_maze_matrix[pos[0] - 1][pos[1]] == 0 and
                  self._walkable_maze_matrix[pos[0]][pos[0]] == 1 and
                    climbing):
                if (random.randint(0, 1) == 0):
                    self.requested_movement = "UP LEFT"
                    climbing = False
            # If the player is not at the top of the ladder but there is an
            # exit on the right they can leave there.
            elif (self._walkable_maze_matrix[pos[0] - 1][pos[1]] == 3 and
                  self._walkable_maze_matrix[pos[0]][pos[1]] == 3 and
                  self._walkable_maze_matrix[pos[0]][pos[0]] == 1 and
                    climbing):
                if (random.randint(0, 1) == 0):
                    self.requested_movement = "UP RIGHT"
                    climbing = False
            # If the player is not at the top of the ladder but there is an
            # exit on the left they can leave there.
            elif (self._walkable_maze_matrix[pos[0] - 1][pos[1]] == 3 and
                  self._walkable_maze_matrix[pos[0]][pos[1]] == 3 and
                  self._walkable_maze_matrix[pos[0]][pos[1] + 1] == 1 and
                    climbing):
                if (random.randint(0, 1) == 0):
                    self.requested_movement = "UP RIGHT"
                    climbing = False
                self.requested_movement = "UP LEFT"
                climbing = False
            elif (self._walkable_maze_matrix[pos[0]][pos[1]] == 3):
                # Once the computer finds a ladder, it'll need to randomly
                # decide to climb it or not
                if (random.randint(0, 1) == 0):
                    self.requested_movement = "UP"
                    climbing = True
            # If the player is about to walk into a wall then
            # force it to move the other way
            elif (self._walkable_maze_matrix[pos[0]][pos[1] - 1] == 0):
                self.requested_movement = "RIGHT"
            elif (self._walkable_maze_matrix[pos[0]][pos[1] + 1] == 0):
                self.requested_movement = "LEFT"
            else:
                self.requested_movement = random.choice(self.moves)

            time.sleep(1)


class BFSComputer(Computer):
    """ This class will control the character and do BFS path find. """
    def __init__(self, character, walkable_maze, **kwargs):
        super().__init__(
            character,
            walkable_maze,
            **kwargs
        )

    def generate_path(self) -> list:
        """ This function uses bfs search to find the path to the diamond. """

        start = self.character.get_player_grid_coordinates()
        queue = deque([start])
        visited = []
        # This will contain the all the potential paths, bfs has looked into
        search_path_history = {start: None}

        while queue:
            current = queue.popleft()
            visited.append(current)
            if self._walkable_maze_matrix[current[0]][current[1]] == 2:

                self._visited_grids = visited

                if self.perform_analysis:
                    print(f"The number of visited nodes is: {len(visited)}")

                return self.reconstruct_path(search_path_history, current)

            # Loop through all 4 directions the computer can take
            for direction in self._directions:
                next_grid = (current[0] + direction[0],
                             current[1] + direction[1])

                # Check if the next grid we are looking at is
                # walkable and not visited.
                if (self._walkable_maze_matrix[next_grid[0]][next_grid[1]]
                        != 0 and next_grid not in visited):
                    queue.append(next_grid)
                    search_path_history[next_grid] = current

        return None


class DFSComputer(Computer):
    def __init__(self, character, walkable_maze, **kwargs):
        super().__init__(
            character,
            walkable_maze,
            **kwargs
        )

    def generate_path(self) -> list:
        """ This function uses dfs search to find the path to the diamond. """

        start = self.character.get_player_grid_coordinates()
        stack = [start]
        visited = []
        # We will use this dict to go to generate the final path when
        # the goal is found.
        search_path_history = {start: None}

        while stack:
            current = stack.pop()
            visited.append(current)

            # When we reach the goal state we can end the algorithm
            if self._walkable_maze_matrix[current[0]][current[1]] == 2:
                self._visited_grids = visited
                if self.perform_analysis:
                    print(f"The number of visited nodes is: {len(visited)}")

                return self.reconstruct_path(search_path_history, current)

            # Loop through the neighbours of the current vertex and add to
            # the stack if its not been visited or out of bounds.
            for direction in self._directions:
                next_grid = (current[0] + direction[0],
                             current[1] + direction[1])

                if (self._walkable_maze_matrix[next_grid[0]][next_grid[1]]
                        != 0 and next_grid not in visited):
                    stack.append(next_grid)
                    search_path_history[next_grid] = current
