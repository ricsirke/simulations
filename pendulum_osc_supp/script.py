# -*- coding: utf-8 -*-

import numpy as np
from scipy.integrate import solve_ivp

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


FPS = 30

def solve_pend_osc_supp(A, omega, l, g, t_min, t_max, y_0):
    
    nt = (t_max - t_min) * FPS
    
    def pend_osc_supp(t, y, A, omega, l, g):
        theta, nu = y
        dthetadt = nu
        dnudt = (A*omega**2 * np.cos(omega*t) * np.cos(theta))/l - (g * np.cos(theta))/l
        dydt = [dthetadt, dnudt]
        return dydt
    
    
    t = np.linspace(t_min, t_max, nt)
    sol = solve_ivp(pend_osc_supp, [t_min, t_max], y_0, t_eval=t, args=(A, omega, l, g), method='RK45')
    
    print(sol.message)
    
    sol_t = sol.t
    sol_theta = sol.y[0,:]
    
    return sol_t, sol_theta




def generate_anim(sol_t, sol_theta, A, omega):
    def supp_dyn(t, A, omega):
        return A*np.cos(omega*t)
    
    fig = plt.figure()
    fig.set_dpi(100)
    fig.set_size_inches(7, 6.5)
    
    ax = plt.axes(xlim=(-4, 4), ylim=(-5, 3))
    
    x1, y1 = [0, 0], [0, 0]
    pend_plot, = ax.plot(x1, y1, marker = 'o')
    patch = plt.Circle((0, 0), 0.15, fc='grey')
    time_text = ax.text(0.05, 0.95,'',horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)
    frame_text = ax.text(0.05, 0.90,'',horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)
    support_rod = ax.plot([-4, 4],[0, 0], color='black')
    
    plt.axis('off')
    
    def init():
        patch.center = (0, 0)
        ax.add_patch(patch)
        
        pend_plot.set_data(x1, y1)
        return patch, pend_plot
    
    def animate(i):
        x, y = patch.center
        t_i = sol_t[i]
        x = supp_dyn(t_i, A, omega)
        
        p1_x = x
        p1_y = y
        
        p2_x = x + l*np.sin(sol_theta[i] + np.pi/2)
        p2_y = -l*np.cos(sol_theta[i] + np.pi/2)
        
        
        pend_plot.set_data([p1_x, p2_x], [p1_y, p2_y])
        patch.center = (x, y)
        
        time_text.set_text('time = %.2f/%.2f sec' % (t_i, t_max))
        frame_text.set_text('frame = %d/%d' % (i, len(sol_theta)))
        return pend_plot, time_text, frame_text, patch
    
    
    anim = FuncAnimation(fig,
                         animate, 
                         init_func=init, 
                         frames=len(sol_theta), 
                         interval=1000/FPS,
                         blit=True)
    
    return anim    



###########################################################################

A = 1
omega = 4*np.pi
l = 3
g = 10

t_min = 0
t_max = 10

y_0 = [-np.pi/2, -1]


sol_t, sol_theta = solve_pend_osc_supp(A, omega, l, g, t_min, t_max, y_0)

anim = generate_anim(sol_t, sol_theta, A, omega)
anim.save("vids/omega=4pi.mp4")


###########################################################################

