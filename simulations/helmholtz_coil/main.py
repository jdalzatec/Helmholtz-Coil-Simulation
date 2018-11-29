import sys
sys.path.append("../../src")

from coil import CircularCoil
from plot import plot_coils
from matplotlib import pyplot
import matplotlib
matplotlib.style.use('classic')
import numpy

from functions import *


def main():
    mu0=4 * numpy.pi * 1e-7
    N=100
    I=4.8
    R=0.5
    d = R

    coils = [
        CircularCoil(R, N, I, - 0.5 * d, "crimson"),
        CircularCoil(R, N, I, 0.5 * d, "crimson"),
    ]

    z_arr = numpy.linspace(-0.5 * R, 0.5 * R, 21)
    rho_arr = numpy.linspace(0, R, 20)

    rho_arr[rho_arr == 0.0] = numpy.finfo(numpy.float32).eps
    for coil in coils:
        z_arr[z_arr == coil.pos_z] = coil.pos_z - numpy.finfo(numpy.float32).eps
    
    
    z_grid, rho_grid = numpy.meshgrid(z_arr, rho_arr)
    z_grid = z_grid.T
    rho_grid = rho_grid.T

    Bz_grid = Bz(coils, rho_arr, z_arr, mu0)
    Brho_grid = Brho(coils, rho_arr, z_arr, mu0)
    # Bz_grid, Brho_grid = Bz_Brho(coils, rho_arr, z_arr, mu0)


    norm = numpy.sqrt(Brho_grid**2 + Bz_grid**2)

    #compute bottom left coords of rectangle of homogeneity homo
    uniformity_grid = uniformity(coils, norm, mu0)
    homo = 99
    z, y = homogeneity(uniformity_grid, z_arr, rho_arr, homo)


    max_val = 1e-3
    # surpass is for set the >= symbol in case of norm >= max_val
    surpass = False
    if numpy.any(norm >= max_val):
        surpass = True
        norm[norm >= max_val] = max_val

    min_val = 5e-4
    # underpass is for set the <= symbol in case of norm <= max_val
    underpass = False
    if numpy.any(norm <= min_val):
        underpass = True
        norm[norm <= min_val] = min_val
    

    min_val = numpy.min(norm)
    max_val = numpy.max(norm)

    assert(max_val > min_val)

    # cmap = pyplot.get_cmap('Paired')
    cmap = pyplot.get_cmap('jet')

    pyplot.figure()
    mesh = pyplot.pcolormesh(z_grid, rho_grid, norm,
        shading="gouraud", cmap=cmap)
    mesh = pyplot.pcolormesh(z_grid, -rho_grid, norm,
        shading="gouraud", cmap=cmap)
    cbar = pyplot.colorbar(mesh, format='%.2e')

    # set the ticks and ticks labels for the color bar
    labels = numpy.linspace(min_val, max_val, 5)
    cbar.set_ticks(labels)
    labels = ['%.2e' % s for s in labels]


    # in case of surpass is true, the last label is modified
    if surpass: labels[-1] = r"$\geq$ " + labels[-1]

    # in case of underpass is true, the first label is modified
    if underpass: labels[0] = r"$\leq$ " + labels[0]

    cbar.ax.set_yticklabels(labels)


    for coil in coils:
        pyplot.plot([coil.pos_z, coil.pos_z], [-coil.radius, coil.radius],
            lw=coil.num_turns / 10, color=coil.color)
    
    # plot homogeneity rectangle
    pyplot.gca().add_patch(pyplot.Rectangle((z, y), abs(2 * z), abs(2 * y), fill=False, edgecolor='black', linewidth=coil.num_turns / 50))
 

    pyplot.grid()
    pyplot.xlabel(r"$z$", fontsize=30)
    pyplot.ylabel(r"$y$", fontsize=30)
    pyplot.tight_layout()
    pyplot.savefig("Bz_vs_z_several_r.pdf")
    pyplot.close()

    plot_coils(coils)
    

if __name__ == '__main__':
    main()