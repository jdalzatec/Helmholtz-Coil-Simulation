import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject, GLib

from GridWindow import GridWindow
from CoilsListBox import CoilsListBox
from CoilListRow import CoilListRow
from Presets import HelmholtzCoilPreset
from Presets import MaxwellCoilPreset
from Presets import WangCoilPreset
from Presets import TetraCoilPreset
from Presets import LeeWhitingCoilPreset
from Presets import RandomCoilPreset
from coil import Coil, CreateCoil
from Simulation import Simulation
import random


class InputWindow():
    def __init__(self, glade_file):
        self.glade_file = glade_file
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        
        self.window = self.builder.get_object("wndInput")
        self.btnDeleteAll = self.builder.get_object("btnDeleteAll")
        self.btnAddCoil = self.builder.get_object("btnAddCoil")
        
        self.btnHelmholtzConfig = self.builder.get_object("btnHelmholtzConfig")
        self.btnMaxwellConfig = self.builder.get_object("btnMaxwellConfig")
        self.btnWangConfig = self.builder.get_object("btnWangConfig")
        self.btnTetracoilConfig = self.builder.get_object("btnTetracoilConfig")
        self.btnLeeConfig = self.builder.get_object("btnLeeConfig")
        self.btnRandomConfig = self.builder.get_object("btnRandomConfig")
        
        self.scrListBox = self.builder.get_object("scrListBox")
        self.btnSimulate = self.builder.get_object("btnSimulate")
        self.chbAutoGrid = self.builder.get_object("chbAutoGrid")
        self.menuColorMap = self.builder.get_object("menuColorMap")
        self.treeData = self.builder.get_object("treeData")
        self.btnOpen = self.builder.get_object("btnOpen")
        self.btnNew = self.builder.get_object("btnNew")
        self.btnQuit = self.builder.get_object("btnQuit")
        
        self.listBox = CoilsListBox()
        self.scrListBox.add_with_viewport(self.listBox)

        self.window.connect("destroy", Gtk.main_quit)

        self.btnHelmholtzConfig.connect("activate", self.on_helmholtz_config)
        self.btnMaxwellConfig.connect("activate", self.on_maxwell_config)
        self.btnWangConfig.connect("activate", self.on_wang_config)
        self.btnTetracoilConfig.connect("activate", self.on_tetracoil_config)
        self.btnLeeConfig.connect("activate", self.on_lee_config)
        self.btnRandomConfig.connect("activate", self.on_random_config)

        self.btnSimulate.connect("clicked", self.on_simulate)
        self.chbAutoGrid.connect("toggled", self.on_auto_grid)
        self.btnOpen.connect("activate", self.on_import)
        self.btnQuit.connect("activate", Gtk.main_quit)
        self.btnNew.connect("activate", self.listBox.remove_all_coils)



        self.auto_grid = self.chbAutoGrid.get_active()
        self.coils = []
        self.z_min = 0.0
        self.z_max = 0.0
        self.z_points = 0
        self.y_min = 0.0
        self.y_max = 0.0
        self.y_points = 0

        self.window.show_all()
        self.window.maximize()
        Gtk.main()


    def on_helmholtz_config(self, widget):
        self.listBox.update(HelmholtzCoilPreset())

    def on_maxwell_config(self, widget):
        self.listBox.update(MaxwellCoilPreset())

    def on_wang_config(self, widget):
        self.listBox.update(WangCoilPreset())

    def on_tetracoil_config(self, widget):
        self.listBox.update(TetraCoilPreset())

    def on_lee_config(self, widget):
        self.listBox.update(LeeWhitingCoilPreset())

    def on_random_config(self, widget):
        self.listBox.update(RandomCoilPreset(random.randint(2, 10)))


    def on_auto_grid(self, check):
        self.auto_grid = check.get_active()
        print(self.auto_grid)

    def compute_grid(self):
        if len(self.coils) > 0:
            z_arr = [coil.pos_z for coil in self.coils]
            self.z_min = min(z_arr)
            self.z_max = max(z_arr)

            radius_arr = [coil.radius for coil in self.coils]
            self.y_min = -max(radius_arr)
            self.y_max = max(radius_arr)

            if self.z_min == self.z_max:
                self.z_min = self.z_min - self.y_max
                self.z_max = self.z_max + self.y_max

            PMAX = 50
            if abs(self.z_max - self.z_min) > abs(self.y_max - self.y_min):
                self.z_points = PMAX
                self.y_points = int(abs(self.y_max - self.y_min) * PMAX / abs(self.z_max - self.z_min))
            else:
                self.y_points = PMAX
                self.z_points = int(abs(self.z_max - self.z_min) * PMAX / abs(self.y_max - self.y_min))



    def collect_coils_values(self):
        self.coils = []
        for row in list(self.listBox)[:-1]:
            coil_row, = row.get_children()
            coil = CreateCoil(**coil_row.get_values())
            self.coils.append(coil)


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
                self.y_min, self.y_max, self.y_points)



    def insert_grid_manually(self):
        initial_grid = {
            "z_min": self.z_min,
            "z_max": self.z_max,
            "z_points": self.z_points,
            "y_min": self.y_min,
            "y_max": self.y_max,
            "y_points": self.y_points,
        }

        dialog = GridWindow(self.window, "./interfaces/grid.glade", initial_grid)
        
        response = dialog.window.run()

        if response == Gtk.ResponseType.OK:
            self.z_min = float(dialog.txtMinZ.get_text())
            self.z_max = float(dialog.txtMaxZ.get_text())
            self.z_points = int(dialog.txtPointsZ.get_text())
            self.y_min = float(dialog.txtMinY.get_text())
            self.y_max = float(dialog.txtMaxY.get_text())
            self.y_points = int(dialog.txtPointsY.get_text())
            dialog.window.destroy()
            return True

        dialog.window.destroy()
        return False

    def on_import(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self.window,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        filters = Gtk.FileFilter()
        filters.set_name("Excel files")
        filters.add_pattern("*.*.csv")
        filters.add_pattern("*.xls")
        filters.add_pattern("*.xlsx")
        dialog.add_filter(filters)

        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

            import xlrd

            wb = xlrd.open_workbook(filename)
            wInput = wb.sheet_by_name("input")
            wCoils = wb.sheet_by_name('coils')

            self.z_min = wInput.cell_value(0, 1)
            self.z_max = wInput.cell_value(1, 1)
            self.z_points = int(wInput.cell_value(2, 1))
            self.y_min = wInput.cell_value(3, 1)
            self.y_max = wInput.cell_value(4, 1)
            self.y_points = int(wInput.cell_value(5, 1))

            coils = []
            for i in range(wCoils.nrows - 1):
                radius = wCoils.cell_value(i + 1, 0)
                turns = int(wCoils.cell_value(i + 1, 1))
                current = wCoils.cell_value(i + 1, 2)
                position = wCoils.cell_value(i + 1, 3)
                coils.append(CreateCoil("Circular", radius, turns, current, position))

            coil_rows = []
            for coil in coils:
                coil_row = CoilListRow()
                coil_row.set_values(
                    radius=coil.radius,
                    turns=coil.num_turns,
                    current=coil.I, position=coil.pos_z)
                coil_rows.append(coil_row)
            self.listBox.update(coil_rows)

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

GObject.threads_init()
window = InputWindow("./interfaces/input.glade")
print("hola")