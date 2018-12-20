import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


from CoilsListBox import CoilsListBox
from CoilListRow import CoilListRow
from Presets import HelmholtzCoilPreset
from coil import Coil, CreateCoil
from Simulation import Simulation


class InputWindow():
    def __init__(self, glade_file):
        self.glade_file = glade_file
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        
        self.window = self.builder.get_object("wndInput")
        self.btnDeleteAll = self.builder.get_object("btnDeleteAll")
        self.btnAddCoil = self.builder.get_object("btnAddCoil")
        self.btnSimulate = self.builder.get_object("btnSimulate")
        self.btnHelmholtzConfig = self.builder.get_object("btnHelmholtzConfig")
        self.scrListBox = self.builder.get_object("scrListBox")
        
        self.listBox = CoilsListBox()
        self.scrListBox.add_with_viewport(self.listBox)

        self.window.connect("destroy", Gtk.main_quit)
        self.btnAddCoil.connect("clicked", self.listBox.create_coil_row)
        self.btnDeleteAll.connect("clicked", self.listBox.remove_all_coils)
        self.btnHelmholtzConfig.connect("activate", self.on_helmholtz_config)
        self.btnSimulate.connect("clicked", self.on_simulate)

        self.window.show_all()
        Gtk.main()
    
    
    def on_helmholtz_config(self, widget):
        self.listBox.update(HelmholtzCoilPreset())
    

    def on_simulate(self, widget):
        coils = []
        for row in list(self.listBox)[:-1]:
            coil_row, = row.get_children()
            if coil_row.validate_values():
                coil = CreateCoil(**coil_row.get_values())
                coils.append(coil)

        if len(coils) == 0:
            raise Exception("Paila")

        z_min = -0.5
        z_max = 0.5
        z_points = 100
        rho_min = 0.0
        rho_max = 1.0
        rho_points = 100
        self.simulation = Simulation(coils, z_min, z_max, z_points, rho_min, rho_max, rho_points)

window = InputWindow("./interfaces/input2.glade")
print("hola")














