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

    def minimax(self, state, depth, agent):
        if self.is_terminal(state) or depth == 0:
            return (self.evaluation_function(state, depth), "None")

        action_to_take = "None"

        if agent == 0:
            best_value = float("-inf")
            for action in self.legal_movements(state["main_agent"]):
                successor = self.generate_successor(state, agent, action)
                current_value = self.minimax(successor, depth - 1, agent=1)[0]
                if best_value < current_value:
                    best_value = current_value
                    action_to_take = action
                    # if action == "UP":
                    #     print("UP")
            # print(f"{action_to_take} and best value {best_value}")
            return (best_value, action_to_take)
        else:
            best_value = float("inf")
            if not self.stop_thread:
                for action in self.legal_movements(state["enemies"]):
                    successor = self.generate_successor(state, agent, action)
                    current_value = (
                        self.minimax(successor, depth - 1, agent=0)[0]
                    )
                    if best_value > current_value:
                        best_value = current_value
                        action_to_take = action
                # print(f"{action_to_take} and best value {best_value}")
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
        new_state = state.copy()
        if agent == 0:
            new_state["main_agent"] = (
                self.simulate_movement(
                    new_state["main_agent"],
                    action
                )
            )
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
            self.minimax(state_copy, depth=5, agent=self.agent_type)[1]
        )

        return [next_grid]

    def perform_path_find(self) -> None:
        """ This functions keeps searching for a path until the stop_thread
        flag is set. """
        while not self.stop_thread:
            self.move_based_on_path_instructions()

    def update_state(self, state):
        self.state = state
