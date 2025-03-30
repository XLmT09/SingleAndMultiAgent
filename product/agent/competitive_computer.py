from agent.computer import Computer
import constants as C
import numpy as np
import time
import copy


class MinimaxComputer(Computer):
    """ This class will represent the agents different pathfinding algos
        available to use.

    Most attributes/args have been explained in the parent class, I will
    mention whats ones specific to minimax.

    Attributes:
        character (MainAnimationManager): The character the computer will
            be controlling.
        state (dict): Representation of the game state and any given moment.
        _agent_type (int): Identifies if the agent is the main or enemy.
        _prev_action (str): stores the previous action the minimax agent has
            taken.
    """
    def __init__(self, character, walkable_maze, **kwargs):
        super().__init__(
            character,
            walkable_maze,
            **kwargs
        )

        self.state = kwargs.get("state", {})

        if kwargs.get("is_main"):
            self._agent_type = 0
        else:
            self._agent_type = 1

        self._prev_action = None
        self.num_characters = kwargs.get("character_list")

    def evaluation_function(self, state, depth, player_action):
        """The function is used to calculate the cost of a game state.

        Attributes:
            state (dict): The current game state.
            depth (int): The current depth of the game tree.
            player_action (str): The action taken by the player.

            Returns:
                int: The score of the state.
        """

        main_agent_pos = state["main_agent"]
        enemy_agent_pos = state["enemies"]
        score = 0

        # if the state ends in a win or lose state, we return -/+infinity
        if state["lose"]:
            return float('-inf')
        if state["win"]:
            return float('inf')

        # Add the bfs distance between the main agent and enemy position of
        # the given state.
        score -= (
            20 / (self.generate_bfs_dist(main_agent_pos, enemy_agent_pos) + 1)
        )

        # Calculate the distance between the main_agents position in the
        # actual game and enemy state position.
        real_dist = self.generate_bfs_dist(
            self.state["main_agent"],
            state["enemies"]
            ) + 1

        # If the distance between the current player pos and state pos of the
        # enemy is close, then add a big negative cost.
        if real_dist <= 4:
            score -= 100
        else:
            score += real_dist

        # For the second set of calculations we will need information about
        # the diamonds, so we will store all there coords in a list.
        diamond_positions = state["diamond_positions"]

        # from all the diamonds in the game, find the closet one.
        closest_diamond = float("inf")
        for diamond in diamond_positions:
            closest_diamond = min(
                closest_diamond,
                self.generate_bfs_dist(main_agent_pos, diamond)
            )

        score += 10 / (closest_diamond + 1) - (5 / (real_dist + 1))

        # We will give awards for the number of diamonds the current state
        # covers for the main agent.
        score += state["diamond_count"]

        return score

    def get_manhattan_distance_filled(self, pos1, pos2) -> int:
        """ This function generates the manhattan distance between two coords
        we pass it.

        Attributes:
            pos1 (tuple): The first position to start the search from. It is
                of the form (grid_y, grid_x).
            pos2 (tuple): The goal position.

        Returns:
            int: The manhattan distance between two points.
        """
        horizontal_diff = abs(pos1[1] - pos2[1])
        vertical_diff = abs(pos1[0] - pos2[0])

        offset = 0

        # Update offset value to the heuristic if there is a height difference,
        # to account for the ladder climbing time.
        # In other words, give more priority to positions which are on the
        # same or neighboring levels.
        if vertical_diff:
            offset += vertical_diff * 10

        return vertical_diff + horizontal_diff + offset

    def generate_bfs_dist(self, pos1, pos2) -> int:
        """ This function uses bfs search to find the closest path between two
        positions.

        Attributes:
            pos1 (tuple): The first position to start the search from. It is
                of the form (grid_y, grid_x).
            pos2 (tuple): The goal position.

        Returns:
            int: The shortest distance between two points.
        """

        # The queue will contain tuples with two arguments:
        #   1. arg1 is a pos tuple
        #   2. arg2 is the current distance that has been covered.
        queue = [(pos1, 0)]
        visited = set()

        while queue:
            current, dist = queue.pop(0)
            visited.add(current)

            if current == pos2:
                return dist

            # Loop through all 4 directions the computer can take
            for direction in self._directions:
                next_grid = (current[0] + direction[0],
                             current[1] + direction[1])

                # Check if the next grid we are looking at is
                # walkable and not visited.
                if (self._walkable_maze_matrix[next_grid[0]][next_grid[1]]
                        != 0 and next_grid not in visited):
                    queue.append((next_grid, dist + 1))

        return float("-inf")

    def manhattan_distance(self, pos1, pos2) -> int:
        """Computes manhattan distance between two points.

        Attributes:
            pos1 (tuple): Represents the first coordinates.
            pos2 (tuple): Represents the second coordinates.

        Returns:
            int: The manhattan distance between two points.
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def legal_movements(self, pos, prev_action) -> list:
        """Determine the legal movements that the agent can perform.

        Args:
            pos (tuple): The (x, y) coordinates of the agent, used to check
                available movement directions.
            prev_action: The previous action taken in the recursive call stack,
                not the actual game movement. This prevents redundant
                backtracking and optimizes the minimax algorithm.

        Returns:
            list: A list of valid movement directions based on the given
                coordinates.
        """
        legal_movements = []

        # Define boundary constraints to check if a move is within the game
        # limits.
        # These values help determine whether a movement is valid or out of
        # bounds.
        LEFT_WALL, RIGHT_WALL = 0, len(self._walkable_maze_matrix[0]) - 1
        CEILING, FLOOR = 0, len(self._walkable_maze_matrix) - 1

        if (pos[1] - 1 > LEFT_WALL and
           self._walkable_maze_matrix[pos[0]][pos[1] - 1] !=
           C.NON_WALKABLE_GRID):
            legal_movements.append("LEFT")

        if (pos[1] + 1 < RIGHT_WALL and
           self._walkable_maze_matrix[pos[0]][pos[1] + 1] !=
           C.NON_WALKABLE_GRID
           and prev_action != "LEFT"):
            legal_movements.append("RIGHT")

        if (pos[0] + 1 < FLOOR and
           self._walkable_maze_matrix[pos[0] + 1][pos[1]] == C.LADDER_GRID
           and prev_action != "UP"):
            legal_movements.append("DOWN")

        if (pos[0] - 1 >= CEILING and
           self._walkable_maze_matrix[pos[0] - 1][pos[1]] == C.LADDER_GRID
           and prev_action != "DOWN"):
            legal_movements.append("UP")

        return legal_movements

    def minimax(self, state, depth, agent_index, player_action=None,
                enemy_action=None) -> tuple:
        """ This function will simulate the minimax algorithm. It will
        simulate movement with both the agent and enemies and find the best
        movement for whichever agent called the algo.

        Attributes:
            state (dict): The current game state.
            depth (int): Number which indicated how far down the game tree
                we are.
            agent_index (int): Indicate which agent is currently running the
                function. 0 means main agent otherwise its the enemy.
            visited_sates (set): Avoid going traversing down repeated states
                by keeping track of states combinations currently visited.
            player_action (str): The action taken by the player.
            enemy_action (str): The action taken by the enemy.

        Returns:
            tuple: A tuple containing the best value and the action to take.
                The best value is the score of the state, and the action is
                the movement to take.
        """

        # end algorithm if we reached max depth or find a terminating state
        if self.is_terminal(state) or depth <= 0:
            return (
                self.evaluation_function(
                    state, depth, player_action
                ), None)

        action_to_take = None

        # Check which agent will run the function next.
        next_agent = (agent_index + 1) % self.num_characters

        # There are two loops we can use to traverse the game tree, one for the
        # main agent and one for the enemy. Each loop will call the minimax
        # algo again on the opposite agent.
        if agent_index == 0:
            best_value = float("-inf")
            for action in self.legal_movements(state["main_agent"],
                                               player_action):

                # Generate the sate for when the action is performed.
                successor = self.generate_successor(state, agent_index, action)

                current_value = self.minimax(
                    successor,
                    depth,
                    agent_index=next_agent,
                    player_action=action,
                    enemy_action=enemy_action
                )[0]

                if best_value <= current_value:
                    best_value = current_value
                    action_to_take = action

            return (best_value, action_to_take)
        else:
            best_value = float("inf")
            if not self.stop_thread:

                for action in self.legal_movements(state["enemies"],
                                                   enemy_action):

                    successor = self.generate_successor(
                        state,
                        agent_index,
                        action
                    )

                    # we decrease the depth here because we at this point both
                    # the player and enemy(s) have made there moves.
                    current_value = self.minimax(
                        successor,
                        depth - 1 if next_agent == 0 else depth,
                        next_agent,
                        player_action=player_action,
                        enemy_action=action
                    )[0]

                    if best_value >= current_value:
                        best_value = current_value
                        action_to_take = action

                return (best_value, action_to_take)
            else:
                return (0, "None")

    def simulate_movement(self, position, action) -> tuple:
        """ This function simulates the movement of the agent.

        Attributes:
            position (tuple): The current position of the agent.
            action (str): The movement to perform.

        Returns:
            tuple: The new position after the movement.
        """
        y, x = position

        if action == "UP":
            return (y - 1, x)
        elif action == "DOWN":
            return (y + 1, x)
        elif action == "LEFT":
            return (y, x - 1)
        elif action == "RIGHT":
            return (y, x + 1)

        # if action was not given return None
        return None

    def is_terminal(self, state) -> bool:
        """ This function checks if the game has reached a terminal state.

        Attributes:
            state (dict): The current game state we will assess.

        Returns:
            bool: True if the game has reached a terminal state, otherwise
                False.
        """
        if len(state["diamond_positions"]) == 0:
            state["win"] = True
        elif state["main_agent"] == state["enemies"]:
            state["lose"] = True

        return state["win"] or state["lose"]

    def generate_successor(self, state, agent, action) -> dict:
        """This function generates a new simulated state.

        Attributes:
            state (dict): The state we will use to generate the successor
                state.
            agent (int): The agent type.
            action (String): The movement we want to perform on the current
                state to create the successor.

        Returns:
            dict: The new state after performing the action.
        """

        # We must copy the state, to avoid modifying values of the original
        # one.
        new_state = copy.deepcopy(state)

        # We need to check which agent to perform the action on
        if agent == 0:
            new_state["main_agent"] = (
                self.simulate_movement(
                    new_state["main_agent"],
                    action
                )
            )

            # If the action leads to diamond overlap, then increment the
            # diamond count. This will be useful a useful heuristic to
            # consider for the evaluation function.
            for dmd in state["diamond_positions"]:
                if dmd == new_state["main_agent"]:
                    new_state["diamond_count"] += 1
        else:
            new_state["enemies"] = (
                self.simulate_movement(
                    new_state["enemies"],
                    action
                )
            )

        return new_state

    def generate_path(self) -> list:
        """
        Minimax is different to other algo is, because it doesn't pre-determine
        the whole path. Instead it just needs to locate the best grid to travel
        to at any given moment.

        In other words it only needs to return a path of length one.

        Returns:
            list: A list with one coord representing the next grid to
                traverse to.
        """
        state_copy = copy.deepcopy(self.state)

        cost, action = self.minimax(
            state_copy,
            depth=2,
            agent_index=self._agent_type
        )

        # we are using state coordinates instead of directly retrieving
        # character coordinates to avoid going into illegal girds.
        next_grid = self.simulate_movement(
            self.character.get_player_grid_coordinates(),
            action=action
        )

        self._prev_action = action

        return [next_grid]

    def move_based_on_path_instructions(self) -> None:
        """ This function will use generate_path to locate the next grid to
        traverse to. Then it will update the requested_movement based on which
        grid to travel towards.
        """
        self.path_to_follow = self.generate_path()

        if self.perform_analysis:
            print(f"The path is: {self.path_to_follow}")
            print(f"Path length is: {len(self.path_to_follow)}")

        climbing = False
        player_position = (self.character.grid_y, self.character.grid_x)

        # Go top the next coord in the path, once coord is reached pop it of
        # the list and exit the function.
        while self.path_to_follow:
            if self.stop_thread:
                print("STOPPING THE COMPUTER THREAD.")
                break

            # Check that the path we have generated is valid a grid, if it is
            # not then clear the list and exit the loop.
            path_coord_y, path_coord_x = self.path_to_follow[0]
            if (self._walkable_maze_matrix[path_coord_y][path_coord_x] == 0):
                self.path_to_follow.pop(0)
                break

            # calculate the position difference between the next coord and
            # current player location, to help decide which direction to take.
            pos_diff = tuple(
                np.subtract(
                    player_position,
                    self.path_to_follow[0]
                )
            )

            # Update the requested movement value, this value will be used by
            # the main thread to control player movement.
            coord1, coord2 = player_position

            # if we are currently on the desired grid or is has a distance
            # greater than 1, then remove the value and calculate a new grid
            # to traverse to.
            if (pos_diff == (0, 0) or
               abs(pos_diff[1]) > 1 or abs(pos_diff[0]) > 1):
                self.path_to_follow.pop(0)
                continue
            # If the agent is climbing and the desired grid is to the left,
            # then do a up left movement.
            if ((climbing and pos_diff[1] > 0) or
               (climbing and self._walkable_maze_matrix[coord1][coord2] == 3
               and pos_diff[1] > 0)):
                self.requested_movement = "UP LEFT"
                time.sleep(2)
                climbing = False
            elif ((climbing and pos_diff[1] < 0) or
                  (climbing and self._walkable_maze_matrix[coord1][coord2] == 3
                   and pos_diff[1] < 0)):
                self.requested_movement = "UP RIGHT"
                time.sleep(2)
                climbing = False
            elif (pos_diff[0] > 0):
                self.requested_movement = "UP"
                climbing = True
            elif (pos_diff[0] < 0 or climbing):
                self.requested_movement = "DOWN"
                climbing = False
            elif (pos_diff[1] > 0 and not climbing):
                self.requested_movement = "LEFT"
            elif (pos_diff[1] < 0 and not climbing):
                self.requested_movement = "RIGHT"

            # update the player position value
            player_position = self.character.get_player_grid_coordinates()

        # Sometimes the player will continue climbing down and out of the maze
        # causing an error. This happens when the requested movement stays as
        # DOWN after leaving the loop. To fix this will force requested
        # movement to be NONE instead.
        if self.requested_movement == "DOWN":
            self.requested_movement = "None"

        return 0

    def perform_path_find(self) -> None:
        """ This functions keeps searching for a path until the stop_thread
        flag is set. """
        while not self.stop_thread:
            self.move_based_on_path_instructions()

    def update_state(self, state) -> None:
        self.state = state
