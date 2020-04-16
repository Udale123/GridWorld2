import NeuralNetwork as nn
import numpy as np
import World


class Actor:
    def __init__(self, age=0, energy=10, sight=2):
        self.age = age
        self.energy = energy
        self.brain = nn.NeuralNetwork([24, 40, 4])
        self.sight = sight
        self.alive = True
        self.child_count = 0
        self.ancestor_count = 0

    def eat(self, grass, world):
        self.energy += grass.food
        world.grid[world.grid.index(self)] = 0
        world.grid[world.grid.index(grass)] = self

    def reproduce(self, world, mutation_rate=0.05):
        self.energy -= 10
        location = world.item_to_grid(self)
        child = Actor()
        child.ancestor_count = self.ancestor_count + 1
        # copy weights and biases from network and mutate:
        child.brain.NeuronBias = self.brain.NeuronBias
        child.brain.weights = self.brain.weights
        child.brain.mutate(mutation_rate)

        new_location = [location[0] + np.random.choice([-1, 1]), location[1] + np.random.choice([-1, 1])]
        new_location_current = world.item_from_grid(new_location)
        if type(new_location_current) == Actor:
            new_location_current.die(world)
            world.grid[world.list_from_grid(new_location)] = child
        elif type(new_location_current) == World.Grass:
            child.energy += new_location_current.food
            world.grid[world.list_from_grid(new_location)] = child
        elif new_location_current != -1:
            world.grid[world.list_from_grid(new_location)] = child

    def die(self, world):
        world.grid[world.grid.index(self)] = World.Grass(self.energy + 2)
        self.alive = False

    def fight(self, enemy, world):
        total_energy = self.energy + enemy.energy
        winner = np.random.choice([0, 1], p=[enemy.energy / total_energy, self.energy / total_energy])
        if winner == 0:
            self.die(world)
        else:
            idx = world.grid.index(enemy)
            self.energy += enemy.energy
            enemy.die(world)
            world.grid[world.grid.index(self)] = 0
            world.grid[idx] = self
