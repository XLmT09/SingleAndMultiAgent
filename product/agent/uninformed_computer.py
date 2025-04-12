import random
import time

from agent.computer import Computer
from collections import deque
from queue import PriorityQueue


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


class UCSComputer(Computer):
    def __init__(self, character, walkable_maze, **kwargs):
        super().__init__(
            character,
            walkable_maze,
            kwargs.get("perform_analysis", False),
        )
        self.heuristic = None
        diamond = kwargs.get("diamond")
        self.diamond_grid_x = diamond.grid_x
        self.diamond_grid_y = diamond.grid_y

    def generate_path(self) -> list:
        """ This function uses ucs search to find the path to the diamond. """

        start = self.character.get_player_grid_coordinates()
        fringe = PriorityQueue()
        # This dict records the lowest cost currently seen for any
        # vertex encountered.
        costs = {start: 0}
        # We will use this dict to go to generate the final path when
        # the goal is found.
        came_from = {start: None}
        # I have coded this algo such that a visited list is not needed but
        # we still want to use it for showing which grids were visited on
        # the maze game.
        visited = []

        # The fringe will record the (cost, position) of the grids
        fringe.put((0, start))

        while not fringe.empty():
            cost, current = fringe.get()
            visited.append(current)

            # When we found the diamond we can stop the algorithm
            if current == (self.diamond_grid_y, self.diamond_grid_x):
                self._visited_grids = visited
                if self.perform_analysis:
                    print(f"The number of visited nodes is: {len(came_from)}")

                return self.reconstruct_path(came_from, current)

            # Loop through the neighbours of the current vertex and add to
            # the fringe if its not been recorded in the costs dict, or if it
            # has been recorded then see if it can grant as a lower path cost.
            for neighbour in self.get_neighbour(current, cost):
                new_cost, neighbour_pos = neighbour

                if (neighbour_pos in came_from and
                   came_from[current] == neighbour_pos):
                    continue

                if ((neighbour_pos not in costs) or
                        (new_cost < costs[neighbour_pos])):
                    costs[neighbour_pos] = new_cost
                    came_from[neighbour_pos] = current
                    fringe.put((new_cost, neighbour_pos))

    def get_neighbour(self, current, cost) -> list:
        """ Get the neighbours and its costs from a grid/vertex. """

        neighbours = []

        # Loop through all the neighbours
        for direction in self._directions:
            new_cost = 0
            neighbour = (current[0] + direction[0], current[1] + direction[1])

            # Get the type of grid the neighbour is
            neighbour_grid_value = (
                self._walkable_maze_matrix[neighbour[0]][neighbour[1]]
            )

            # If the neighbour is a wall or floor then skip
            if (neighbour_grid_value == 0):
                continue

            # Check if the neighbour is a empty space or a ladder
            if (neighbour_grid_value == 1 or neighbour_grid_value == 3):
                new_cost = cost + 1
            # Check if the neighbour is a slow tile
            elif (neighbour_grid_value == 4):
                new_cost = cost + 3

            neighbours.append((new_cost, neighbour))

        # sort neighbour from low to high using the cost value
        return sorted(neighbours, key=lambda x: x[0])
