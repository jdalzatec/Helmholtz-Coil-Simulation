from plot import plot_coils
from matplotlib import pyplot
import matplotlib
matplotlib.style.use('classic')
import numpy

from functions import *

class Simulation(object):
    def __init__(self, coils, z_min, z_max, z_points, rho_min, rho_max, rho_points):
        self.coils = coils
        self.z_min = z_min
        self.z_max = z_max
        self.z_points = z_points
        self.rho_min = rho_min
        self.rho_max = rho_max
        self.rho_points = rho_points


    def run(self):
        mu0 = 4 * numpy.pi * 1e-7
        z_arr = numpy.linspace(self.z_min, self.z_max, self.z_points)
        rho_arr = numpy.linspace(self.rho_min, self.rho_max, self.rho_points)

        rho_arr[rho_arr == 0.0] = numpy.finfo(numpy.float32).eps

        for coil in self.coils:
            z_arr[z_arr == coil.pos_z] = coil.pos_z - numpy.finfo(numpy.float32).eps
        
        
        z_grid, rho_grid = numpy.meshgrid(z_arr, rho_arr)
        z_grid = z_grid.T
        rho_grid = rho_grid.T

        Bz_grid = numpy.zeros(shape=(len(z_arr), len(rho_arr)))
        Brho_grid = numpy.zeros(shape=(len(z_arr), len(rho_arr)))
        for i, z in enumerate(z_arr):
            for j, rho in enumerate(rho_arr):
                Bz_grid[i, j] = Bz(self.coils, rho, z, mu0)
                Brho_grid[i, j] = Brho(self.coils, rho, z, mu0)
        

        print("simulation done")
        