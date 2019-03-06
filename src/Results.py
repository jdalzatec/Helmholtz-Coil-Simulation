import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
# from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

import numpy
from PlotWindow import PlotBox
from ZoomWindow import ZoomWindow
from HomogeneityWindow import HomogeneityWindow
from coil import Coil, CreateCoil
from CoilListRow import CoilListRow


class Results():
    def __init__(self, parent, simulation):
        self.parent = parent
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./interfaces/results.glade")
        self.window = self.builder.get_object("wndResults")
        self.boxPlot = self.builder.get_object("boxPlot")
        self.btnBack = self.builder.get_object("btnBack")
        self.btnZoom = self.builder.get_object("btnZoom")
        self.btnHomogeneity = self.builder.get_object("btnHomogeneity")
        self.statBar = self.builder.get_object("statBar")
        self.menuColorMap = self.builder.get_object("menuColorMap")
        self.txtInputParameters = self.builder.get_object("txtInputParameters")
        self.txtElectircalParameters = self.builder.get_object("txtElectircalParameters")
        self.btnSaveAs = self.builder.get_object("btnSaveAs")
        self.btnOpen = self.builder.get_object("btnOpen")
        self.btnQuit = self.builder.get_object("btnQuit")

        self.simulation = simulation

        self.colormap = "jet"

        self.window.set_transient_for(self.parent.window)

        self.window.connect("destroy", self.quit)
        self.btnBack.connect("clicked", self.on_back)
        self.btnZoom.connect("clicked", self.on_zoom)
        self.btnHomogeneity.connect("clicked", self.on_homogeneity)
        self.btnSaveAs.connect("activate", self.on_export)
        self.btnOpen.connect("activate", self.on_import)
        self.btnQuit.connect("activate", Gtk.main_quit)


        # Get a list of the colormaps in matplotlib.  Ignore the ones that end with
        # '_r' because these are simply reversed versions of ones that don't end
        # with '_r'
        maps = sorted(m for m in pyplot.cm.datad if not m.endswith("_r"))

        firstitem = Gtk.RadioMenuItem(self.colormap)
        firstitem.set_active(True)
        firstitem.connect('activate', self.on_color_bar_menu, self.colormap)
        self.menuColorMap.append(firstitem)
        for name in maps:
            if name != self.colormap:
                item = Gtk.RadioMenuItem.new_with_label([firstitem], name)
                item.set_active(False)
                item.connect('activate', self.on_color_bar_menu, name)
                self.menuColorMap.append(item)

        self.load_simulation()
        
        self.window.maximize()
        self.window.show_all()



    def load_simulation(self):
        z_arr = [coil.pos_z for coil in self.simulation.coils]
        radius_arr = [coil.radius for coil in self.simulation.coils]
        
        xlims = (min(z_arr), max(z_arr))
        ylims = (-max(radius_arr), max(radius_arr))

        for ch in self.boxPlot:
            self.boxPlot.remove(ch)

        self.plot = PlotBox(self, self.simulation,
            self.colormap, self.statBar, xlims, ylims)
        self.boxPlot.pack_start(self.plot.boxPlot, True, True, 0)
        self.populate_input_parameters()
        self.populate_electrical_parameters()

        self.window.show_all()




    def on_zoom(self, widget):
        self.plot.clear_rectangle()
        zoom = ZoomWindow(self, self.simulation, self.colormap)

    def on_homogeneity(self, widget):
        homogeneity = HomogeneityWindow(self, self.simulation, self.colormap)

    def populate_input_parameters(self):
        text = "\n"
        text += "\t{}\t\t=\t\t{}\n".format("Min Z", str(self.simulation.z_min))
        text += "\t{}\t\t=\t\t{}\n".format("Max Z", str(self.simulation.z_max))
        text += "\t{}\t\t=\t\t{}\n".format("Points Z", str(self.simulation.z_points))
        text += "\t{}\t\t=\t\t{}\n".format("Min Y", str(self.simulation.y_min))
        text += "\t{}\t\t=\t\t{}\n".format("Max Y", str(self.simulation.y_max))
        text += "\t{}\t\t=\t\t{}\n".format("Points Y", str(self.simulation.y_points))

        text += "\n"

        text += "\t{}\t\t{}\t\t{}\t\t{}\n".format(
            "Radius [m]", "Turns", "Current [A]", "Position [m]")

        for coil in self.simulation.coils:
            text += "\t{:.5f}\t\t\t{:d}\t\t\t{:.5f}\t\t\t{:.5f}\n".format(
                coil.radius, coil.num_turns, coil.I, coil.pos_z)

        self.txtInputParameters.get_buffer().set_text(text)


    def populate_electrical_parameters(self):
        gauge, diameter, section, resist, Inominal = numpy.loadtxt("awg.dat", unpack=True)
        Imax = max([coil.I for coil in self.simulation.coils])
        index = numpy.argmin(Inominal > Imax) - 1
        gauge = gauge[index]
        diameter = diameter[index]
        section = section[index]
        resist = resist[index]
        Inominal = Inominal[index]

        length = sum([2*numpy.pi*coil.radius*coil.num_turns for coil in self.simulation.coils]) * 1.05
        
        text = "\n"
        text += "\t{}\t\t\t\t\t=\t\t{:d}\n".format("AWG Gauge", int(gauge))
        text += "\t{}\t\t\t=\t\t{:.5f}\n".format("Wire diameter [mm]", diameter)
        text += "\t{}\t\t=\t\t{:.5f}\n".format("Wire sectional area [mm2]", section)
        text += "\t{}\t\t\t=\t\t{:.5f}\n".format("Nominal current [A]", Inominal)
        text += "\t{}\t\t\t=\t\t{:.5f}\n".format("Maximum current [A]", Inominal * 1.1)
        text += "\t{}\t\t\t=\t\t{:.5f}\n".format("Total wire length [m]", length)
        text += "\t{}\t\t=\t\t{:.5f}\n".format("Wire resistance [Ohm]", resist * length / 1000)

        self.txtElectircalParameters.get_buffer().set_text(text)



    def on_color_bar_menu(self, widget, name):
        self.colormap = name
        self.plot.update_plot(name)


    def quit(self, widget):
        if not self.parent.window.get_visible():
            Gtk.main_quit()
        else:
            self.window.close()


    def on_back(self, widget):
        coil_rows = []
        for coil in self.simulation.coils:
            coil_row = CoilListRow()
            coil_row.set_values(
                radius=coil.radius,
                turns=coil.num_turns,
                current=coil.I, position=coil.pos_z)
            coil_rows.append(coil_row)
        self.parent.listBox.update(coil_rows)
        self.parent.window.show()
        self.window.close()


    def on_export(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self.window,
            Gtk.FileChooserAction.SAVE,
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
            print("Open clicked")
            print("File selected: " + filename)
            if "." not in filename:
                filename += ".xls"

            import xlwt

            wb = xlwt.Workbook()
            wInput = wb.add_sheet('Simulation parameters')
            wCoils = wb.add_sheet('Input parameters')
            wBy = wb.add_sheet('B y')
            wBz = wb.add_sheet('B z')
            wBnorm = wb.add_sheet('B norm')
            title_style = xlwt.easyxf('font: bold 1') 

            wInput.write(0, 0, "Min Z", title_style)
            wInput.write(0, 1, self.simulation.z_min)
            wInput.write(1, 0, "Max Z", title_style)
            wInput.write(1, 1, self.simulation.z_max)
            wInput.write(2, 0, "Points Z", title_style)
            wInput.write(2, 1, self.simulation.z_points - 1)
            wInput.write(3, 0, "Min Y", title_style)
            wInput.write(3, 1, self.simulation.y_min)
            wInput.write(4, 0, "Max Y", title_style)
            wInput.write(4, 1, self.simulation.y_max)
            wInput.write(5, 0, "Points Y", title_style)
            wInput.write(5, 1, self.simulation.y_points - 1)

            wCoils.write(0, 0, "Radius [m]", title_style)
            wCoils.write(0, 1, "Num. turns", title_style)
            wCoils.write(0, 2, "Current [A]", title_style)
            wCoils.write(0, 3, "Pos. Z [m]", title_style)

            for i, coil in enumerate(self.simulation.coils):
                wCoils.write(i + 1, 0, coil.radius)
                wCoils.write(i + 1, 1, coil.num_turns)
                wCoils.write(i + 1, 2, coil.I)
                wCoils.write(i + 1, 3, coil.pos_z)

            for i, val in enumerate(self.simulation.z_arr):
                wBz.write(0, i + 1, val, title_style)
                wBy.write(0, i + 1, val, title_style)
                wBnorm.write(0, i + 1, val, title_style)

            for i, val in enumerate(self.simulation.y_arr):
                wBz.write(i + 1, 0, val, title_style)
                wBy.write(i + 1, 0, val, title_style)
                wBnorm.write(i + 1, 0, val, title_style)

            for i, _ in enumerate(self.simulation.z_arr):
                for j, _ in enumerate(self.simulation.y_arr):
                    wBz.write(j + 1, i + 1, self.simulation.Bz_grid[i, j])
                    wBy.write(j + 1, i + 1, self.simulation.Brho_grid[i, j])
                    wBnorm.write(j + 1, i + 1, self.simulation.norm[i, j])


            wb.save(filename)

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()



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
            wInput = wb.sheet_by_name("Simulation parameters")
            wCoils = wb.sheet_by_name('Input parameters')
            wBy = wb.sheet_by_name('B y')
            wBz = wb.sheet_by_name('B z')
            wBnorm = wb.sheet_by_name('B norm')

            z_min = wInput.cell_value(0, 1)
            z_max = wInput.cell_value(1, 1)
            z_points = int(wInput.cell_value(2, 1))
            y_min = wInput.cell_value(3, 1)
            y_max = wInput.cell_value(4, 1)
            y_points = int(wInput.cell_value(5, 1))

            coils = []
            for i in range(wCoils.nrows - 1):
                radius = wCoils.cell_value(i + 1, 0)
                turns = int(wCoils.cell_value(i + 1, 1))
                current = wCoils.cell_value(i + 1, 2)
                position = wCoils.cell_value(i + 1, 3)
                coils.append(CreateCoil("Circular", radius, turns, current, position))

            z_arr = []
            for i in range(wBz.ncols - 1):
                z_arr.append(wBz.cell_value(0, i + 1))

            y_arr = []
            for i in range(wBz.nrows - 1):
                y_arr.append(wBz.cell_value(i + 1, 0))

            Bz_grid = numpy.zeros(shape=(len(z_arr), len(y_arr)))
            Brho_grid = numpy.zeros(shape=(len(z_arr), len(y_arr)))
            norm = numpy.zeros(shape=(len(z_arr), len(y_arr)))
            for i in range(len(z_arr) - 1):
                for j in range(len(y_arr) - 1):
                    Bz_grid[i, j] = wBz.cell_value(j + 1, i + 1)
                    Brho_grid[i, j] = wBy.cell_value(j + 1, i + 1)
                    norm[i, j] = wBnorm.cell_value(j + 1, i + 1)

            self.simulation.set_data(coils, z_min, z_max, z_points, y_min, y_max, y_points,
                 z_arr, y_arr, Bz_grid, Brho_grid, norm)


            self.load_simulation()

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()