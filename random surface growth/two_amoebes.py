import numpy as np

import Amoebes


world_size = 30
world = Amoebes.World(world_size=world_size)        

starting_point_coord = int(np.floor(world.world_size/2))
starting_point = [starting_point_coord, starting_point_coord]
amoebe = Amoebes.Amoebe(world, starting_point, mark=1)
amoebe_2 = Amoebes.Amoebe(world, [0,0], mark=2)
amoebes = [amoebe_2, amoebe]

world.init_amoebes(amoebes)
          
world.visualise_amoebes_evolution(interval_ms=50, frames=500, output_filename="anim.mp4")