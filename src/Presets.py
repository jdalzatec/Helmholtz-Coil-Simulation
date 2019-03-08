import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from CoilListRow import CoilListRow

import numpy


class HelmholtzCoilPreset(list):
    def __init__(self):
        coil_row_1 = CoilListRow()
        coil_row_2 = CoilListRow()
        
        coil_row_1.set_values(radius=0.2, turns=500, current=1.0, position=-0.1)
        coil_row_2.set_values(radius=0.2, turns=500, current=1.0, position=0.1)

        self.append(coil_row_1)
        self.append(coil_row_2)


class RandomCoilPreset(list):
    def __init__(self, N):
        self.N = N
        for i in range(self.N):
            radius = numpy.random.uniform(0.1, 1.0)
            turns = numpy.random.randint(10, 500)
            current = numpy.random.uniform(1.0, 5.0)
            position = numpy.random.uniform(-1.0, 1.0)

            coil_row = CoilListRow()
            coil_row.set_values(radius=radius, turns=turns, current=current, position=position)
            self.append(coil_row)


class MaxwellCoilPreset(list):
    def __init__(self):

        coil_row_1 = CoilListRow()
        coil_row_1.set_values(radius=0.2*numpy.sqrt(4/7), turns=490, current=1.0, position=-0.2*numpy.sqrt(3/7))
        self.append(coil_row_1)

        coil_row_2 = CoilListRow()
        coil_row_2.set_values(radius=0.2, turns=640, current=1.0, position=0.0)
        self.append(coil_row_2)

        coil_row_3 = CoilListRow()
        coil_row_3.set_values(radius=0.2*numpy.sqrt(4/7), turns=490, current=1.0, position=0.2*numpy.sqrt(3/7))
        self.append(coil_row_3)

class WangCoilPreset(list):
    def __init__(self):

        coil_row_1 = CoilListRow()
        coil_row_1.set_values(radius=0.2, turns=555, current=1.0, position=-0.2*0.76)
        self.append(coil_row_1)

        coil_row_2 = CoilListRow()
        coil_row_2.set_values(radius=0.2, turns=295, current=1.0, position=0.0)
        self.append(coil_row_2)

        coil_row_3 = CoilListRow()
        coil_row_3.set_values(radius=0.2, turns=555, current=1.0, position=0.2*0.76)
        self.append(coil_row_3)

class TetraCoilPreset(list):
    def __init__(self):

        radius_tetracoil=0.2
        coil_row_1 = CoilListRow()
        coil_row_1.set_values(radius=radius_tetracoil*0.672, turns=365, current=1.0, position=-2*radius_tetracoil*0.399)
        self.append(coil_row_1)

        coil_row_2 = CoilListRow()
        coil_row_2.set_values(radius=radius_tetracoil, turns=535, current=1.0, position=-2*radius_tetracoil*0.149)
        self.append(coil_row_2)

        coil_row_3 = CoilListRow()
        coil_row_3.set_values(radius=radius_tetracoil, turns=535, current=1.0, position=2*radius_tetracoil*0.149)
        self.append(coil_row_3)

        coil_row_4 = CoilListRow()
        coil_row_4.set_values(radius=radius_tetracoil*0.672, turns=365, current=1.0, position=2*radius_tetracoil*0.399)
        self.append(coil_row_4)

class LeeWhitingCoilPreset(list):
    def __init__(self):
        
        radius_lee = 0.2
        coil_row_1 = CoilListRow()
        coil_row_1.set_values(radius=radius_lee, turns=450, current=1.0, position=-2*radius_lee*0.4704)
        self.append(coil_row_1)

        coil_row_2 = CoilListRow()
        coil_row_2.set_values(radius=radius_lee, turns=200, current=1.0, position=-2*radius_lee*0.1216)
        self.append(coil_row_2)

        coil_row_3 = CoilListRow()
        coil_row_3.set_values(radius=radius_lee, turns=200, current=1.0, position=2*radius_lee*0.1216)
        self.append(coil_row_3)

        coil_row_4 = CoilListRow()
        coil_row_4.set_values(radius=radius_lee, turns=450, current=1.0, position=2*radius_lee*0.4704)
        self.append(coil_row_4)

