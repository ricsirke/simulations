import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


NODE_DRAW_SIZE = 50

def calc_interpolated_poses_between(pos, new_pos, Nt):
    interpolated_poses = []
    dt = 1/(Nt-1) 
    t_ax = np.linspace(0, 1, Nt)
    for t in t_ax:
        interpos = {}
        for k in new_pos.keys():
            try:
                interpos[k] = (1-t)*pos[k] + t*new_pos[k]
            except KeyError:
                interpos[k] = new_pos[k]           
        interpolated_poses.append(interpos)
    return interpolated_poses

def calc_interpolated_poses(poses, Nt):
    interpolated_poses = []
    for ind, pos in enumerate(poses[:-1]):
        interpolated_poses_between = calc_interpolated_poses_between(poses[ind], poses[ind+1], Nt)
        interpolated_poses += interpolated_poses_between
    return interpolated_poses

def get_node_color_list(G, node_color_attribute_name, default_color="b"):
    colors = []
    for n in G.node:
        try:
            colors.append(G.node[n][node_color_attribute_name])
        except KeyError:
            colors.append(default_color)
    return colors

def generate_interpolated_graph_evolution_animation(Gs, Nt, interval):
    poses = [nx.spring_layout(Gs[0])]
    for G in Gs[1:]:
        pos = nx.spring_layout(G, pos=poses[-1])
        poses.append(pos)
        
    interpolated_poses = calc_interpolated_poses(poses, Nt)
    
    fig = plt.figure()
    ax = plt.subplot()

    G0 = Gs[0]
    nx.draw(G0,
            pos=interpolated_poses[0],
            edge_color="gray",
            node_size=NODE_DRAW_SIZE,
            node_color=range(len(G0.node)),
            cmap=plt.cm.winter)

    def animate(frame_number):
        ax.clear()
        current_graph = Gs[int(np.ceil(frame_number/Nt))]
        #node_colors = get_node_color_list(current_graph, node_color_attribute_name='color', default_color="b")
        nx.draw(current_graph,
                pos=interpolated_poses[frame_number],
                #node_color=node_colors,
                node_color=range(len(current_graph.node)),
                edge_color="gray",
                node_size=NODE_DRAW_SIZE,
                cmap=plt.cm.winter)

    anim = FuncAnimation(fig, animate, interval=interval, frames=len(interpolated_poses))
    return anim