import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from CoilListRow import CoilListRow

import numpy


class HelmholtzCoilPreset(list):
    def __init__(self):
        coil_row_1 = CoilListRow()
        coil_row_2 = CoilListRow()
        
        coil_row_1.set_values(radius=1.0, turns=100, current=1.0, position=-0.5)
        coil_row_2.set_values(radius=1.0, turns=100, current=1.0, position=0.5)

        self.append(coil_row_1)
        self.append(coil_row_2)


class RandomCoilPreset(list):
    def __init__(self, N):
        self.N = N
        for i in range(self.N):
            radius = numpy.random.uniform(0.5, 4.0)
            turns = numpy.random.randint(10, 200)
            current = numpy.random.uniform(1.0, 4.0)
            position = numpy.random.uniform(-10.0, 10.0)

            coil_row = CoilListRow()
            coil_row.set_values(radius=radius, turns=turns, current=current, position=position)
            self.append(coil_row)


class MaxwellCoilPreset(list):
    def __init__(self):

        coil_row_1 = CoilListRow()
        coil_row_1.set_values(radius=numpy.sqrt(4/7), turns=98, current=1.0, position=-numpy.sqrt(3/7))
        self.append(coil_row_1)

        coil_row_2 = CoilListRow()
        coil_row_2.set_values(radius=1.0, turns=128, current=1.0, position=0.0)
        self.append(coil_row_2)

        coil_row_3 = CoilListRow()
        coil_row_3.set_values(radius=numpy.sqrt(4/7), turns=98, current=1.0, position=numpy.sqrt(3/7))
        self.append(coil_row_3)

class WangCoilPreset(list):
    def __init__(self):

        coil_row_1 = CoilListRow()
        coil_row_1.set_values(radius=1.0, turns=111, current=1.0, position=-0.76)
        self.append(coil_row_1)

        coil_row_2 = CoilListRow()
        coil_row_2.set_values(radius=1.0, turns=59, current=1.0, position=0.0)
        self.append(coil_row_2)

        coil_row_3 = CoilListRow()
        coil_row_3.set_values(radius=1.0, turns=111, current=1.0, position=0.76)
        self.append(coil_row_3)

class TetraCoilPreset(list):
    def __init__(self):

        coil_row_1 = CoilListRow()
        coil_row_1.set_values(radius=0.672, turns=73, current=1.0, position=-0.798)
        self.append(coil_row_1)

        coil_row_2 = CoilListRow()
        coil_row_2.set_values(radius=1.0, turns=107, current=1.0, position=-0.298)
        self.append(coil_row_2)

        coil_row_3 = CoilListRow()
        coil_row_3.set_values(radius=1.0, turns=107, current=1.0, position=0.298)
        self.append(coil_row_3)

        coil_row_4 = CoilListRow()
        coil_row_4.set_values(radius=0.672, turns=73, current=1.0, position=0.798)
        self.append(coil_row_4)

class LeeWhitingCoilPreset(list):
    def __init__(self):

        coil_row_1 = CoilListRow()
        coil_row_1.set_values(radius=1.0, turns=90, current=1.0, position=-0.9408)
        self.append(coil_row_1)

        coil_row_2 = CoilListRow()
        coil_row_2.set_values(radius=1.0, turns=40, current=1.0, position=-0.2432)
        self.append(coil_row_2)

        coil_row_3 = CoilListRow()
        coil_row_3.set_values(radius=1.0, turns=40, current=1.0, position=0.2432)
        self.append(coil_row_3)

        coil_row_4 = CoilListRow()
        coil_row_4.set_values(radius=1.0, turns=90, current=1.0, position=0.9408)
        self.append(coil_row_4)

