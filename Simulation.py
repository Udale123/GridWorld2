import World
import Actors
import pygame
import numpy as np

# simulation parameters
map_size = 100
time_scale = 1
# will automatically produce new random organisms up to this point
lower_population_bound = 30
lower_food_bound = int(map_size ** 2 / 3)
# minimum requirements for reproduction:
reproduction_age = 10
reproduction_energy = 15
# how many children actors should reproduce once they satisfy requirements
max_children = 2
# energy per second to live:
living_cost = 2
# requirements to die:
death_energy = 2
# rate that weights and biases mutate in network:
mutation_rate = 0.05

# statistics
best_age = 0
best_ancestors = 0

# world init
world = World.World(map_size)
world.place_items(Actors.Actor(), lower_population_bound)


# convert world grid coords to pixel coords for finding colour at a point gives left corner pixel
def grid_to_pixel(location, WIDTH, HEIGHT, WINDOW_SIZE):
    return [location[1] * HEIGHT+1,location[0] * WIDTH+1]


# pygame parameters:
WINDOW_SIZE = [1000, 1000]
screen = pygame.display.set_mode(WINDOW_SIZE)
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = int(WINDOW_SIZE[0] / world.cols)
HEIGHT = int(WINDOW_SIZE[1] / world.rows)

pygame.init()
# Set title of screen
pygame.display.set_caption("Grid World")
# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
dt = 0
time_since_last_tick = 0

while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    time_since_last_tick += dt/1000
    if time_since_last_tick > 0:
        # Population Manager:
        pop = world.get_type(Actors.Actor())
        for i in pop:
            if i.alive:
                # 1. reproduction
                if i.age > reproduction_age and i.energy > reproduction_energy and i.child_count < max_children:
                    i.reproduce(world, mutation_rate)
                    i.child_count += 1

                # 2. movement
                location = world.item_to_grid(i)
                # get inputs
                inputs = []
                for m in [-2,-1,1,2]:
                    x = screen.get_at(grid_to_pixel([location[0]+m,location[1]],WIDTH,HEIGHT,WINDOW_SIZE))
                    for k in x[0:3]:
                        inputs.append(k/255)
                    x = screen.get_at(grid_to_pixel([location[0], location[1]+m], WIDTH, HEIGHT, WINDOW_SIZE))
                    for k in x[0:3]:
                        inputs.append(k / 255)
                inputs.append(i.energy/100)
                # get outputs - probabilities of moving to each place
                preferences = i.brain.feed_forward(inputs)
                output = preferences.index(max(preferences))
                # 0 = right #1 = left #2 = up #3 = down

                # move item

                new_location = location.copy()
                if output == 0:
                    new_location[1] = new_location[1] + 1
                elif output == 1:
                    new_location[1] = new_location[1] - 1
                elif output == 2:
                    new_location[0] = new_location[0] + 1
                elif output == 3:
                    new_location[0] = new_location[0] - 1

                # what is in the target square?
                current_occupant = world.item_from_grid(new_location)
                if current_occupant == -1:
                    world.grid[world.grid.index(i)] = 0
                    i.alive = False
                elif type(current_occupant) == World.Grass:
                    i.eat(current_occupant, world)
                    if len(world.get_type(World.Grass())) < lower_food_bound:
                        world.place_items(World.Grass(), 1)
                elif type(current_occupant) == Actors.Actor:
                    i.fight(current_occupant, world)
                elif world.grid[world.list_from_grid(new_location)] == 0:
                    world.grid[world.grid.index(i)] = 0
                    world.grid[world.list_from_grid(new_location)] = i

            # 3. death
            if i.alive:
                i.age += time_since_last_tick*time_scale
                i.energy -= (time_since_last_tick*time_scale * living_cost)
                if i.energy < death_energy:
                    i.die(world)

        # population top up
        if len(pop) < lower_population_bound:
            world.place_items(Actors.Actor(), lower_population_bound - len(pop))
        time_since_last_tick = 0

    # compute max age and energy
    max_ancestors = max([i.ancestor_count for i in world.get_type(Actors.Actor())])
    max_energy = max([i.energy for i in world.get_type(Actors.Actor())])
    if max_ancestors > best_ancestors:
        best_ancestors = max_ancestors
        print(best_ancestors)

    # Draw the world
    for row in range(world.rows):
        for column in range(world.cols):
            if world.item_from_grid([row, column]) == -1:
                color = BLACK
            else:
                color = WHITE

            if type(world.item_from_grid([row, column])) == Actors.Actor:
                color = (int(255 * world.item_from_grid([row, column]).energy / max_energy),0,0)
            elif type(world.item_from_grid([row, column])) == World.Grass:
                color = (0, int(255 * world.item_from_grid([row, column]).food / 9), 0)

            pygame.draw.rect(screen,
                             color,
                             [WIDTH * column,
                              HEIGHT * row,
                              WIDTH,
                              HEIGHT])

    # Limit to 60 frames per second
    dt = clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
