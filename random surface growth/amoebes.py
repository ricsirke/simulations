import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class World:
    def __init__(self, world_size):
        self.world_size = world_size
        self.world = np.zeros((world_size, world_size))
        self.empty_block_mark = 0
        self.amoebes = None

    def get_neighs(self, pos):
        i = pos[0]
        j = pos[1]
        
        neighs = []
        if i+1 < self.world_size:
            neighs.append([i+1,j])
        if j+1 < self.world_size:
            neighs.append([i,j+1])
        if 0 <= i-1:
            neighs.append([i-1,j])
        if 0 <= j-1:
            neighs.append([i,j-1])
        return neighs
    
    def is_free_block(self, pos):
        return self.world[pos[0], pos[1]] == self.empty_block_mark
    
    def get_new_free_neighs(self, pos, perimeters):
        neighs = self.get_neighs(pos)
        
        # filter inner points and old perimeter
        new_perimeters = []
        for neigh in neighs:
            if self.is_free_block(neigh) and neigh not in perimeters:
                new_perimeters.append(neigh)
                
        return new_perimeters
        
    def occupy_block_by_amoebe(self, pos, amoebe):
        self.world[pos[0], pos[1]] = amoebe.mark
        
    def init_amoebes(self, amoebes):
        self.amoebes = amoebes
        for amoebe in amoebes:
            self.occupy_block_by_amoebe(amoebe.starting_pos, amoebe)
            
    def evolve_amoebes(self):
        for amoebe in self.amoebes:
            random_perimeter = amoebe.occupy_random_perimeter()
            if random_perimeter:
                self.occupy_block_by_amoebe(random_perimeter, amoebe)
                    
    def visualise_amoebes_evolution(self, interval_ms=50, frames=50, output_filename=None):
        fig = plt.figure(figsize=(10,10))
        im = plt.imshow(self.world)

        def animate(i):
            self.evolve_amoebes()
            im.set_array(self.world)
            
        anim = FuncAnimation(fig, animate, frames=frames, interval=interval_ms, repeat=False)

        plt.axis('off')
        
        if output_filename:
            anim.save(output_filename)
        else:
            plt.show()



class Amoebe:
    def __init__(self, world, starting_pos, mark):
        self.world = world
        
        self.starting_pos = starting_pos
        self.blocks = [self.starting_pos]
        self.perimeters = self.world.get_new_free_neighs(self.starting_pos, [])
        
        if mark == self.world.empty_block_mark:
            raise Exception
        self.mark = mark
        
    def _pop_random_perimeter(self):
        random_index = np.random.randint(0, len(self.perimeters))
        return self.perimeters.pop(random_index)

    def occupy_random_perimeter(self):
        if len(self.perimeters) > 0:
            random_perimeter = self._pop_random_perimeter()
        else:
            return
        
        while not self.world.is_free_block(random_perimeter):
            if len(self.perimeters) > 0:
                random_perimeter = self._pop_random_perimeter()
            else:
                return
            
        self.blocks.append(random_perimeter)
        new_perimeters = self.world.get_new_free_neighs(random_perimeter, self.perimeters)
        self.perimeters = self.perimeters + new_perimeters
        
        return random_perimeter
        