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
    N=50
    I=1.0
    R=1.0
    d = R

    coils = [
        CircularCoil(R, N, I, -0.5 * d, "crimson"),
        CircularCoil(R, N, I, 0.5 * d, "royalblue"),
        CircularCoil(2 * R, N, I, 0.0, "black"),
    ]

    rho = 0.00001

    z_arr = numpy.linspace(-1, 1, 50)
    Bz_arr = numpy.zeros_like(z_arr)
    for i, z in enumerate(z_arr):
        for coil in coils:
            Bz_arr[i] += mu0 * coil.Bz(rho, z)


    Bz_teo = numpy.zeros_like(z_arr)
    for coil in coils:
        Bz_teo += 0.5 * mu0 * coil.num_turns * coil.I * coil.radius**2 / (coil.radius**2 + (z_arr - coil.pos_z)**2)**(3/2)



    pyplot.figure()
    pyplot.plot(z_arr, Bz_arr, "o", label=r"$B_{z}^{\rm num.}$")
    pyplot.plot(z_arr, Bz_teo, "--k", label=r"$B_{z}^{\rm theo.}$")
    for coil in coils:
        pyplot.axvline(coil.pos_z, ls="-", lw=coil.num_turns / 10,
            color=coil.color, zorder=0)
    pyplot.grid()
    pyplot.legend(loc="best")
    pyplot.title(r"$\rho = 0.0$", fontsize=20)
    pyplot.xlabel(r"$z \ \rm [a.u.]$", fontsize=30)
    pyplot.ylabel(r"$B_{z} \ \rm [a.u.]$", fontsize=30)
    pyplot.tight_layout()
    pyplot.savefig("Bz_vs_z.pdf")
    pyplot.close()

    plot_coils(coils)

if __name__ == '__main__':
    main()