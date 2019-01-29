from coil import Coil
from numbers import Number
from multipledispatch import dispatch
from functools import reduce
import numpy


@dispatch((tuple, list, numpy.ndarray), Number, Number, Number)
def Bz(coils, rho, z, mu0):
    return numpy.sum([mu0 * coil.Bz(rho, z) for coil in coils])


@dispatch((tuple, list, numpy.ndarray), Number, Number, Number)
def Brho(coils, rho, z, mu0):
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

def uniformity(coils, norm, mu0):
        B0 = Bz(coils, numpy.finfo(numpy.float32).eps, numpy.finfo(numpy.float32).eps, mu0)
        return 1.0 - numpy.abs((norm - B0) / B0)

def homogeneity(uniformity_grid, z_arr, rho_arr, homo):
    # z, y = z_arr[0], -rho_arr[-1]
    z, y = z_arr[0], -rho_arr[-1]
    for i in range(int(len(z_arr)/2 + 1)):
            if uniformity_grid[int(len(z_arr)/2) + i, 0] < homo/100:
                    z = z_arr[int(len(z_arr)/2) - i + 1]
                    break
    for j in range(len(rho_arr)):
            if uniformity_grid[int(len(z_arr)/2), j] < homo/100:
                    y = -rho_arr[j - 1]
                    break
    return (z, y)