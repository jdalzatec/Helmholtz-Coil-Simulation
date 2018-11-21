from scipy.integrate import simps
from matplotlib import pyplot
import matplotlib
matplotlib.style.use('classic')
import numpy

pi = numpy.pi

def K(kto2, points=1000):
    phi = numpy.linspace(0, 0.5 * pi, points)
    values = numpy.zeros_like(kto2)
    func = 1.0 / numpy.sqrt(1 - kto2 * numpy.sin(phi))
    return simps(func, phi)


def E(kto2, points=1000):
    phi = numpy.linspace(0, 0.5 * pi, points)
    values = numpy.zeros_like(kto2)
    func = numpy.sqrt(1 - kto2 * numpy.sin(phi))
    return simps(func, phi)


def Br(r, z, d=1.0, mu0=1.0, N=10, I=1.0, R=1.0):
    k1to2 = (4 * R * r) / ((R + r)**2 + (z + 0.5 * d)**2)
    k2to2 = (4 * R * r) / ((R + r)**2 + (z - 0.5 * d)**2)
    K1 = K(k1to2)
    K2 = K(k2to2)
    E1 = E(k1to2)
    E2 = E(k2to2)
    return (((mu0 / (2.0 * pi * r)) * N * I * (z + 0.5 * d)) / numpy.sqrt((R + r)**2 + (z + 0.5 * d)**2)) * \
           ((R**2 + r**2 + (z + 0.5 * d)**2) * E1 / ((R - r)**2 + (z + 0.5 * d)**2) - K1) + \
           (((mu0 / (2.0 * pi * r)) * N * I * (z - 0.5 * d)) / numpy.sqrt((R + r)**2 + (z - 0.5 * d)**2)) * \
           ((R**2 + r**2 + (z - 0.5 * d)**2) * E2 / ((R - r)**2 + (z - 0.5 * d)**2) - K2)

def Bz(r, z, d=1.0, mu0=1.0, N=10, I=1.0, R=1.0):
    k1to2 = (4 * R * r) / ((R + r)**2 + (z + 0.5 * d)**2)
    k2to2 = (4 * R * r) / ((R + r)**2 + (z - 0.5 * d)**2)
    K1 = K(k1to2)
    K2 = K(k2to2)
    E1 = E(k1to2)
    E2 = E(k2to2)
    return (((mu0 / (2.0 * pi)) * N * I) / numpy.sqrt((R + r)**2 + (z + 0.5 * d)**2)) * \
           ((R**2 - r**2 - (z + 0.5 * d)**2) * E1 / ((R - r)**2 + (z + 0.5 * d)**2) + K1) + \
           (((mu0 / (2.0 * pi)) * N * I) / numpy.sqrt((R + r)**2 + (z - 0.5 * d)**2)) * \
           ((R**2 - r**2 - (z - 0.5 * d)**2) * E2 / ((R - r)**2 + (z - 0.5 * d)**2) + K2)


def example1():
    z_arr = numpy.linspace(-1, 1, 50)
    mu0=1.0
    N=100
    I=1.0
    R=1.0
    d = R
    r_arr = [0.00001]

    Bz_arr = numpy.zeros((len(z_arr), len(r_arr)))
    Br_arr = numpy.zeros((len(z_arr), len(r_arr)))

    for i, z in enumerate(z_arr):
        for j, r in enumerate(r_arr):
            Bz_arr[i, j] = Bz(r, z, d=d, mu0=mu0, N=N, I=I, R=R)
            Br_arr[i, j] = Br(r, z, d=d, mu0=mu0, N=N, I=I, R=R)

    Bz_theo = 0.5 * mu0 * N * I * R**2 * (
        (R**2 + (z_arr + 0.5 * d)**2)**(-3/2) + \
        (R**2 + (z_arr - 0.5 * d)**2)**(-3/2)
        )

    pyplot.figure()
    pyplot.plot(z_arr, Bz_arr[:, 0], "o", label=r"$B_{z}^{\rm num.}$")
    pyplot.plot(z_arr, Bz_theo, "--k", lw=2, label=r"$B_{z}^{\rm theo.}$")
    pyplot.axvline(d*0.5, lw=2, ls="-", color="crimson")
    pyplot.axvline(-d*0.5, lw=2, ls="-", color="crimson")
    pyplot.axhline(8*mu0*N*I / (numpy.sqrt(125) * R), lw=2, ls="--", color="royalblue")
    pyplot.grid()
    pyplot.legend(loc="best", fontsize=20)
    pyplot.xlabel(r"$z \ \rm [a.u.]$", fontsize=30)
    pyplot.ylabel(r"$B_{z} \ \rm [a.u.]$", fontsize=30)
    pyplot.tight_layout()
    pyplot.savefig("Bz_vs_z.pdf")
    pyplot.close()


def example2():
    mu0=1.0
    N=100
    I=4.8
    R=0.475
    d = R
    z_arr = numpy.linspace(0, R/3, 50)
    r_arr = numpy.linspace(0.000001, R, 50)
    
    z_grid, r_grid = numpy.meshgrid(z_arr, r_arr)
    z_grid = z_grid.T
    r_grid = r_grid.T

    Bz_grid = numpy.zeros_like(z_grid)
    Br_grid = numpy.zeros_like(z_grid)

    for i in range(len(z_arr)):
        for j in range(len(r_arr)):
            z, r = z_grid[i, j], r_grid[i, j]
            Bz_grid[i, j] = Bz(r, z, d=d, mu0=mu0, N=N, I=I, R=R)
            Br_grid[i, j] = Br(r, z, d=d, mu0=mu0, N=N, I=I, R=R)


    norm = numpy.sqrt(Br_grid**2 + Bz_grid**2)

    pyplot.figure()
    mesh = pyplot.pcolormesh(z_grid, r_grid, norm, shading="gouraud")
    pyplot.pcolormesh(-z_grid, r_grid, norm, shading="gouraud")
    pyplot.pcolormesh(z_grid, -r_grid, norm, shading="gouraud")
    pyplot.pcolormesh(-z_grid, -r_grid, norm, shading="gouraud")
    cbar = pyplot.colorbar(mesh)

    pyplot.axvline(-d*0.5, ls="--", lw=2, color="black")
    pyplot.axvline(d*0.5, ls="--", lw=2, color="black")
    pyplot.axhline(-R, ls="--", lw=2, color="black")
    pyplot.axhline(R, ls="--", lw=2, color="black")
    pyplot.grid()
    pyplot.legend(loc="best", ncol=2)
    pyplot.xlabel(r"$z$", fontsize=30)
    pyplot.ylabel(r"$y$", fontsize=30)
    pyplot.tight_layout()
    pyplot.savefig("Bz_vs_z_several_r.pdf")
    # pyplot.show()
    pyplot.close()

def main():
    # example1()
    example2()
    

if __name__ == '__main__':
    main()