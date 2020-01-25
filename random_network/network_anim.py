import random
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import networkx as nx
import time
import math

NUM_OF_FRAMES = 300
NODE_DRAW_SIZE = 40

graph = nx.Graph()
node_number = 0
graph.add_node(node_number, node_number=node_number)

#degrees = {0: 0}

pos = nx.spring_layout(graph)
pos_prev = pos

fig, ax = plt.subplots(figsize=(8,7))

nx.draw_networkx(graph, pos=pos, node_color="green", ax=ax, node_size=NODE_DRAW_SIZE, with_labels=False)


nodes_number_text_handle = plt.text(0.02, -0.01, "number of nodes: 0", horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
#plt.show()


def animate(frame):
    global graph, node_number, degrees, pos_prev, nodes_number_text_handle, NUM_OF_FRAMES
    print(int(math.floor(frame*100 / NUM_OF_FRAMES)), " %")
    node_number += 1
    nodes = graph.nodes()
    random_node_index = random.randrange(len(nodes))
    random_node = nodes[random_node_index]
    random_node_number = random_node['node_number']
    #degrees[node_number] = 1
    #degrees[random_node_number] += 1
    
    new_edge = (node_number, random_node_number)
    
    graph.add_node(node_number, node_number=node_number)
    graph.add_edge(*new_edge)
    
    pos = nx.spring_layout(graph, pos=pos_prev, iterations=30)
    
    plt.cla()
    nx.draw_networkx(graph, ax=ax, node_color=range(len(nodes)), edge_color="gray", pos=pos, node_size=NODE_DRAW_SIZE, with_labels=False, cmap=plt.cm.winter)
    plt.text(0.02, -0.01, "number of nodes: " + str(node_number), horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
    
    pos_prev = pos
    
ani = FuncAnimation(fig, animate, frames=NUM_OF_FRAMES, interval=200, repeat=False)
ani.save('netw_anim.mp4')

#plt.show()