import threading
import time
import random
from collections import deque
import numpy as np
from queue import PriorityQueue
import inspect
from lock import visited_and_path_data_flag

moves = ["LEFT", "RIGHT"]


class Computer:
    """ This class will represent the agent different pathfinding algos
        available to use.

    Attributes:
        character (CharacterAnimationManager): The character the computer will
            be controlling.
        requested_movement (str): The movement the computer class will command
            the character to perfrom.
        _walkable_maze_matrix (list of list): The maze which represents the
            walakable areas of the character.
        _directions (list of tuple): The directions the computer can command
            the player to do.
        stop_thread (bool): A flag to stop the path find algo thread.
        th (Thread): The thread which will do the pathfinding.
        perfrom_analysis (bool): When this flag is set it records and prints
            analysis of the particular algo being used.
        _visited_grids (list of tuple): List of grids visited to get to the
            goal state by a algorithm.
        _path_generated (list of grids): List of sequential grids from start
            to get to the goal state.

    Args:
        character (CharacterAnimationManager): The character the computer will
            be controlling.
        walkable_maze (list of list): The maze which represents the walakable
            areas of the character.
    """
    def __init__(self, character, walkable_maze, perfrom_analysis):
        self.character = character
        self.requested_movement = "RIGHT"
        self._walkable_maze_matrix = walkable_maze
        # right, left, up, down
        self._directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.stop_thread = False
        self.perfrom_analysis = perfrom_analysis
        self._visited_grids = []
        self._path_generated = []
        self.th = threading.Thread(target=self.perfrom_path_find)

    def start_thread(self) -> None:
        """ Start the path find thread. """
        self.th.start()

    def stop_path_find_algo_thread(self) -> None:
        """ Stop the path find thread. """
        self.stop_thread = True

    def move(self, screen, world_data, asset_groups, game_over):
        """ Move the character based on the requested movement. """
        return self.character.draw_animation(screen, world_data, asset_groups,
                                             game_over,
                                             self.requested_movement)

    def reconstruct_path(self, search_path_histroy, end) -> None:
        """ Some algo's will store store contents of every path its
            looked into, in this function we will extract the
            path its found to the target.

        Args:
            search_path_histroy (list of tuples): A list of all the paths that
                                                  has been looked into.
            end (list): The coord of the diamond.
        """
        final_path = []
        current = end

        while current is not None:
            final_path.append(current)
            current = search_path_histroy[current]

        final_path.reverse()

        if self.perfrom_analysis:
            print(f"The path generated is: {final_path}")

        self._path_generated = final_path
        visited_and_path_data_flag.clear()

        return final_path

    def move_based_on_path_instructions(self) -> None:
        """ This function will get the BFS path, then  move the character
        to follow the path it's found. """
        path_to_follow = self.generate_path()

        if self.perfrom_analysis:
            print(f"The path is: {path_to_follow}")
            print(f"Path length is: {len(path_to_follow)}")

        instruction_number = 0
        target = path_to_follow[-1]
        climbing = False
        player_position = (self.character.grid_y, self.character.grid_x)

        while player_position != target:
            if self.stop_thread:
                print("STOPPING THE COMPUTER THREAD.")
                break
            if instruction_number == len(path_to_follow):
                return

            pos_diff = tuple(np.subtract(player_position,
                             path_to_follow[instruction_number]))

            if (pos_diff == (0, 0)):
                instruction_number += 1
                continue

            if (climbing and pos_diff[1] > 0):
                self.requested_movement = "UP LEFT"
                time.sleep(1)
                climbing = False
            elif (climbing and pos_diff[1] < 0):
                self.requested_movement = "UP RIGHT"
                time.sleep(1)
                climbing = False
            elif (pos_diff[0] > 0 or climbing):
                self.requested_movement = "UP"
                climbing = True
            elif (pos_diff[1] > 0 and not climbing):
                self.requested_movement = "LEFT"
            elif (pos_diff[1] < 0 and not climbing):
                self.requested_movement = "RIGHT"

            # update the player position value
            player_position = (self.character.grid_y, self.character.grid_x)

        self.requested_movement = "None"
        return

    def get_visited_grids_and_path_to_goal(self) -> list:
        """ This function retrives and returns the visted list generated by
        whatever algorithm is currently in use. """

        if self.perfrom_analysis:
            print(f"The list of visited grids is: {self._visited_grids}")

        if (self._visited_grids == [] or self._visited_grids is None):
            print(f"{inspect.currentframe().f_code.co_name}: Cannot get "
                  "visited grids")
            return None

        return self._visited_grids, self._path_generated

    def set_walkable_maze(self, walkable_maze) -> None:
        """ Set the walkable maze matrix with a new one. """
        self._walkable_maze_matrix = walkable_maze


