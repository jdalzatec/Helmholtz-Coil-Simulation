import sys

is_frozen = getattr(sys, 'frozen', False)
frozen_temp_path = getattr(sys, '_MEIPASS', '')

import os

# This is needed to find resources when using pyinstaller
if is_frozen:
    basedir = frozen_temp_path
else:
    basedir = os.path.dirname(os.path.abspath(__file__))
resource_dir = os.path.join(basedir, 'resources')




import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

import timeit
import datetime
import threading

from Results import Results

from plot import plot_coils
from matplotlib import pyplot
import matplotlib
matplotlib.style.use('classic')
import numpy
from itertools import product

from functions import *

class Simulation(object):
    def __init__(self, parent, coils, z_min, z_max, z_points, y_min, y_max, y_points):
        self.parent = parent
        self.builder = Gtk.Builder()
        self.builder.add_from_file(resource_dir + "/running.glade")
        self.window = self.builder.get_object("wndRunning")
        self.progressBar = self.builder.get_object("progressBar")
        self.lblETA = self.builder.get_object("lblETA")
        self.btnCancel = self.builder.get_object("btnCancel")

        self.btnCancel.connect("clicked", self.on_cancel)
        self.window.set_transient_for(parent.window)
        self.progressBar.set_fraction(0.0)
        
        self.mu0 = 4 * numpy.pi * 1e-7 * 1000
    
        self.build_data(coils, z_min, z_max, z_points, y_min, y_max, y_points)

        self.pair_values = product(self.z_arr, self.y_arr)
        self.pair_indexes = product(range(self.z_points), range(self.y_points))
        self.count = 0

        self.stop = False
        self.finish = False
        self.times = []


    
    def simulate(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

        self.wait_for_the_simulation()

        self.window.show_all()

    def build_data(self, coils, z_min, z_max, z_points, y_min, y_max, y_points):
        self.coils = coils
        self.z_min = z_min
        self.z_max = z_max
        self.z_points = z_points + 1
        self.y_min = y_min
        self.y_max = y_max
        self.y_points = y_points + 1

        self.z_arr = numpy.linspace(self.z_min, self.z_max, self.z_points)
        self.y_arr = numpy.linspace(self.y_min, self.y_max, self.y_points)

        self.z_grid, self.y_grid = numpy.meshgrid(self.z_arr, self.y_arr)
        self.z_grid = self.z_grid.T
        self.y_grid = self.y_grid.T

        self.Bz_grid = numpy.zeros(shape=(len(self.z_arr), len(self.y_arr)))

        self.Brho_grid = numpy.zeros(shape=(len(self.z_arr), len(self.y_arr)))

        zmid = (self.z_min + self.z_max) * 0.5
        ymid = (self.y_min + self.y_max) * 0.5
        self.norm_center = compute_norm(self.coils, abs(ymid), zmid, self.mu0)

    def set_data(self, coils, z_min, z_max, z_points, y_min, y_max, y_points,
                 z_arr, y_arr, Bz_grid, Brho_grid, norm):
        self.coils = coils
        self.z_min = z_min
        self.z_max = z_max
        self.z_points = z_points + 1
        self.y_min = y_min
        self.y_max = y_max
        self.y_points = y_points + 1

        self.z_arr = z_arr
        self.y_arr = y_arr

        self.z_grid, self.y_grid = numpy.meshgrid(self.z_arr, self.y_arr)
        self.z_grid = self.z_grid.T
        self.y_grid = self.y_grid.T

        self.Bz_grid = Bz_grid
        self.Brho_grid = Brho_grid

        zmid = (self.z_min + self.z_max) * 0.5
        ymid = (self.y_min + self.y_max) * 0.5
        self.norm_center = compute_norm(self.coils, abs(ymid), zmid, self.mu0)

        self.norm = norm
        
    def wait_for_the_simulation(self):
        if not self.thread.is_alive():
            self.thread.join()

            if self.finish:
                # print("finish")
                self.parent.window.hide()
                self.norm = numpy.sqrt(self.Brho_grid**2 + self.Bz_grid**2)
                results = Results(self.parent, self)

                # from matplotlib import pyplot
                # flatten = self.norm.flatten()
                # flatten[flatten > 1] = 0
                # pyplot.figure()
                # pyplot.hist(flatten, 50)
                # pyplot.show()
        else:
            GLib.timeout_add(10, self.wait_for_the_simulation)

    def on_cancel(self, widget):
        self.stop = True
        self.finish = False


    def update_progress(self):
        self.progressBar.set_fraction(self.count / (self.z_points * self.y_points))
        ETA = numpy.mean(self.times) * (self.z_points * self.y_points - self.count)
        self.lblETA.set_text("ETA : %s seconds" % str(datetime.timedelta(seconds=int(ETA))))
        return False


    def step(self):
        start = timeit.default_timer()

        z, y = next(self.pair_values)
        i, j = next(self.pair_indexes)

        self.Bz_grid[i, j] = Bz(self.coils, abs(y), z, self.mu0)
        self.Brho_grid[i, j] = Brho(self.coils, abs(y), z, self.mu0)
        self.count += 1

        if (i == (self.z_points - 1) and j == (self.y_points - 1)):
            self.stop = True
            self.finish = True

        stop = timeit.default_timer()
        self.times.append(stop - start)

        GLib.idle_add(self.update_progress)
        # print(i, j, self.progressBar.get_fraction())


    def run(self):
        while not self.stop:
            self.step()
        self.window.close()


