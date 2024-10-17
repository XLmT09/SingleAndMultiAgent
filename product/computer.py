import threading
import time
import random

data = [
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

moves = ["LEFT", "RIGHT"]

class Computer:
    def __init__(self, character, maze_map):
        self.character = character
        self.maze_map = maze_map
        self.character_map = [[0 for _ in range(len(maze_map[0]))] for _ in range(len(maze_map))]

        self.fill_map_with_walkable_areas()

        self.running = True
        self.requested_random_movement = "RIGHT"
        self.random_movement_thread = threading.Thread(target=self.update_random_movement)
        self.random_movement_thread.daemon = True
        self.random_movement_thread.start()
    
    def fill_map_with_walkable_areas(self):
        for i in range(len(self.maze_map)):
            for j in range(len(self.maze_map[0])):
                if(self.maze_map[i][j] == 0):
                    if ((i - 1 >= 0) and (j - 1 >= 0) and (i + 1 < len(self.maze_map)) and (j + 1 < len(self.maze_map[0]))):
                        if ((self.maze_map[i-1][j] == 1) and (self.maze_map[i + 1][j] == 1)):
                            self.character_map[i][j] = 1
                if(self.maze_map[i][j] == 3):
                    self.character_map[i][j] = 3
        
        print(*self.character_map, sep="\n")

    def update_random_movement(self):
        # Use this flag to allow the player to descend down a ladder instead of always climbing it 
        climbing = False

        while self.running:
            # Once the player reaches the top of a ladder they can exit by holding the up and right key at the same time
            if (self.character_map[self.character.grid_y][self.character.grid_x] == 3 and 
                self.character_map[self.character.grid_y][self.character.grid_x+1] == 1 and
                self.character_map[self.character.grid_y][self.character.grid_x-1] == 1 and
                climbing):
                self.requested_random_movement = random.choice(["UP RIGHT", "UP LEFT"])
                climbing = False
            elif (self.character_map[self.character.grid_y][self.character.grid_x] == 3 and 
                self.character_map[self.character.grid_y][self.character.grid_x+1] == 1 and
                climbing):
                self.requested_random_movement = "UP RIGHT"
                climbing = False
            elif (self.character_map[self.character.grid_y][self.character.grid_x] == 3 and 
                self.character_map[self.character.grid_y][self.character.grid_x+1] == 1 and
                climbing):
                self.requested_random_movement = "UP LEFT"
                climbing = False
            elif (self.character_map[self.character.grid_y][self.character.grid_x] == 3):
                # Once the computer finds a ladder, it'll need to randomly decide to climb it or not
                if (random.randint(0, 1) == 0): 
                    self.requested_random_movement = "UP"
                    climbing = True
            # If the player is about to walk into a wall then force it to move the other way
            elif (self.character_map[self.character.grid_y][self.character.grid_x - 1] == 0):
                self.requested_random_movement = "RIGHT"
            elif (self.character_map[self.character.grid_y][self.character.grid_x + 1] == 0):
                self.requested_random_movement = "LEFT"
            else:
                self.requested_random_movement = random.choice(moves)
            time.sleep(1)

    def move(self, screen, world_data, asset_groups, game_over):
        return self.character.draw_animation(screen, world_data, asset_groups, game_over, self.requested_random_movement)


    