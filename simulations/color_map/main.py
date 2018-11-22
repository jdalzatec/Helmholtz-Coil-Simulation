import sys
sys.path.append("../../src")

from coil import CircularCoil
from plot import plot_coils
from matplotlib import pyplot
import matplotlib
matplotlib.style.use('classic')
import numpy



def main():
    mu0=1.0
    N=100
    I=4.8
    R=0.5
    d = R

    coils = [
        CircularCoil(R, N, I, -0.5 * d, "crimson"),
        CircularCoil(R, N, I, 0.5 * d, "crimson"),
    ]


    z_arr = numpy.linspace(-R*12/25, R*12/25, 50)
    rho_arr = numpy.linspace(0.000001, R, 50)
    
    z_grid, rho_grid = numpy.meshgrid(z_arr, rho_arr)
    z_grid = z_grid.T
    rho_grid = rho_grid.T

    Bz_grid = numpy.zeros_like(z_grid)
    Brho_grid = numpy.zeros_like(z_grid)

    for i in range(len(z_arr)):
        for j in range(len(rho_arr)):
            z, rho = z_grid[i, j], rho_grid[i, j]
            for coil in coils:
                Bz_grid[i, j] += mu0 * coil.Bz(rho, z)
                Brho_grid[i, j] += mu0 * coil.Brho(rho, z)


    norm = numpy.sqrt(Brho_grid**2 + Bz_grid**2)

    max_val = 1000
    # overpass is for set the >= symbol in case of norm >= max_val
    overpass = False
    if numpy.any(norm >= max_val):
        overpass = True
        norm[norm >= max_val] = max_val

    min_val = numpy.floor(numpy.min(norm))
    max_val = numpy.ceil(numpy.max(norm))

    assert(max_val > min_val)

    # cmap = pyplot.get_cmap('Paired')
    cmap = pyplot.get_cmap('jet')

    pyplot.figure()
    mesh = pyplot.pcolormesh(z_grid, rho_grid, norm,
        shading="gouraud", vmin=min_val, vmax=max_val, cmap=cmap)
    mesh = pyplot.pcolormesh(z_grid, -rho_grid, norm,
        shading="gouraud", vmin=min_val, vmax=max_val, cmap=cmap)
    cbar = pyplot.colorbar(mesh)
    
    # set the ticks and ticks labels for the color bar
    labels = numpy.linspace(min_val, max_val, 5)
    cbar.set_ticks(labels)
    labels = [str(s) for s in labels]

    # in case of overpass is true, the last label is modified
    if overpass:
        labels[-1] = r"$\geq$ " + labels[-1]
    cbar.ax.set_yticklabels(labels)


    for coil in coils:
        pyplot.plot([coil.pos_z, coil.pos_z], [-coil.radius, coil.radius],
            lw=coil.num_turns / 10, color=coil.color)

    pyplot.grid()
    pyplot.xlabel(r"$z$", fontsize=30)
    pyplot.ylabel(r"$y$", fontsize=30)
    pyplot.tight_layout()
    pyplot.savefig("Bz_vs_z_several_r.pdf")
    pyplot.close()

    plot_coils(coils)
    

if __name__ == '__main__':
    main()