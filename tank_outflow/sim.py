from scipy import integrate
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches




x0, y0 = [0, 0]
h0 = 5
A2 = 1
A1 = 10
rho = 1
g = 10


K = A2 / (rho * A1) * np.sqrt(2*g)

h = lambda t: (-K/2 * t + np.sqrt(h0))**2
v0 = lambda t: np.sqrt( 2*g*h(t) )
y_gen = lambda x, x0, y0, vx0: -g*(x-x0)**2/(2*vx0**2) + y0
y = lambda x, t: y_gen(x, x0, y0, v0(t))

#############################################################################

t0 = 0
dt = 0.008
T = 0.95 * 2*np.sqrt(h0)/K
num_of_frames = int(np.floor((T-t0)/dt))
print("number of frames:", num_of_frames)

x = np.linspace(0, 20, 100)

#----------------------------------------------------------------------------

fig = plt.figure()

rect_water_color = '#6DD2DA'

ax, = plt.plot(x, y(x, t0) , rect_water_color)

rect_water_width = 10
rect_water_height = 10* h0 * rect_water_width / A1
rect_water_pos = (-rect_water_width, 0)

rect_water = patches.Rectangle(rect_water_pos,
                               rect_water_width,
                               rect_water_height,
                               linewidth=1,
                               edgecolor=rect_water_color,
                               facecolor=rect_water_color)

rect_container_pos = rect_water_pos
rect_container_height = rect_water_height
rect_container_width = rect_water_width
rect_container_color = '#E86F2A'

rect_container = patches.Rectangle(rect_container_pos,
                                   rect_container_width,
                                   rect_container_height,
                                   linewidth=2,
                                   edgecolor=rect_container_color,
                                   facecolor='w')

plt.gca().add_patch(rect_container)
plt.gca().add_patch(rect_water)

plt.xlim([-31,30])
plt.ylim([-19,52])

plt.axis('off')


def gen():
    frame_number = 0
    while frame_number < num_of_frames:
        frame_number += 1
        print(frame_number)
        print("number of frames:", num_of_frames)
        yield frame_number

def animate(frame_number):
    t = t0 + frame_number * dt
    ax.set_ydata(y(x,t))
    new_water_height = rect_water_height * h(t) / h0
    rect_water.set_height(new_water_height)

interval_ms = 35
anim = FuncAnimation(fig, animate, frames=num_of_frames, interval=interval_ms, repeat=False)
anim.save('test.mp4')
#plt.show()