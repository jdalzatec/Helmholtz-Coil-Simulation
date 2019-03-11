from coil import Coil
from numbers import Number
from multipledispatch import dispatch
from functools import reduce
import numpy

def compute_norm(coils, rho, z, mu0):
    return numpy.sqrt(Bz(coils, rho, z, mu0)**2 + Brho(coils, rho, z, mu0)**2)


@dispatch((tuple, list, numpy.ndarray), Number, Number, Number)
def Bz(coils, rho, z, mu0):
    if rho == 0.0:
        rho = numpy.finfo(numpy.float32).eps
    for coil in coils:
        if z == coil.pos_z:
            z = coil.pos_z - numpy.finfo(numpy.float32).eps

    return numpy.sum([mu0 * coil.Bz(rho, z) for coil in coils])


@dispatch((tuple, list, numpy.ndarray), Number, Number, Number)
def Brho(coils, rho, z, mu0):
    if rho == 0.0:
        rho = numpy.finfo(numpy.float32).eps
    for coil in coils:
        if z == coil.pos_z:
            z = coil.pos_z - numpy.finfo(numpy.float32).eps
    return numpy.sum([mu0 * coil.Brho(rho, z) for coil in coils])


@dispatch((tuple, list, numpy.ndarray), Number, (tuple, list, numpy.ndarray), Number)
def Bz(coils, rho, z_arr, mu0):
    return numpy.array([Bz(coils, rho, z, mu0) for z in z_arr])


@dispatch((tuple, list, numpy.ndarray), Number, (tuple, list, numpy.ndarray), Number)
def Brho(coils, rho, z_arr, mu0):
    return numpy.array([Brho(coils, rho, z, mu0) for z in z_arr])


@dispatch((tuple, list, numpy.ndarray), (tuple, list, numpy.ndarray), Number, Number)
def Bz(coils, rho_arr, z, mu0):
    return numpy.array([Bz(coils, rho, z, mu0) for rho in rho_arr])


@dispatch((tuple, list, numpy.ndarray), (tuple, list, numpy.ndarray), Number, Number)
def Brho(coils, rho_arr, z, mu0):
    return numpy.array([Brho(coils, rho, z, mu0) for rho in rho_arr])


@dispatch((tuple, list, numpy.ndarray), (tuple, list, numpy.ndarray), (tuple, list, numpy.ndarray), Number)
def Bz(coils, rho_arr, z_arr, mu0):
    Bz_grid = numpy.zeros(shape=(len(z_arr), len(rho_arr)))
    for i, z in enumerate(z_arr):
        for j, rho in enumerate(rho_arr):
            Bz_grid[i, j] = Bz(coils, rho, z, mu0)
    return Bz_grid


@dispatch((tuple, list, numpy.ndarray), (tuple, list, numpy.ndarray), (tuple, list, numpy.ndarray), Number)
def Brho(coils, rho_arr, z_arr, mu0):
    Brho_grid = numpy.zeros(shape=(len(z_arr), len(rho_arr)))
    for i, z in enumerate(z_arr):
        for j, rho in enumerate(rho_arr):
            Brho_grid[i, j] = Brho(coils, rho, z, mu0)
    return Brho_grid


@dispatch((tuple, list, numpy.ndarray), (tuple, list, numpy.ndarray), (tuple, list, numpy.ndarray), Number)
def Bz_Brho(coils, rho_arr, z_arr, mu0):
    Bz_grid = numpy.zeros(shape=(len(z_arr), len(rho_arr)))
    Brho_grid = numpy.zeros(shape=(len(z_arr), len(rho_arr)))
    for i, z in enumerate(z_arr):
        for j, rho in enumerate(rho_arr):
            Bz_grid[i, j] = Bz(coils, rho, z, mu0)
            Brho_grid[i, j] = Brho(coils, rho, z, mu0)
    return Bz_grid, Brho_grid

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
