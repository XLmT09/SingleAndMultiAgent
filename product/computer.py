import threading
import time
import random

moves = ["LEFT", "RIGHT"]

class Computer:
    def __init__(self, character, walkable_maze):
        self.character = character
        self.running = True
        self.requested_random_movement = "RIGHT"
        self._walkable_maze_matrix = walkable_maze

        self.random_movement_thread = threading.Thread(target=self.update_random_movement)
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
    
    # def bfs_path_find(self):

    def move(self, screen, world_data, asset_groups, game_over):
        return self.character.draw_animation(screen, world_data, asset_groups, game_over, self.requested_random_movement)
    
    def set_walkable_maze(self, walkable_maze) -> None:
        self._walkable_maze_matrix = walkable_maze


    