class RandomComputer(Computer):
    """ This class will randomly move the character around the map. """
    def __init__(self, character, walkable_maze, perfrom_analysis=False):
        super().__init__(character, walkable_maze, perfrom_analysis)

    def perfrom_path_find(self) -> None:
        """ This function will use the random libary to randomly select a
        movement for the character to do, it does this by randomly updating
        self.requested_movement.
        """
        # Use this flag to allow the player to descend down a ladder instead
        # of always climbing it
        climbing = False

        while not self.stop_thread:
            # Once the player reaches the top of a ladder they can exit by
            # holding the up and right key at the same time
            if (self._walkable_maze_matrix[self.character.grid_y]
                                          [self.character.grid_x] == 3 and
                self._walkable_maze_matrix[self.character.grid_y]
                                          [self.character.grid_x+1] == 1 and
                self._walkable_maze_matrix[self.character.grid_y]
                                          [self.character.grid_x-1] == 1 and
                    climbing):
                self.requested_movement = random.choice(
                                            ["UP RIGHT", "UP LEFT"])
                climbing = False
            elif (self._walkable_maze_matrix[self.character.grid_y]
                                            [self.character.grid_x] == 3 and
                  self._walkable_maze_matrix[self.character.grid_y]
                                            [self.character.grid_x+1] == 1 and
                    climbing):
                self.requested_movement = "UP RIGHT"
                climbing = False
            elif (self._walkable_maze_matrix[self.character.grid_y]
                                            [self.character.grid_x] == 3 and
                  self._walkable_maze_matrix[self.character.grid_y]
                                            [self.character.grid_x+1] == 1 and
                    climbing):
                self.requested_movement = "UP LEFT"
                climbing = False
            elif (self._walkable_maze_matrix[self.character.grid_y]
                                            [self.character.grid_x] == 3):
                # Once the computer finds a ladder, it'll need to randomly
                # decide to climb it or not
                if (random.randint(0, 1) == 0):
                    self.requested_movement = "UP"
                    climbing = True
            # If the player is about to walk into a wall then
            # force it to move the other way
            elif (self._walkable_maze_matrix[self.character.grid_y]
                                            [self.character.grid_x - 1] == 0):
                self.requested_movement = "RIGHT"
            elif (self._walkable_maze_matrix[self.character.grid_y]
                                            [self.character.grid_x + 1] == 0):
                self.requested_movement = "LEFT"
            else:
                self.requested_movement = random.choice(moves)

            time.sleep(1)


class BFSComputer(Computer):
    """ This class will control the character and do BFS path find. """
    def __init__(self, character, walkable_maze, perfrom_analysis=False):
        super().__init__(character, walkable_maze, perfrom_analysis)

    def perfrom_path_find(self) -> None:
        """ This functions keeps searching for a path until the stop_thread
        flag is set. """
        while not self.stop_thread:
            self.move_based_on_path_instructions()
        print("PERFORM_PATH_FIND THREAD HAS STOPPED")

    def generate_path(self) -> list:
        """ This function uses bfs search to find the path to the diamond. """

        start = self.character.get_player_grid_coordinates()
        queue = deque([start])
        visited = []
        # This will contain the all the potential paths, bfs has looked into
        search_path_histroy = {start: None}

        while queue:
            current = queue.popleft()
            visited.append(current)
            if self._walkable_maze_matrix[current[0]][current[1]] == 2:

                self._visited_grids = visited

                if self.perfrom_analysis:
                    print(f"The number of visited nodes is: {len(visited)}")

                return self.reconstruct_path(search_path_histroy, current)

            # Loop through all 4 directions the computer can take
            for direction in self._directions:
                next_grid = (current[0] + direction[0],
                             current[1] + direction[1])

                # Check if the next grid we are looking at is
                # walkable and not visited.
                if (self._walkable_maze_matrix[next_grid[0]][next_grid[1]]
                        != 0 and next_grid not in visited):
                    queue.append(next_grid)
                    search_path_histroy[next_grid] = current

        return None


class DFSComputer(Computer):
    def __init__(self, character, walkable_maze, perfrom_analysis=False):
        super().__init__(character, walkable_maze, perfrom_analysis)

    def perfrom_path_find(self) -> None:
        """ This functions keeps searching for a path until the stop_thread
        flag is set. """
        while not self.stop_thread:
            self.move_based_on_path_instructions()
        print("PERFORM_PATH_FIND THREAD HAS STOPPED")

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
                if self.perfrom_analysis:
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
    def __init__(self, character, walkable_maze, perfrom_analysis=False):
        super().__init__(character, walkable_maze, perfrom_analysis)

    def perfrom_path_find(self) -> None:
        """ This functions keeps searching for a path until the stop_thread
        flag is set. """
        while not self.stop_thread:
            self.move_based_on_path_instructions()
        print("PERFORM_PATH_FIND THREAD HAS STOPPED")

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
        # I haved coded this algo such that a visited list is not needed but
        # we still want to use it for showing which grids were visited on
        # the maze game.
        visited = []

        # The fringe will record the (cost, position) of the grids
        fringe.put((0, start))

        while not fringe.empty():
            cost, current = fringe.get()
            visited.append(current)

            # When we found the diamond we can stop the algorithm
            if self._walkable_maze_matrix[current[0]][current[1]] == 2:
                self._visited_grids = visited
                if self.perfrom_analysis:
                    print(f"The number of visited nodes is: {len(came_from)}")

                return self.reconstruct_path(came_from, current)

            # Loop through the neighbours of the current vertex and add to
            # the fringe if its not been recorded in the costs dict, or if it
            # has been recoeded then see if it can grant as a lower path cost.
            for neighbour in self.get_neighbour(current, cost):
                new_cost, neighbour_pos = neighbour
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
            neighbour_grid_vlaue = (
                self._walkable_maze_matrix[neighbour[0]][neighbour[1]]
            )

            # If the neighbour is a wall or floor then skip
            if (neighbour_grid_vlaue == 0):
                continue

            # Check if the neighbour is a empty space or a ladder
            if (neighbour_grid_vlaue == 1 or neighbour_grid_vlaue == 3):
                new_cost = cost + 1
            # Check of the neighbour is a slow tile
            elif (neighbour_grid_vlaue == 4):
                new_cost = cost + 20

            neighbours.append((new_cost, neighbour))

        # sort neighbour from low to high using the cost value
        return sorted(neighbours, key=lambda x: x[0])


agent_types = {
    "random": RandomComputer,
    "bfs": BFSComputer,
    "dfs": DFSComputer,
    "ucs": UCSComputer
}
