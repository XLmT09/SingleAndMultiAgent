import heapq

from agent.computer import Computer
from queue import PriorityQueue
from collections import deque


class InformedComputer(Computer):
    """ This computer class will hold similar characteristics between different
    informed search algorithms. """

    def __init__(self, character, walkable_maze, **kwargs):
        super().__init__(character, walkable_maze, **kwargs)

    def generate_path(self) -> list:
        """ This function generates a path leading to the diamond. """

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
                    self.tracker.total_nodes_visited += len(visited)
                    if not self.character.in_filled_maze:
                        print(
                            f"The number of visited nodes is: {len(came_from)}"
                        )

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

            if self.heuristic == "manhattan":
                new_cost += self.get_manhattan_distance(neighbour)
            elif self.heuristic == "weighted_manhattan":
                new_cost += self.get_weighted_manhattan_distance(neighbour)

            neighbours.append((new_cost, neighbour))

        # sort neighbour from low to high using the cost value
        return sorted(neighbours, key=lambda x: x[0])

    def get_manhattan_distance(self, neighbour) -> int:
        """ This function gets the manhattan distance between player
        current pos and goal. """
        horizontal_diff = abs(neighbour[1] - self.diamond_grid_x)
        vertical_diff = abs(neighbour[0] - self.diamond_grid_y)

        offset = 0

        if vertical_diff:
            offset += vertical_diff * 4

        return vertical_diff + horizontal_diff + offset

    def get_weighted_manhattan_distance(self, neighbour) -> int:
        """ This function gets the manhattan distance between player
        current pos and goal. """
        return ((abs(neighbour[1] - self.diamond_grid_x) +
                abs(neighbour[0] - self.diamond_grid_y)) *
                self.MANHATTAN_WEIGHT)

    def get_manhattan_distance_filled(self, pos1=None, pos2=None) -> int:
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
            offset += vertical_diff * 5

        return vertical_diff + horizontal_diff + offset


class AStarFilledComputer(InformedComputer):
    def __init__(self, character, walkable_maze, **kwargs):
        super().__init__(
            character,
            walkable_maze,
            **kwargs
        )

        self.MANHATTAN_WEIGHT = 2
        self.mst_edges = []

        self.diamond_list = kwargs.get("diamond_list")

        if kwargs.get("is_weighted", False):
            self.heuristic = "weighted_manhattan"
        else:
            self.heuristic = "manhattan"

    def generate_mst(self) -> list:
        """ This generates all the edges of the minimum spanning tree.
        The MST will act as heuristic for some path finding algorithms."""

        start = self.character.get_player_grid_coordinates()
        visited = set()

        # key points are all the diamond position
        key_points = [
            (diamond.grid_y, diamond.grid_x) for diamond in self.diamond_list
        ]

        # The heap data struct that will store the POSSIBLE costs between
        # key points.
        min_heap = []

        # This will contain all the edges for the final MST, so there will be
        # no cycles.
        self.mst_edges = []

        min_cost = float('inf')
        first_diamond = None

        # This dict will store the lowest cost we can find between two points.
        # It doesn't guarantee we find its partner (point) with the lowest cost
        # for various reasons. For example, the globally lowest partner point
        # has already been visited.
        edge_map = {}

        # Before staring the algorithm we will first find the diamond with the
        # lowest cost from the players start position.
        for diamond_pos in key_points:
            cost = self.get_manhattan_distance_filled(start, diamond_pos)

            if cost < min_cost:
                edge_map[start] = (cost, diamond_pos)
                min_cost = cost
                first_diamond = diamond_pos

        # push the diamond with the lowest cost from the start to the heap
        heapq.heappush(min_heap, (min_cost, start, first_diamond))

        # Now we start running the MST algo
        while min_heap:
            cost, coord_1, coord_2 = heapq.heappop(min_heap)

            if coord_2 in visited:
                continue

            # We found the shortest coord from coord_1, now we need to go find
            # the next shortest cost coord from coord_2.
            self.mst_edges.append((coord_1, coord_2))
            visited.add(coord_2)

            new_point, min_cost = None, float('inf')

            # This loop is similar to what we done earlier, but this time find
            # the diamond with the lowest cost from coord_2.
            for point in key_points:
                new_cost = self.get_manhattan_distance_filled(coord_2, point)
                if point not in visited and new_cost < min_cost:
                    new_point = point
                    min_cost = new_cost
                    edge_map[new_point] = (new_cost, coord_2)

            # once we find the next coord pair, push it to the heap
            if new_point:
                heapq.heappush(
                    min_heap,
                    (
                        edge_map[new_point][0],
                        coord_2,
                        new_point
                    )
                )

        return self.mst_edges

    def generate_path(self) -> list:
        """ This function uses ucs search to find the path to the diamond. """

        if not self.mst_edges:
            self.mst_edges = self.generate_mst()

        goal = (0, 0)

        while self._walkable_maze_matrix[goal[0]][goal[1]] != 2:
            goal = self.mst_edges.pop(0)[1]
            self.diamond_grid_y, self.diamond_grid_x = goal

        return super().generate_path()


class AStarComputer(InformedComputer):
    def __init__(self, character, walkable_maze, **kwargs):
        super().__init__(
            character,
            walkable_maze,
            **kwargs
        )

        self.MANHATTAN_WEIGHT = 2

        diamond = kwargs.get("diamond")
        self.diamond_grid_x = diamond.grid_x
        self.diamond_grid_y = diamond.grid_y

        if kwargs.get("is_weighted", False):
            self.heuristic = "weighted_manhattan"
        else:
            self.heuristic = "manhattan"


class GreedyComputer(InformedComputer):
    def __init__(self, character, walkable_maze, **kwargs):
        super().__init__(
            character,
            walkable_maze,
            **kwargs,
        )
        self.heuristic = None
        self.diamond_list = kwargs.get("diamond_list")

    def generate_path(self) -> list:
        """ This function uses the manhattan distance to get the closet
        diamond, then it will use bfs to get the path to that diamond."""

        start = self.character.get_player_grid_coordinates()
        goal = self.get_manhattan_distance_of_all_diamonds()
        queue = deque([start])
        visited = []
        # This will contain the all the potential paths, bfs has looked into
        search_path_history = {start: None}

        while queue:
            current = queue.popleft()
            visited.append(current)

            if current == goal:
                self._visited_grids = visited

                if self.perform_analysis:
                    self.tracker.total_nodes_visited += len(visited)
                    if not self.character.in_filled_maze:
                        print(
                            f"The number of visited nodes is: {len(visited)}"
                        )

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

    def get_manhattan_distance_of_all_diamonds(self) -> tuple:
        """ This function returns the coordinates of the diamond with the
        shortest manhattan distance in a filled maze."""

        current_target = (-1, -1)
        distance = shortest_distance = 1000000

        for diamond in self.diamond_list:
            distance = (abs(self.character.grid_x - diamond.grid_x) +
                        abs(self.character.grid_y - diamond.grid_y))

            if distance < shortest_distance:
                shortest_distance = distance
                current_target = (diamond.grid_y, diamond.grid_x)

        return current_target
