import numpy as np

import Amoebes


world_size = 30
world = Amoebes.World(world_size=world_size)        

starting_point_coord = int(np.floor(world.world_size/2))
starting_point = [starting_point_coord, starting_point_coord]
amoebe = Amoebes.Amoebe(world, starting_point, mark=1)
amoebe_2 = Amoebes.Amoebe(world, [0,0], mark=2)
amoebe_3 = Amoebes.Amoebe(world, [world_size-1,0], mark=3)
amoebe_4 = Amoebes.Amoebe(world, [0,world_size-1], mark=4)
amoebe_5 = Amoebes.Amoebe(world, [world_size-1,world_size-1], mark=5)
amoebes = [amoebe_2, amoebe, amoebe_3, amoebe_4, amoebe_5]

world.init_amoebes(amoebes)
          
world.visualise_amoebes_evolution(interval_ms=50, frames=200, output_filename="anim.mp4")