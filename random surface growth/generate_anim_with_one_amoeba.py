import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


N = 100


world = np.zeros((N, N))


def get_neighs(i,j):
    neighs = []
    if i+1 < N:
        neighs.append([i+1,j])
    if j+1 < N:
        neighs.append([i,j+1])
    if 0 <= i-1:
        neighs.append([i-1,j])
    if 0 <= j-1:
        neighs.append([i,j-1])
    return neighs


starting_point_coord = int(np.floor(N/2))
starting_point = [starting_point_coord, starting_point_coord]
amoebe = [starting_point]
amoebe_mark = 1

world[0,0] = amoebe_mark
perimeters = get_neighs(*starting_point)
           
####################################################################            
fig = plt.figure()
im = plt.imshow(world)
pos_x = 0
pos_y = -8
player_score_text_handle = plt.text(pos_x, pos_y, "blocks: 0")
perimeter_score_text_handle = plt.text(0, -3, "perimeter blocks: 0")
 

def animate(i):
    global perimeters, world, im
    random_index = np.random.randint(0, len(perimeters))
    
    random_perimeter = perimeters.pop(random_index)
    print(random_perimeter)
    neighs = get_neighs(*random_perimeter)
    
    # filter inner points
    new_perimeters = []
    for neigh in neighs:
        if world[neigh[0], neigh[1]] != amoebe_mark and neigh not in perimeters:
            new_perimeters.append(neigh)
    #######
            
    perimeters = perimeters + new_perimeters
    
    world[random_perimeter[0], random_perimeter[1]] = amoebe_mark
    
    
    im.set_array(world)
    player_score_text_handle.set_text("player: " + str(i))
    perimeter_score_text_handle.set_text("perimeter:" + str(len(perimeters)))

    

interval_ms = 50
anim = FuncAnimation(fig, animate, frames=2000, interval = interval_ms, repeat = False)

plt.axis('off')


anim.save("anim.mp4")
####################################################################

#plt.show()
