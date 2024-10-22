import threading
import time
import random
from collections import deque
import numpy as np

moves = ["LEFT", "RIGHT"]

class Computer:
    def __init__(self, character, walkable_maze):
        self.character = character
        self.running = True
        self.requested_movement = "RIGHT"
        self._walkable_maze_matrix = walkable_maze
        # right, down, left, right
        self._directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] 

        self.random_movement_thread = threading.Thread(target=self.move_based_on_path_instructions)
        self.random_movement_thread.daemon = True
        self.random_movement_thread.start()

    def update_random_movement(self):
        # Use this flag to allow the player to descend down a ladder instead of always climbing it 
        climbing = False

        while self.running:
            # Once the player reaches the top of a ladder they can exit by holding the up and right key at the same time
            if (self._walkable_maze_matrix[self.character.grid_y][self.character.grid_x] == 3 and 
                self._walkable_maze_matrix[self.character.grid_y][self.character.grid_x+1] == 1 and
                self._walkable_maze_matrix[self.character.grid_y][self.character.grid_x-1] == 1 and
                climbing):
                self.requested_random_movement = random.choice(["UP RIGHT", "UP LEFT"])
                climbing = False
            elif (self._walkable_maze_matrix[self.character.grid_y][self.character.grid_x] == 3 and 
                self._walkable_maze_matrix[self.character.grid_y][self.character.grid_x+1] == 1 and
                climbing):
                self.requested_random_movement = "UP RIGHT"
                climbing = False
            elif (self._walkable_maze_matrix[self.character.grid_y][self.character.grid_x] == 3 and 
                self._walkable_maze_matrix[self.character.grid_y][self.character.grid_x+1] == 1 and
                climbing):
                self.requested_random_movement = "UP LEFT"
                climbing = False
            elif (self._walkable_maze_matrix[self.character.grid_y][self.character.grid_x] == 3):
                # Once the computer finds a ladder, it'll need to randomly decide to climb it or not
                if (random.randint(0, 1) == 0): 
                    self.requested_random_movement = "UP"
                    climbing = True
            # If the player is about to walk into a wall then force it to move the other way
            elif (self._walkable_maze_matrix[self.character.grid_y][self.character.grid_x - 1] == 0):
                self.requested_random_movement = "RIGHT"
            elif (self._walkable_maze_matrix[self.character.grid_y][self.character.grid_x + 1] == 0):
                self.requested_random_movement = "LEFT"
            else:
                self.requested_random_movement = random.choice(moves)
            time.sleep(1)

    def move_based_on_path_instructions(self):
        path_to_follow = self.bfs_path_find()
        instruction_number = 0
        target = path_to_follow[-1]

        player_position = (self.character.grid_y, self.character.grid_x)

        while player_position != target:
            if instruction_number == len(path_to_follow):
                return
            
            pos_diff = tuple(np.subtract(player_position, path_to_follow[instruction_number]))
            
            if (pos_diff == (0, 0)):
                instruction_number += 1
                continue
            
            if (pos_diff[1] > 0):
                self.requested_movement = "LEFT"
            elif(pos_diff[1] < 0):
                self.requested_movement = "RIGHT"
            
            # update the player position value
            player_position = (self.character.grid_y, self.character.grid_x)
                
            print(player_position)


    
    def bfs_path_find(self) -> list:
        """ This function uses bfs search to find the path to the diamond. """
        start = self.character.get_player_grid_coordinates()
        queue = deque([start])
        visited = {start}
        # This will contain the all the potential paths, bfs has looked into
        search_path_histroy = {start: None}

        while queue:
            current = queue.popleft()

            if self._walkable_maze_matrix[current[0]][current[1]] == 2:
                return self.reconstruct_path(search_path_histroy, current)

            # Loop through all 4 directions the computer can take
            for direction in self._directions:
                next_grid = (current[0] + direction[0], current[1] + direction[1])

                # Check if the next grid we are looking at is walkable and not visited
                if (self._walkable_maze_matrix[next_grid[0]][next_grid[1]] != 0 and next_grid not in visited):
                    queue.append(next_grid)
                    visited.add(next_grid)
                    search_path_histroy[next_grid] = current         

        return None           

    def reconstruct_path(self, search_path_histroy, end) -> None:
        final_path = []
        current = end

        while current is not None:
            final_path.append(current)
            current = search_path_histroy[current]
            
        final_path.reverse()
        return final_path

    def move(self, screen, world_data, asset_groups, game_over):
        return self.character.draw_animation(screen, world_data, asset_groups, game_over, self.requested_movement)
    
    def set_walkable_maze(self, walkable_maze) -> None:
        self._walkable_maze_matrix = walkable_maze


    