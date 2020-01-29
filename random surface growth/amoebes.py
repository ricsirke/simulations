import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class World:
    def __init__(self, world):
        self.world_shape = world.shape
        self.world = world
        self.empty_block_mark = 0
        self.amoebes = None
        
    def get_neighs(self, pos):
        i = pos[0]
        j = pos[1]
        
        neighs = []
        if i+1 < self.world_shape[0]:
            neighs.append([i+1,j])
        if j+1 < self.world_shape[1]:
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
            ###
            amoebe.perimeter_lengths.append(len(amoebe.perimeters))
            amoebe.block_lengths.append(len(amoebe.blocks))
            ###
            
    def evolve_amoebes(self):
        for amoebe in self.amoebes:
            random_perimeter = amoebe.occupy_random_perimeter()
            if random_perimeter:
                self.occupy_block_by_amoebe(random_perimeter, amoebe)
            ###    
            amoebe.perimeter_lengths.append(len(amoebe.perimeters))
            amoebe.block_lengths.append(len(amoebe.blocks))
            ###
            
    def visualise_amoebes_evolution(self, interval_ms=50, frames=50, output_filename=None, figsize=None, cmap=None):
        fig = plt.figure()
        gs = fig.add_gridspec(2,3)
        
        im_ax = fig.add_subplot(gs[:2, :2])
        
        perimeter_plot_ax = fig.add_subplot(gs[0,2])
        blocks_plot_ax = fig.add_subplot(gs[1,2])
        
        im_ax.axis('off')
        im = im_ax.imshow(self.world, cmap=cmap)
        color_matrix = im.cmap(im.norm(im.get_array()))
        for amoebe in self.amoebes:
            i = amoebe.starting_pos[0]
            j = amoebe.starting_pos[1]
            amoebe.color = matplotlib.colors.to_hex(color_matrix[i,j])
        
        
        perimeter_plots = []
        blocks_plots = []
        self.perimeter_max = 0
        self.block_max = 0
        for amoebe in self.amoebes:
            perimeter_plot, = perimeter_plot_ax.plot(list(range(len(amoebe.perimeter_lengths))), amoebe.perimeter_lengths, color=amoebe.color, linewidth=2)
            perimeter_plots.append(perimeter_plot)
            blocks_plot, = blocks_plot_ax.plot(list(range(len(amoebe.block_lengths))), amoebe.block_lengths, color=amoebe.color, linewidth=2)
            blocks_plots.append(blocks_plot)
            
            if amoebe.perimeter_lengths[-1] > self.perimeter_max:
                self.perimeter_max = amoebe.perimeter_lengths[-1]
            if amoebe.block_lengths[-1] > self.block_max:
                self.block_max = amoebe.block_lengths[-1]
            
        perimeter_plot_ax.set_xlim([0, frames])
        perimeter_plot_ax.set_ylim([0, self.perimeter_max*1.1])
        perimeter_plot_ax.set_xlabel('time')
        perimeter_plot_ax.set_ylabel('perimeters')
        
        blocks_plot_ax.set_xlim([0, frames])
        blocks_plot_ax.set_ylim([0, self.block_max*1.1])
        blocks_plot_ax.set_xlabel('time')
        blocks_plot_ax.set_ylabel('blocks')
        
        plt.tight_layout()
        
        def animate(i):
            self.evolve_amoebes()
            
            im.set_array(self.world)
            
            for i, perimeter_plot in enumerate(perimeter_plots):
                xdata_perimeter = list(range(len(self.amoebes[i].perimeter_lengths)))
                perimeter_plot.set_xdata(xdata_perimeter)
                perimeter_plot.set_ydata(self.amoebes[i].perimeter_lengths)
                
                xdata_blocks = list(range(len(self.amoebes[i].block_lengths)))
                blocks_plots[i].set_xdata(xdata_blocks)
                blocks_plots[i].set_ydata(self.amoebes[i].block_lengths)
                
                if self.amoebes[i].perimeter_lengths[-1] > self.perimeter_max:
                    self.perimeter_max = self.amoebes[i].perimeter_lengths[-1]
                    
                if self.amoebes[i].block_lengths[-1] > self.block_max:
                    self.block_max = self.amoebes[i].block_lengths[-1]
            
            perimeter_plot_ax.set_ylim([0, self.perimeter_max*1.1])
            blocks_plot_ax.set_ylim([0, self.block_max*1.1])
            
            
        anim = FuncAnimation(fig, animate, frames=frames, interval=interval_ms, repeat=False)
        
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
        
        self.perimeter_lengths = [len(self.perimeters)]
        self.block_lengths = [len(self.blocks)]
        
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
        