import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


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
        self.btnSettings = self.builder.get_object("btnSettings")
        self.lblGridInfo = self.builder.get_object("lblGridInfo")
        
        self.listBox = CoilsListBox()
        self.scrListBox.add_with_viewport(self.listBox)

        self.window.connect("destroy", Gtk.main_quit)
        self.btnAddCoil.connect("clicked", self.listBox.create_coil_row)
        self.btnDeleteAll.connect("clicked", self.listBox.remove_all_coils)
        self.btnHelmholtzConfig.connect("activate", self.on_helmholtz_config)
        self.btnSimulate.connect("clicked", self.on_simulate)
        self.btnSettings.connect("clicked", self.on_settings)


        self.auto_grid = True
        self.coils = []
        self.z_min = 0.0
        self.z_max = 0.0
        self.z_points = 0
        self.rho_min = 0.0
        self.rho_max = 0.0
        self.rho_points = 0

        self.update_grid_info()

        self.window.show_all()
        Gtk.main()
    
    def update_grid_info(self):
        mode = "Auto" if self.auto_grid else "Manual"
        text = "Grid (%s): Z from %s to %s (%i points); ρ from %s to %s (%i points);" % (
            mode, self.z_min, self.z_max, self.z_points,
            self.rho_min, self.rho_max, self.rho_points)
        self.lblGridInfo.set_text(text)
    
    def on_helmholtz_config(self, widget):
        self.listBox.update(HelmholtzCoilPreset())
        self.collect_coils_values()
        self.compute_grid_automatically()
        self.update_grid_info()

    def compute_grid_automatically(self):
        if self.auto_grid:
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

                self.z_points = 100
                self.rho_points = 100
            else:
                self.z_min = 0.0
                self.z_max = 0.0
                self.z_points = 0
                self.rho_min = 0.0
                self.rho_max = 0.0
                self.rho_points = 0


    def collect_coils_values(self):
        self.coils = []
        for row in list(self.listBox)[:-1]:
            coil_row, = row.get_children()
            if coil_row.validate_values():
                coil = CreateCoil(**coil_row.get_values())
                self.coils.append(coil)

        if len(self.coils) == 0:
            # raise Exception("Paila")
            print("paila")
            return False

        return True


    def on_simulate(self, widget):
        ready = self.collect_coils_values()
        if ready:
            self.compute_grid_automatically()

            self.simulation = Simulation(self.coils,
                self.z_min, self.z_max, self.z_points,
                self.rho_min, self.rho_max, self.rho_points)


    def on_settings(self, widget):
        ready = self.collect_coils_values()
        if ready:
            self.compute_grid_automatically()
            self.auto_grid = False

        dialog = GridWindow(self.window)

        dialog.txtMinZ.set_property("text", str(self.z_min))
        dialog.txtMaxZ.set_property("text", str(self.z_max))
        dialog.txtPointsZ.set_property("text", str(self.z_points))
        dialog.txtMinRho.set_property("text", str(self.rho_min))
        dialog.txtMaxRho.set_property("text", str(self.rho_max))
        dialog.txtPointsRho.set_property("text", str(self.rho_points))


        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.z_min = float(dialog.txtMinZ.get_text())
            self.z_max = float(dialog.txtMaxZ.get_text())
            self.z_points = int(dialog.txtPointsZ.get_text())
            self.rho_min = float(dialog.txtMinRho.get_text())
            self.rho_max = float(dialog.txtMaxRho.get_text())
            self.rho_points = int(dialog.txtPointsRho.get_text())
        elif response == Gtk.ResponseType.HELP:
            self.auto_grid = True
            ready = self.collect_coils_values()
            if ready:
                self.compute_grid_automatically()
        else:
            pass

        self.update_grid_info()

        print(response)

        dialog.destroy()
        # Gtk.main()

window = InputWindow("./interfaces/input2.glade")
print("hola")














