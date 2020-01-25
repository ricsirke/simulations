import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


N = 20
EMPTY_MARK = 0

world = np.zeros((N, N))


def get_neighs(pos):
    i = pos[0]
    j = pos[1]
    
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
    
def is_free_block(pos):
    return world[pos[0], pos[1]] == EMPTY_MARK
    
def get_new_free_neighs(pos, perimeters):
    neighs = get_neighs(pos)
    
    # filter inner points and old perimeter
    new_perimeters = []
    for neigh in neighs:
        if is_free_block(neigh) and neigh not in perimeters:
            new_perimeters.append(neigh)
            
    return new_perimeters
    



class Amoebe:
    def __init__(self, starting_pos, mark):
        self.starting_pos = starting_pos
        self.blocks = [self.starting_pos]
        self.perimeters = get_new_free_neighs(self.starting_pos, [])
        self.mark = mark
        
    def _pop_random_perimeter(self):
        random_index = np.random.randint(0, len(self.perimeters))
        return self.perimeters.pop(random_index)

    def occupy_random_perimeter(self):
        random_perimeter = self._pop_random_perimeter()
        while not is_free_block(random_perimeter):
            random_perimeter = self._pop_random_perimeter()
            
        self.blocks.append(random_perimeter)
        new_perimeters = get_new_free_neighs(random_perimeter, self.perimeters)
        self.perimeters = self.perimeters + new_perimeters
        return random_perimeter

        

starting_point_coord = int(np.floor(N/2))
starting_point = [starting_point_coord, starting_point_coord]
amoebe = Amoebe(starting_point, mark=1)
amoebe_2 = Amoebe([0,0], mark=2)


amoebes = [amoebe_2, amoebe]
amoebe_marks = [amoebe.mark for amoebe in amoebes]

for amoebe in amoebes:
    world[amoebe.starting_pos[0], amoebe.starting_pos[1]] = amoebe.mark
          
           
####################################################################            
fig = plt.figure()
im = plt.imshow(world)
#score_pos_x = 0
#score_pos_y = -8
#player_score_text_handle = plt.text(score_pos_x, score_pos_y, "blocks: 0")
#perimeter_score_text_handle = plt.text(score_pos_x, score_pos_y+5, "perimeter blocks: 0")

def animate(i):
    global world
    
    for amoebe in amoebes:
        if len(amoebe.perimeters) > 0:
            random_perimeter = amoebe.occupy_random_perimeter()
            world[random_perimeter[0], random_perimeter[1]] = amoebe.mark
    
    
    im.set_array(world)
    #player_score_text_handle.set_text("amoebe: " + str(len(amoebe.blocks)))
    #perimeter_score_text_handle.set_text("perimeter:" + str(len(amoebe.perimeters)))

interval_ms = 50
anim = FuncAnimation(fig, animate, frames=200, interval=interval_ms, repeat=False)

plt.axis('off')


anim.save("anim.mp4")
####################################################################

#plt.show()
