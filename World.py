import numpy as np
import random
import Actors
import noise


class World:
    def __init__(self, size=100):
        self.rows = size
        self.cols = size
        self.food_count = 0

        # create grid. Everything will take up one grid space.
        self.grid = []
        for i in range(self.rows * self.cols):
            self.grid.append(0)
            if i < 2 * self.rows or i > self.rows * self.cols - 2 * self.rows \
                    or i % self.rows < 2 or i % self.rows > self.rows - 3:
                self.grid[i] = -1

        # use perlin noise to generate realistic terrain:
        scale = 100.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0

        terrain = np.zeros((self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                terrain[i][j] = noise.pnoise2(i / scale,
                                              j / scale,
                                              octaves=octaves,
                                              persistence=persistence,
                                              lacunarity=lacunarity,
                                              repeatx=1024,
                                              repeaty=1024,
                                              base=0)
                if 0 < terrain[i][j] < 0.4 and self.item_from_grid([i, j]) != -1:
                    self.grid[self.list_from_grid([i, j])] = Grass(food=np.random.randint(0, 1))
                elif 0.4 < terrain[i][j] < 0.7 and self.item_from_grid([i, j]) != -1:
                    self.grid[self.list_from_grid([i, j])] = Grass(food=np.random.randint(1, 6))
                elif 0.7 < terrain[i][j] < 1 and self.item_from_grid([i, j]) != -1:
                    self.grid[self.list_from_grid([i, j])] = Grass(food=np.random.randint(6, 10))
                elif -1 < terrain[i][j] < -0.3:
                    self.grid[self.list_from_grid([i, j])] = -1

    def item_to_grid(self, value):
        key = self.grid.index(value)
        return [key // self.rows, key % self.rows]

    def list_from_grid(self, location):
        return location[0] * self.rows + location[1]

    def item_from_grid(self, location):
        return self.grid[location[0] * self.rows + location[1]]

    def find_emptys(self, n):
        return np.random.choice([i for i, x in enumerate(self.grid) if x == 0], n, replace=False)

    def place_items(self, item, number=1):
        place = self.find_emptys(number)
        for i in place:
            new_item = type(item)()
            self.grid[i] = new_item

    def get_type(self, item):
        return [x for x in self.grid if type(x) == type(item)]




class Grass:
    def __init__(self, food=5):
        self.food = np.random.choice(10)
