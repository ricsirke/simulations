import numpy as np

import time
import util as u

# simulation parameters
dt = 0.1       # time step
T = 3000       # number of time steps

# parameters of the system
gamma = .00002 # gravitational coefficient
m1 = 300       # mass of the first planet
m2 = 1         # mass of the second planet

# initial conditions: state of the system in the first two time steps
x0 = np.array([0, 0, 1, 0])
x1 = np.array([0, 0, 1, 0.005])

# initializing the vector of system states
xs = [x0, x1]

# defining the function that calculates the forces acting on the planets at a time step
def F(x):
    r1 = x[:2]   # position of the first planet
    r2 = x[2:4]  # position of the second planet
    
    posdiff_vec = r2 - r1                 # vector of difference of the positions
    dist = np.linalg.norm(posdiff_vec)    # distance between the planets
    
    # Newton's law of universal gravitation
    F1 = gamma * m2 * posdiff_vec / (dist**2)    # force acting on the first planet
    F2 = - gamma * m1 * posdiff_vec / (dist**2)  # force acting on the second planet
    
    return np.concatenate([F1, F2], axis=0)


for i in range(T):
    # getting previous values of the iteration
    Lx = xs[-1]
    LLx = xs[-2]
    
    # approximating the second derivative with finite differences
    F_prev = F(Lx)                  # force acting at the previous time step
    x = dt**2*F_prev + 2*Lx - LLx   # estimated position at the next time step
    
    xs.append(x)

####################################################

x, y = np.split(np.array(xs), 2, axis=1)

u.plotAnim(x, y, T, isSaveVideo=False)

# this is slow and not working properly
#u.plotScatter(x, y)
