from scipy.integrate import simps
from matplotlib import pyplot
import numpy

pi = numpy.pi

def K(kto2, points=100):
    phi = numpy.linspace(0, 0.5 * pi, points)
    values = numpy.zeros_like(kto2)
    for i in range(len(kto2)):
        func = 1.0 / numpy.sqrt(1 - kto2[i] * numpy.sin(phi))
        values[i] = simps(func, phi)
    return values


def E(kto2, points=100):
    phi = numpy.linspace(0, 0.5 * pi, points)
    values = numpy.zeros_like(kto2)
    for i in range(len(kto2)):
        func = numpy.sqrt(1 - kto2[i] * numpy.sin(phi))
        values[i] = simps(func, phi)
    return values


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

def main():
    z = numpy.linspace(-1, 1, 50)


    mu0=1.0
    N=100
    I=1.0
    R=1.0
    d = R
    r = 0.00001

    Bz_arr = Bz(r, z, d=d, mu0=mu0, N=N, I=I, R=R)
    Br_arr = Br(r, z, d=d, mu0=mu0, N=N, I=I, R=R)

    Bz_theo = 0.5 * mu0 * N * I * R**2 * (
        (R**2 + (z + 0.5 * d)**2)**(-3/2) + \
        (R**2 + (z - 0.5 * d)**2)**(-3/2)
        )

    pyplot.figure()
    pyplot.plot(z, Bz_arr, "o", label=r"$B_{z}^{\rm num.}$")
    pyplot.plot(z, Bz_theo, "--k", lw=2, label=r"$B_{z}^{\rm theo.}$")
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

if __name__ == '__main__':
    main()