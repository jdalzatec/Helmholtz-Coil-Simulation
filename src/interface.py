import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject, GLib

from Results import Results


from GridWindow import GridWindow
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
        self.btnHelmholtzConfig = self.builder.get_object("btnHelmholtzConfig")
        self.scrListBox = self.builder.get_object("scrListBox")
        self.btnSimulate = self.builder.get_object("btnSimulate")
        self.chbAutoGrid = self.builder.get_object("chbAutoGrid")
        
        self.listBox = CoilsListBox()
        self.scrListBox.add_with_viewport(self.listBox)

        self.window.connect("destroy", Gtk.main_quit)
        self.btnAddCoil.connect("clicked", self.listBox.create_coil_row)
        self.btnDeleteAll.connect("clicked", self.listBox.remove_all_coils)
        self.btnHelmholtzConfig.connect("activate", self.on_helmholtz_config)
        self.btnSimulate.connect("clicked", self.on_simulate)
        self.chbAutoGrid.connect("activate", self.on_auto_grid)


        self.auto_grid = self.chbAutoGrid.get_active()
        self.coils = []
        self.z_min = 0.0
        self.z_max = 0.0
        self.z_points = 0
        self.rho_min = 0.0
        self.rho_max = 0.0
        self.rho_points = 0

        self.window.show_all()
        Gtk.main()


    def on_auto_grid(self, check):
        self.auto_grid = check.get_active()


    def on_helmholtz_config(self, widget):
        self.listBox.update(HelmholtzCoilPreset())


    def compute_grid(self):
        if len(self.coils) > 0:
            z_arr = [coil.pos_z for coil in self.coils]
            self.z_min = min(z_arr)
            self.z_max = max(z_arr)

            radius_arr = [coil.radius for coil in self.coils]
            self.rho_min = 0.0
            self.rho_max = max(radius_arr)

            if self.z_min == self.z_max:
                self.z_min = self.z_min - self.rho_max
                self.z_max = self.z_max + self.rho_max

            self.z_points = 50
            self.rho_points = 50


    def collect_coils_values(self):
        self.coils = []
        for row in list(self.listBox)[:-1]:
            coil_row, = row.get_children()
            if coil_row.validate_values():
                coil = CreateCoil(**coil_row.get_values())
                self.coils.append(coil)

    def wait_for_the_simulation(self, thread):
       if not thread.is_alive():
           thread.join()
           print("finish")
       else:
           GLib.timeout_add(10, self.wait_for_the_simulation, thread)

    def on_simulate(self, widget):
        self.collect_coils_values()

        if len(self.coils) == 0:
            print("No hay bobinas")
            return

        self.compute_grid()
        ready = True
        if not self.auto_grid:
            ready = self.insert_grid_manually()

        if ready:
            print("lets go")
            self.simulation = Simulation(self, self.coils,
                self.z_min, self.z_max, self.z_points,
                self.rho_min, self.rho_max, self.rho_points)

            self.wait_for_the_simulation(self.simulation.thread)



    def insert_grid_manually(self):
        initial_grid = {
            "z_min": self.z_min,
            "z_max": self.z_max,
            "z_points": self.z_points,
            "rho_min": self.rho_min,
            "rho_max": self.rho_max,
            "rho_points": self.rho_points,
        }

        dialog = GridWindow(self.window, "./interfaces/grid.glade", initial_grid)
        
        response = dialog.window.run()

        if response == Gtk.ResponseType.OK:
            self.z_min = float(dialog.txtMinZ.get_text())
            self.z_max = float(dialog.txtMaxZ.get_text())
            self.z_points = int(dialog.txtPointsZ.get_text())
            self.rho_min = float(dialog.txtMinRho.get_text())
            self.rho_max = float(dialog.txtMaxRho.get_text())
            self.rho_points = int(dialog.txtPointsRho.get_text())
            dialog.window.destroy()
            return True

        dialog.window.destroy()
        return False

GObject.threads_init()
window = InputWindow("./interfaces/input2.glade")
print("hola")