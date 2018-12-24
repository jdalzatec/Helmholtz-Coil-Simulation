import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from CoilListRow import CoilListRow

import numpy


class HelmholtzCoilPreset(list):
    def __init__(self):
        coil_row_1 = CoilListRow()
        coil_row_2 = CoilListRow()
        
        coil_row_1.set_values(shape="Circular", radius=0.5, turns=100, current=1.0, position=0.25)
        coil_row_2.set_values(shape="Circular", radius=0.5, turns=100, current=1.0, position=-0.25)

        self.append(coil_row_1)
        self.append(coil_row_2)


class RandomCoilPreset(list):
    def __init__(self, N):
        self.N = N
        for i in range(self.N):
            radius = numpy.random.uniform(0.2, 1.0)
            turns = numpy.random.randint(100, 200)
            current = numpy.random.uniform(0.1, 1.0)
            position = numpy.random.uniform(-1.0, 1.0)

            coil_row = CoilListRow()
            coil_row.set_values(shape="Circular", radius=radius, turns=turns, current=current, position=position)
            self.append(coil_row)
