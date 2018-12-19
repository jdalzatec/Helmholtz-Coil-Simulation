import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from CoilListRow import CoilListRow


class HelmholtzCoilPreset(list):
    def __init__(self):
        coil_row_1 = CoilListRow()
        coil_row_2 = CoilListRow()
        
        coil_row_1.set_values(shape="Circular", radius=0.5, turns=100, current=1.0, position=0.25)
        coil_row_2.set_values(shape="Circular", radius=0.5, turns=100, current=1.0, position=-0.25)

        self.append(coil_row_1)
        self.append(coil_row_2)