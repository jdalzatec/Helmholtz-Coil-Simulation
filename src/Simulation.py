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
        self.coils = coils
        self.z_min = z_min
        self.z_max = z_max
        self.z_points = z_points
        self.y_min = y_min
        self.y_max = y_max
        self.y_points = y_points

        self.builder = Gtk.Builder()
        self.builder.add_from_file("./interfaces/running.glade")
        self.window = self.builder.get_object("wndRunning")
        self.progressBar = self.builder.get_object("progressBar")
        self.lblETA = self.builder.get_object("lblETA")
        self.btnCancel = self.builder.get_object("btnCancel")

        self.btnCancel.connect("clicked", self.on_cancel)

        self.window.set_transient_for(parent)

        self.progressBar.set_fraction(0.0)
        
        self.mu0 = 4 * numpy.pi * 1e-7
        self.z_arr = numpy.linspace(self.z_min, self.z_max, self.z_points)
        self.y_arr = numpy.linspace(self.y_min, self.y_max, self.y_points)

        self.y_arr[self.y_arr == 0.0] = numpy.finfo(numpy.float32).eps

        for coil in self.coils:
            self.z_arr[self.z_arr == coil.pos_z] = coil.pos_z - numpy.finfo(numpy.float32).eps
        
        # self.z_min = min(self.z_arr)
        # self.z_max = max(self.z_arr)
        # self.y_min = min(self.y_arr)
        # self.y_max = max(self.y_arr)
        
        self.z_grid, self.y_grid = numpy.meshgrid(self.z_arr, self.y_arr)
        self.z_grid = self.z_grid.T
        self.y_grid = self.y_grid.T

        self.Bz_grid = numpy.zeros(shape=(len(self.z_arr), len(self.y_arr)))
        self.Brho_grid = numpy.zeros(shape=(len(self.z_arr), len(self.y_arr)))

        self.pair_values = product(self.z_arr, self.y_arr)
        self.pair_indexes = product(range(self.z_points), range(self.y_points))
        self.count = 0

        self.stop = False
        self.finish = False
        self.times = []

        self.window.show_all()

        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

        self.wait_for_the_simulation()
        
    def wait_for_the_simulation(self):
        if not self.thread.is_alive():
            self.thread.join()

            if self.finish:
                self.parent.hide()
                print("finish")
                self.norm = numpy.sqrt(self.Brho_grid**2 + self.Bz_grid**2)
                zmid = (self.z_min + self.z_max) * 0.5
                ymid = (self.y_min + self.y_max) * 0.5
                self.norm_center = norm(self.coils, abs(ymid), zmid, self.mu0)
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


