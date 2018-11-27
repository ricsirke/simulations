import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np


def plotAnim(x, y, T, isSaveVideo=False):
    fig = plt.figure()
    ax1 = plt.axes(xlim=(-1.2, 1.2), ylim=(-1.2, 1.2))
    line, = ax1.plot([], [], 'o')
    line2, = ax1.plot([], [], 'o')

    def init():
        line.set_data([], [])
        line2.set_data([], [])
        return line, line2,
        
    def animate(i):
        line2.set_data(np.transpose(x[:(i%T)]))
        line.set_data(np.transpose(y[:(i%T)]))
        return line, line2,
        
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=T, interval=10, blit=True)
    if isSaveVideo:
        anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
        
    plt.show()
    
    
def plotScatter(x,y):
    for p in x:
        plt.plot(p, 'o')
    for p in y:
        plt.plot(p, 'x')
    plt.show()
