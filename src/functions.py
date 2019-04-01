from coil import Coil
from numbers import Number
from functools import reduce
import numpy

def compute_norm(coils, rho, z, mu0):
    return numpy.sqrt(Bz(coils, rho, z, mu0)**2 + Brho(coils, rho, z, mu0)**2)


def Bz(coils, rho, z, mu0):
    if rho == 0.0:
        rho = numpy.finfo(numpy.float32).eps
    for coil in coils:
        if z == coil.pos_z:
            z = coil.pos_z - numpy.finfo(numpy.float32).eps

    return numpy.sum([mu0 * coil.Bz(rho, z) for coil in coils])


def Brho(coils, rho, z, mu0):
    if rho == 0.0:
        rho = numpy.finfo(numpy.float32).eps
    for coil in coils:
        if z == coil.pos_z:
            z = coil.pos_z - numpy.finfo(numpy.float32).eps
    return numpy.sum([mu0 * coil.Brho(rho, z) for coil in coils])


def uniformity(coils, norm, mu0, center):
    zmid, ymid = center
    if ymid == 0.0:
        ymid = numpy.finfo(numpy.float32).eps

    Bz_mid = Bz(coils, numpy.abs(ymid), zmid, mu0)
    Brho_mid = Brho(coils, numpy.abs(ymid), zmid, mu0)


    norm_mid = numpy.sqrt(Bz_mid**2 + Brho_mid**2)
    
    values = 1.0 - numpy.abs((norm - norm_mid) / norm_mid)
    values[values <= 0.0] = 0.0
    return values
