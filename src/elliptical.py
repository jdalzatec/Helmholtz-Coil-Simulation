from scipy.integrate import simps
import numpy

def K(kto2, points=1000):
    phi = numpy.linspace(0, 0.5 * numpy.pi, points)
    values = numpy.zeros_like(kto2)
    func = 1.0 / numpy.sqrt(1 - kto2 * numpy.sin(phi))
    return simps(func, phi)


def E(kto2, points=1000):
    phi = numpy.linspace(0, 0.5 * numpy.pi, points)
    values = numpy.zeros_like(kto2)
    func = numpy.sqrt(1 - kto2 * numpy.sin(phi))
    return simps(func, phi)