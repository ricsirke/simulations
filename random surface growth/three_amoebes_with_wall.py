import numpy as np

import amoebes as Amoebes

N = 28
interval_ms = 50
wait_in_sec = 5
repeat = 5

for i in range(repeat):
    world_map = np.zeros((N,N))

    # wall
    for n in range(int(N/2), N):
        world_map[n,int(N/2)] = -1

    world = Amoebes.World(world_map)


    amoebe = Amoebes.Amoebe(world, [int(N/4),int(N/2)], mark=1)
    amoebe_2 = Amoebes.Amoebe(world, [3*int(N/4),int(N/4)], mark=2)
    amoebe_3 = Amoebes.Amoebe(world, [3*int(N/4),3*int(N/4)], mark=3)
    amoebes = [amoebe_2, amoebe, amoebe_3]

    world.init_amoebes(amoebes)       

    frames = int(N**2 / len(amoebes))
    print("number of frames:", frames)

    duration = frames*interval_ms / 1000
    print("video duration:", str(duration), "seconds")


    num_of_additional_frames = (wait_in_sec / (interval_ms/1000))
    num_of_additional_frames = int(num_of_additional_frames)
    
    filename = "anim" + str(i) + ".mp4"
    world.visualise_amoebes_evolution(interval_ms=interval_ms, frames=frames+num_of_additional_frames, cmap="rainbow", output_filename=filename, figsize=(10,10))