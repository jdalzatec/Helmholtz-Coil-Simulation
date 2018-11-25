from coil import Coil
from numbers import Number
from multipledispatch import dispatch
from functools import reduce
import numpy


@dispatch(list, Number, Number, Number)
def Bz(coils, rho, z, mu0):
    return numpy.sum([mu0 * coil.Bz(rho, z) for coil in coils])


@dispatch(list, Number, Number, Number)
def Brho(coils, rho, z, mu0):
    return numpy.sum([mu0 * coil.Brho(rho, z) for coil in coils])


@dispatch(list, Number, (list, numpy.ndarray), Number)
def Bz(coils, rho, z_arr, mu0):
    return numpy.array([Bz(coils, rho, z, mu0) for z in z_arr])


@dispatch(list, Number, (list, numpy.ndarray), Number)
def Brho(coils, rho, z_arr, mu0):
    return numpy.array([Brho(coils, rho, z, mu0) for z in z_arr])


@dispatch(list, (list, numpy.ndarray), Number, Number)
def Bz(coils, rho_arr, z, mu0):
    return numpy.array([Bz(coils, rho, z, mu0) for rho in rho_arr])


@dispatch(list, (list, numpy.ndarray), Number, Number)
def Brho(coils, rho_arr, z, mu0):
    return numpy.array([Brho(coils, rho, z, mu0) for rho in rho_arr])


@dispatch(list, (list, numpy.ndarray), (list, numpy.ndarray), Number)
def Bz(coils, rho_arr, z_arr, mu0):
    Bz_grid = numpy.zeros(shape=(len(z_arr), len(rho_arr)))
    for i, z in enumerate(z_arr):
        for j, rho in enumerate(rho_arr):
            Bz_grid[i, j] = Bz(coils, rho, z, mu0)
    return Bz_grid


@dispatch(list, (list, numpy.ndarray), (list, numpy.ndarray), Number)
def Brho(coils, rho_arr, z_arr, mu0):
    Brho_grid = numpy.zeros(shape=(len(z_arr), len(rho_arr)))
    for i, z in enumerate(z_arr):
        for j, rho in enumerate(rho_arr):
            Brho_grid[i, j] = Brho(coils, rho, z, mu0)
    return Brho_grid


@dispatch(list, (list, numpy.ndarray), (list, numpy.ndarray), Number)
def Bz_Brho(coils, rho_arr, z_arr, mu0):
    Bz_grid = numpy.zeros(shape=(len(z_arr), len(rho_arr)))
    Brho_grid = numpy.zeros(shape=(len(z_arr), len(rho_arr)))
    for i, z in enumerate(z_arr):
        for j, rho in enumerate(rho_arr):
            Bz_grid[i, j] = Bz(coils, rho, z, mu0)
            Brho_grid[i, j] = Brho(coils, rho, z, mu0)
    return Bz_grid, Brho_grid