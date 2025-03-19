from agent.computer import Computer
import numpy as np
import time


class MinimaxComputer(Computer):
    def __init__(self, character, walkable_maze, **kwargs):
        super().__init__(
            character,
            walkable_maze,
            **kwargs
        )

        self.state = kwargs.get("state", {})
        if kwargs.get("is_main"):
            self.agent_type = 0
        else:
            self.agent_type = 1

    def evaluation_function(self, state):
        """The function is used to calculate the cost of a game state."""

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
        score += self.generate_bfs_dist(main_agent_pos, enemy_agent_pos)

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

        # We will also use manhattan for our evaluation
        score += self.manhattan_distance(main_agent_pos, enemy_agent_pos)

        # For the second set of calculations we will need information about
        # the diamonds, so we will store all there coords in a list.
        diamond_positions = [
            (dmd.grid_y, dmd.grid_x) for dmd in state["diamond_positions"]
        ]

        # from all the diamonds in the game, find the closet one.
        closest_diamond = float("inf")
        for diamond in diamond_positions:
            closest_diamond = min(
                closest_diamond,
                self.generate_bfs_dist(main_agent_pos, diamond)
            )

        score += 5000 / (closest_diamond + 1)

        # We will give awards for the number of diamonds the current state
        # covers for the main agent.
        score += state["diamond_count"]

        return score

    def get_manhattan_distance_filled(self, pos1, pos2) -> int:
        """ This function generates the manhattan distance between two coords
        we pass it. """
        horizontal_diff = abs(pos1[1] - pos2[1])
        vertical_diff = abs(pos1[0] - pos2[0])

        offset = 0

        # update offset value to the heuristic if there is a height difference,
        # to account for the ladder climbing time.
        # In other words, give more priority to positions which are on the
        # same or neighboring levels.
        if vertical_diff:
            offset += vertical_diff * 10

        return vertical_diff + horizontal_diff + offset

    def generate_bfs_dist(self, pos1, pos2) -> list:
        """ This function uses bfs search to find the closest path between two
        positions.

        Attributes:
            pos1 (tuple): The first position to start the search from. It is
            of the form (grid_y, grid_x).
            pos2 (tuple): The goal position.
        """
        # The queue will contain tuples with two arguments.
        # arg1 is a pos tuple
        # arg2 is the current distance that has been covered.
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

        return None

    def manhattan_distance(self, pos1, pos2):
        """Computes Manhattan distance between two points."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def legal_movements(self, pos):
        """Find the legal movements that the agent can perform."""
        legal_movements = []

        if (pos[1] - 1 > 1 and
           self._walkable_maze_matrix[pos[0]][pos[1] - 1] != 0):
            legal_movements.append("LEFT")
        if (pos[1] + 1 < len(self._walkable_maze_matrix[0]) - 1 and
           self._walkable_maze_matrix[pos[0]][pos[1] + 1] != 0):
            legal_movements.append("RIGHT")
        if (pos[0] + 1 < len(self._walkable_maze_matrix) - 1 and
           self._walkable_maze_matrix[pos[0] + 1][pos[1]] == 3):
            legal_movements.append("DOWN")
        if (pos[0] - 1 >= 1 and
           self._walkable_maze_matrix[pos[0] - 1][pos[1]] == 3):
            legal_movements.append("UP")

        return legal_movements

    def minimax(self, state, depth, agent, visited_states=None):
        """ This function will simulate the minimax algorithm. It will
        simulate movement with both the agent and enemies and find the best
        movement for whichever agent called the algo.

        Attributes:
            state (dict): The current game state.
            depth (int): Number which indicated how far down the game tree
                we are.
            agent (int): Indicate which agent is currently running the
                function. 0 means main agent otherwise its the enemy.
            visited_sates (set): Avoid going traversing down repeated states
                by keeping track of states combinations currently visited.
        """
        if visited_states is None:
            visited_states = set()

        state_tuple = (tuple(state["main_agent"]), tuple(state["enemies"]))
        if state_tuple in visited_states:
            return (self.evaluation_function(state, depth), "None")

        visited_states.add(state_tuple)

        # end algorithm if we reached max depth or find a terminating state
        if self.is_terminal(state) or depth <= 0:
            return (self.evaluation_function(state, depth), None)

        action_to_take = None

        if agent == 0:
            best_value = float("-inf")
            for action in self.legal_movements(state["main_agent"]):
                successor = self.generate_successor(state, agent, action)

                current_value = self.minimax(
                    successor,
                    depth,
                    agent=1,
                    visited_states=visited_states
                )[0]

                if best_value <= current_value:
                    best_value = current_value
                    action_to_take = action
            return (best_value, action_to_take)
        else:
            best_value = float("inf")
            if not self.stop_thread:

                for action in self.legal_movements(state["enemies"]):
                    successor = self.generate_successor(state, agent, action)

                    # we decrease the depth here because we at this point both
                    # the player and enemy(s) have made there moves.
                    current_value = self.minimax(
                        successor,
                        depth - 1,
                        agent=0,
                        visited_states=visited_states
                    )[0]

                    if best_value >= current_value:
                        best_value = current_value
                        action_to_take = action

                return (best_value, action_to_take)
            else:
                return (0, "None")

    def simulate_movement(self, position, action):
        y, x = position

        if action == "UP":
            return (y - 1, x)
        elif action == "DOWN":
            return (y + 1, x)
        elif action == "LEFT":
            return (y, x - 1)
        elif action == "RIGHT":
            return (y, x + 1)

        return position

    def is_terminal(self, state):
        if len(state["diamond_positions"]) == 0:
            state["win"] = True
        elif state["main_agent"] == state["enemies"]:
            state["lose"] = True
        return state["win"] or state["lose"]

    def generate_successor(self, state, agent, action):
        """This function generates a new simulated state.

        Attributes:
            state (dict): The state we will use to generate the successor
                state.
            agent (int): The agent type.
            action (String): The movement we want to perform on the current
                state to create the successor.
        """

        # We must copy the state, to avoid modifying values of the original
        # one.
        new_state = state.copy()

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
                if (dmd.grid_y, dmd.grid_x) == new_state["main_agent"]:
                    new_state["diamond_count"] += 1
        else:
            new_state["enemies"] = (
                self.simulate_movement(
                    new_state["enemies"],
                    action
                )
            )

        return new_state

    def generate_path(self):
        """
        Minimax is different to other algo is, because it doesn't pre-determine
        the whole path. Instead it just needs to locate the best grid to travel
        to at any given moment.

        In other words it only needs to return a path of length one.
        """
        state_copy = self.state.copy()

        cost, action = self.minimax(state_copy, depth=3, agent=self.agent_type)

        # we are using state coordinates instead of directly retrieving
        # character coordinates to avoid going into illegal girds.
        next_grid = self.simulate_movement(
            self.character.get_player_grid_coordinates(),
            action=action
        )

        return [next_grid]

    def move_based_on_path_instructions(self) -> None:
        """ This function will get the BFS path, then  move the character
        to follow the path it's found. """
        self.path_to_follow = self.generate_path()

        print(self.path_to_follow)
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

            # If for some reason the enemy is very close to us then generate a
            # new coord to go to.
            if self.enemy_in_way:
                self.path_to_follow = self.generate_path()
                continue

            # Check that the path we have generated is valid a grid, if it is
            # not then clear the list and exit the loop.
            path_coord_y, path_coord_x = self.path_to_follow[0]
            if self._walkable_maze_matrix[path_coord_y][path_coord_x] == 0:
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

            # update the requested movement value, this value will be used by
            # the main thread to control player movement.
            coord1, coord2 = player_position

            if (pos_diff == (0, 0) or
               abs(pos_diff[1]) > 1 or abs(pos_diff[0]) > 1):
                self.path_to_follow.pop(0)
                continue
            if (climbing and (pos_diff[1] > 0 and
               self._walkable_maze_matrix[coord1][coord2] == 3)):
                self.requested_movement = "UP LEFT"
                time.sleep(2)
                climbing = False
            elif (climbing and (pos_diff[1] < 0 and
                  self._walkable_maze_matrix[coord1][coord2] == 3)):
                self.requested_movement = "UP RIGHT"
                time.sleep(2)
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

        return 0

    def perform_path_find(self) -> None:
        """ This functions keeps searching for a path until the stop_thread
        flag is set. """
        while not self.stop_thread:
            self.move_based_on_path_instructions()

    def update_state(self, state):
        self.state = state
