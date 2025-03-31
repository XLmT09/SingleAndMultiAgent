import threading
import time
import inspect
import numpy as np

from lock import visited_and_path_data_flag


class Computer:
    """ This class will represent the agent different pathfinding algos
        available to use.

    Attributes:
        character (MainAnimationManager): The character the computer will
            be controlling.
        requested_movement (str): The movement the computer class will command
            the character to perform.
        _walkable_maze_matrix (list of list): The maze which represents the
            walkable areas of the character.
        _directions (list of tuple): The directions the computer can command
            the player to do.
        stop_thread (bool): A flag to stop the path find algo thread.
        th (Thread): The thread which will do the pathfinding.
        perform_analysis (bool): When this flag is set it records and prints
            analysis of the particular algo being used.
        _visited_grids (list of tuple): List of grids visited to get to the
            goal state by a algorithm.
        _path_generated (list of grids): List of sequential grids from start
            to get to the goal state.

    Args:
        character (MainAnimationManager): The character the computer will
            be controlling.
        walkable_maze (list of list): The maze which represents the walkable
            areas of the character.
    """
    def __init__(self, character, walkable_maze, **kwargs):
        self.character = character
        self.requested_movement = "RIGHT"
        self._walkable_maze_matrix = walkable_maze
        # right, left, up, down
        self._directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.stop_thread = False
        self.perform_analysis = kwargs.get("perform_analysis", False)
        self._visited_grids = []
        self._path_generated = []
        self.path_to_follow = []
        self.enemy_list = kwargs.get("enemy_list", [])
        self.enemy_in_way = False
        self.th = threading.Thread(target=self.perform_path_find)
        if self.enemy_list:
            self.check_th = threading.Thread(target=self.check_for_enemies)

    def start_thread(self) -> None:
        """ Start the path find thread. """
        self.th.start()
        if self.enemy_list:
            self.check_th.start()

    def stop_path_find_algo_thread(self) -> None:
        """ Stop the path find thread. """
        self.stop_thread = True

    def move(self, screen, world_data, **kwargs):
        """ Move the character based on the requested movement. """
        return self.character.draw_animation(
            screen,
            world_data,
            self.requested_movement,
            **kwargs
        )

    def perform_path_find(self) -> None:
        """ This functions keeps searching for a path until the stop_thread
        flag is set. """
        while not self.stop_thread:
            self.move_based_on_path_instructions()
        print("PERFORM_PATH_FIND THREAD HAS STOPPED")

    def check_for_enemies(self) -> bool:
        search_depth = 3
        left_side, right_side, enemy_coords = set(), set(), set()

        while not self.stop_thread:
            for enemy in self.enemy_list:
                for step in range(search_depth):
                    y, x = self.character.get_player_grid_coordinates()

                    enemy_coords.add(enemy.get_player_grid_coordinates())

                    left_side.add((y, x-step))
                    right_side.add((y, x+step))

            if enemy_coords & left_side:
                self.requested_movement = "RIGHT"
                self.enemy_in_way = True
            elif enemy_coords & right_side:
                self.requested_movement = "LEFT"
                self.enemy_in_way = True
            else:
                self.enemy_in_way = False

            left_side.clear()
            right_side.clear()
            enemy_coords.clear()

    def reconstruct_path(self, search_path_history, end, **kwargs) -> None:
        """ Some algo's will store store contents of every path its
            looked into, in this function we will extract the
            path its found to the target.

        Args:
            search_path_history (list of tuples): A list of all the paths that
                                                  has been looked into.
            end (list): The coord of the diamond.
        """
        final_path = []
        current = end

        while current is not None:
            final_path.append(current)
            current = search_path_history[current]

        final_path.reverse()

        if self.perform_analysis:
            print(f"The path generated is: {final_path}")

        self._path_generated = final_path
        visited_and_path_data_flag.clear()

        return final_path

    def move_based_on_path_instructions(self) -> None:
        """ This function will get the BFS path, then  move the character
        to follow the path it's found. """
        path_to_follow = self.generate_path()

        if self.perform_analysis:
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
        """ This function retrieves and returns the visited list generated by
        whatever algorithm is currently in use. """

        if self.perform_analysis:
            print(f"The list of visited grids is: {self._visited_grids}")

        if (self._visited_grids == [] or self._visited_grids is None):
            print(f"{inspect.currentframe().f_code.co_name}: Cannot get "
                  "visited grids")
            return None

        return self._visited_grids, self._path_generated

    def set_walkable_maze(self, walkable_maze) -> None:
        """ Set the walkable maze matrix with a new one. """
        self._walkable_maze_matrix = walkable_maze

    def update_diamond_list(self, new_diamond_list):
        """ This function is used to update the status of the list of
        diamonds present. """

        # The first case updates status of filled maze, else we are nothing
        # the filled maze and just need to update the single diamond hence the
        # index zero.
        if hasattr(self, "diamond_list"):
            self.diamond_list = new_diamond_list
        else:
            self.diamond_grid_x = new_diamond_list.sprites()[0].grid_x
            self.diamond_grid_y = new_diamond_list.sprites()[0].grid_y


def get_agent_types():
    from agent.informed_computer import (
        UCSComputer,
        AStarComputer,
        AStarFilledComputer,
        GreedyComputer
    )
    from agent.uninformed_computer import (
        RandomComputer, BFSComputer, DFSComputer
    )
    from agent.competitive_computer import (
        MinimaxComputer
    )

    return {
        "random": RandomComputer,
        "bfs": BFSComputer,
        "dfs": DFSComputer,
        "ucs": UCSComputer,
        "astar": AStarComputer,
        "astarFilled": AStarFilledComputer,
        "greedy": GreedyComputer,
        "minimax": MinimaxComputer
    }
