from agent.computer import Computer


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

    def evaluation_function(self, state, depth):
        main_agent_pos = (
            state["main_agent"]
        )
        enemy_position = (
            state["enemies"]
        )

        diamond_positions = [
            (dmd.grid_y, dmd.grid_x) for dmd in state["diamond_positions"]
        ]
        score = state["score"]

        distance = self.manhattan_distance(main_agent_pos, enemy_position)
        enemy_distance = distance = (
            self.manhattan_distance(main_agent_pos, enemy_position)
        )

        if main_agent_pos == enemy_position:
            return -500

        score -= 1 * (1 + enemy_distance)

        for diamond in diamond_positions:
            distance = self.manhattan_distance(main_agent_pos, diamond)
            score += 10 / (distance + 1) + depth

        return score

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
        legal_movements = set()
        if pos[1] >= len(self._walkable_maze_matrix[0]):
            return legal_movements

        # check if its possible to move to the next grid.
        if (pos[0] >= 0 and
           self._walkable_maze_matrix[pos[0] - 1][pos[1]] == 3):
            legal_movements.add("UP")
        if (pos[1] - 1 > 0 and
           self._walkable_maze_matrix[pos[0]][pos[1] - 1] != 0):
            legal_movements.add("LEFT")
        if (pos[1] + 1 <= len(self._walkable_maze_matrix[0]) and
           self._walkable_maze_matrix[pos[0]][pos[1] + 1] != 0):
            legal_movements.add("RIGHT")
        if (pos[0] + 1 <= len(self._walkable_maze_matrix) and
           self._walkable_maze_matrix[pos[0] + 1][pos[1]] != 0):
            legal_movements.add("DOWN")

        # if self.agent_type == 1:
        #     print(legal_movements)

        return list(legal_movements)

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
            return (self.evaluation_function(state, depth), "None")

        action_to_take = "None"

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
            else:
                return (0, "None")

        return (best_value, action_to_take)

    def simulate_movement(self, position, action):
        y, x = position

        if action == 'UP':
            return (y - 1, x)
        elif action == 'DOWN':
            return (y + 1, x)
        elif action == 'LEFT':
            return (y, x - 1)
        elif action == 'RIGHT':
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

        # we are using state coordinates instead of directly retrieving
        # character coordinates to avoid going into illegal girds.
        next_grid = self.simulate_movement(
            self.state["main_agent"] if self.agent_type == 0
            else self.state["enemies"],
            action=self.minimax(state_copy, depth=2, agent=self.agent_type)[1]
        )

        return [next_grid]

    def perform_path_find(self) -> None:
        """ This functions keeps searching for a path until the stop_thread
        flag is set. """
        while not self.stop_thread:
            self.move_based_on_path_instructions()

    def update_state(self, state):
        self.state = state
