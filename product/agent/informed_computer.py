from agent.computer import Computer
from queue import PriorityQueue


class InformedComputer(Computer):
    """ This computer class will hold similar characteristics between different
    informed search algorithms. """

    def __init__(self, character, walkable_maze, perform_analysis):
        super().__init__(character, walkable_maze, perform_analysis)

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
            if self._walkable_maze_matrix[current[0]][current[1]] == 2:
                self._visited_grids = visited
                if self.perform_analysis:
                    print(f"The number of visited nodes is: {len(came_from)}")

                return self.reconstruct_path(came_from, current)

            # Loop through the neighbours of the current vertex and add to
            # the fringe if its not been recorded in the costs dict, or if it
            # has been recorded then see if it can grant as a lower path cost.
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
            neighbour_grid_value = (
                self._walkable_maze_matrix[neighbour[0]][neighbour[1]]
            )

            # If the neighbour is a wall or floor then skip
            if (neighbour_grid_value == 0):
                continue

            # Check if the neighbour is a empty space or a ladder
            if (neighbour_grid_value == 1 or neighbour_grid_value == 3):
                new_cost = cost + 1
            # Check of the neighbour is a slow tile
            elif (neighbour_grid_value == 4):
                new_cost = cost + 3

            if self.heuristic == "manhattan":
                new_cost += self.get_manhattan_distance()

            neighbours.append((new_cost, neighbour))

        # sort neighbour from low to high using the cost value
        return sorted(neighbours, key=lambda x: x[0])


class UCSComputer(InformedComputer):
    def __init__(self, character, walkable_maze, **kwargs):
        super().__init__(
            character,
            walkable_maze,
            kwargs.get("perform_analysis", False)
        )
        self.heuristic = None


class AStarComputer(InformedComputer):
    def __init__(self, character, walkable_maze, **kwargs):
        super().__init__(
            character,
            walkable_maze, 
            kwargs.get("perform_analysis", False)
        )
        diamond = kwargs.get("diamond")
        self.diamond_grid_x = diamond.grid_x
        self.diamond_grid_y = diamond.grid_y
        self.heuristic = "manhattan"

    def get_manhattan_distance(self) -> int:
        """ This function gets the manhattan distance between player
        current pos and goal. """
        return (abs(self.character.grid_x - self.diamond_grid_x) +
                abs(self.character.grid_y - self.diamond_grid_y))
