"""Module creates an animation of an oscillating point charge's fields."""
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.animation import FuncAnimation

import pycharge as pc

lim = 50e-9
grid_size = 2000
x, y, z = np.meshgrid(np.linspace(0,lim, grid_size), np.linspace(0, lim, grid_size),
                      0, indexing='ij')


charge=pc.LinearAcceleratingCharge(5E-2)

simulation = pc.Simulation(charge)

fig, ax = plt.subplots(figsize=(5, 5))
ax.set_position([0, 0, 1, 1])
# Initialie im plot
im = ax.imshow(np.zeros((grid_size, grid_size)), origin='lower',
               extent=[0, lim, 0, lim], vmax=7)
ax.set_xticks([])
ax.set_yticks([])
im.set_norm(mpl.colors.LogNorm(vmin=1e5, vmax=1e8))

# Quiver plot
grid_size_quiver = 17
lim = 46e-9
x_quiver, y_quiver, z_quiver = np.meshgrid(
    np.linspace(0, lim, grid_size_quiver),
    np.linspace(0, lim, grid_size_quiver), 0,indexing='ij'
)
#Q = ax.quiver(x_quiver, y_quiver,
 #             x_quiver[:, :, 0], y_quiver[:, :, 0], scale_units='xy')
#pos = ax.scatter(charge.xpos(0), 0, s=5, c='red', marker='o')
t0 = np.array([0])  # time as array
pos = ax.scatter(charge.xpos(t0)[0], 0, s=5, c='red', marker='o')


def _update_animation(frame):
    text = f"\rProcessing frame {frame+1}/{n_frames}."
    sys.stdout.write(text)
    sys.stdout.flush()
    t = frame*dt
    E_total = simulation.calculate_E(t=t, x=x, y=y, z=z, pcharge_field='Total')
    #u = E_total[0][:, :, 0]
    u=0
    v = E_total[2][:, :, 0]
    #breakpoint()
    im.set_data(np.sqrt(v**2+v**2).T)
    #im.set_data(np.array(v).T)
    #E_total = simulation.calculate_E(
     #   t=t, x=x_quiver, y=y_quiver, z=z_quiver, pcharge_field='Total')
    #v = E_total[2][:, :, 0]
    #r = np.power(np.add(np.power(v, 2), np.power(v, 2)), 0.5)
    #Q.set_UVC(v/r, v/r)
    #pos.set_offsets((charge.xpos(t), 0))
    t_array = np.array([t])
    pos.set_offsets((charge.xpos(t_array)[0], 0))
    return im


def _init_animate():
    """Necessary for matplotlib animate."""
    pass  # pylint: disable=unnecessary-pass


n_frames = 12  # Number of frames in gif
dt = 1E-4
ani = FuncAnimation(fig, _update_animation,
                    frames=n_frames, blit=False, init_func=_init_animate)

ani.save('accelerating_charge_xy.gif',\
         writer=animation.FFMpegWriter(fps=12), dpi=200)
plt.close()