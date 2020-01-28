import numpy as np

import amoebes as Amoebes


world_map = np.zeros((30,30))
world = Amoebes.World(world_map)

starting_point_coord = int(np.floor(world.world_shape[0]/2))
starting_point = [starting_point_coord, starting_point_coord]
amoebe = Amoebes.Amoebe(world, starting_point, mark=1)
amoebe_2 = Amoebes.Amoebe(world, [0,0], mark=2)
amoebes = [amoebe_2, amoebe]

world.init_amoebes(amoebes)
          
world.visualise_amoebes_evolution(interval_ms=50, frames=200, output_filename="anim.mp4")