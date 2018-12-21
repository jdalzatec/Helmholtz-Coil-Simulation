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


    # def update_grid_info(self):
    #     mode = "Auto" if self.auto_grid else "Manual"
    #     text = "Grid (%s)" % mode
    #     if mode == "Auto":
    #         text += ": Z from %s to %s (%i points); ρ from %s to %s (%i points);" % (
    #         self.z_min, self.z_max, self.z_points,
    #         self.rho_min, self.rho_max, self.rho_points)
    #     self.lblGridInfo.set_text(text)
    
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

            self.z_points = 100
            self.rho_points = 100


    def collect_coils_values(self):
        self.coils = []
        for row in list(self.listBox)[:-1]:
            coil_row, = row.get_children()
            if coil_row.validate_values():
                coil = CreateCoil(**coil_row.get_values())
                self.coils.append(coil)


    def on_simulate(self, widget):
        self.collect_coils_values()

        if len(self.coils) == 0:
            print("No hay bobinas")
            return

        self.compute_grid()
        if not self.auto_grid:
            self.insert_grid_manually()



        # if ready:
        #     self.compute_grid()

        #     self.simulation = Simulation(self.coils,
        #         self.z_min, self.z_max, self.z_points,
        #         self.rho_min, self.rho_max, self.rho_points)


    def insert_grid_manually(self):
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

            dialog.destroy()

        elif response == Gtk.ResponseType.HELP:
            self.compute_grid()

            dialog.txtMinZ.set_property("text", str(self.z_min))
            dialog.txtMaxZ.set_property("text", str(self.z_max))
            dialog.txtPointsZ.set_property("text", str(self.z_points))
            dialog.txtMinRho.set_property("text", str(self.rho_min))
            dialog.txtMaxRho.set_property("text", str(self.rho_max))
            dialog.txtPointsRho.set_property("text", str(self.rho_points))


            
        else:
            dialog.destroy()


        print(response)

        
        # Gtk.main()

window = InputWindow("./interfaces/input2.glade")
print("hola")














