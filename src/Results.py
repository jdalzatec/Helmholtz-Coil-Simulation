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


class Results():
    def __init__(self, parent, simulation):
        self.parent = parent
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./interfaces/results.glade")
        self.window = self.builder.get_object("wndResults")
        self.boxPlot = self.builder.get_object("boxPlot")
        self.btnBack = self.builder.get_object("btnBack")
        self.btnZoom = self.builder.get_object("btnZoom")
        self.statBar = self.builder.get_object("statBar")
        self.menuColorMap = self.builder.get_object("menuColorMap")
        self.treeData = self.builder.get_object("treeData")
        self.treeGridInfo = self.builder.get_object("treeGridInfo")
        self.treeCoilsInfo = self.builder.get_object("treeCoilsInfo")

        self.simulation = simulation

        self.colormap = "jet"

        self.window.set_transient_for(self.parent)
        self.window.maximize()

        self.window.connect("destroy", self.quit)
        self.btnBack.connect("clicked", self.on_back)
        self.btnZoom.connect("clicked", self.on_zoom)

        self.plot = PlotBox(self.window, self.simulation, self.colormap)
        self.boxPlot.pack_start(self.plot.boxPlot, True, True, 0)

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

        self.window.show_all()
        self.populate_input_params_trees()


    def on_zoom(self, widget):
        print("hola")

    def populate_input_params_trees(self):
        coilsList = Gtk.ListStore(str, float, int, float, float)
        for coil in self.simulation.coils:
            coilsList.append([coil.shape, coil.radius, coil.num_turns, coil.I, coil.pos_z])

        self.treeCoilsInfo.set_model(coilsList)

        for i, column_title in enumerate(["Shape", "Radius [m]", "Turns", "Current [A]", "Position [m]"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_expand(True)
            self.treeCoilsInfo.append_column(column)

        # now for the grid
        lblMinZ = self.builder.get_object("lblMinZ")
        lblMaxZ = self.builder.get_object("lblMaxZ")
        lblPointsZ = self.builder.get_object("lblPointsZ")
        lblMinRho = self.builder.get_object("lblMinRho")
        lblMaxRho = self.builder.get_object("lblMaxRho")
        lblPointsRho = self.builder.get_object("lblPointsRho")


        lblMinZ.set_label(str(self.simulation.z_min))
        lblMaxZ.set_label(str(self.simulation.z_max))
        lblPointsZ.set_label(str(self.simulation.z_points))
        lblMinRho.set_label(str(self.simulation.rho_min))
        lblMaxRho.set_label(str(self.simulation.rho_max))
        lblPointsRho.set_label(str(self.simulation.rho_points))


    def on_color_bar_menu(self, widget, name, first=False):
        self.colormap = name
        self.plot.update_plot(name)

    # def plot_point(self, event):
    #     if event.button != 1:
    #         return

    #     if (event.xdata is None):
    #         return

    #     if self.pan_active or self.zoom_active:
    #         return

    #     x, y = event.xdata, event.ydata
    #     self.ax.scatter(x, y, s=10, c="black")
    #     self.statBar.push(1, ("Coordinates: x = " + str(round(x, 3)) + "; y = " + str(round(y, 3))))
        

    def update_cursor_position(self, event):
        if event.button != 1:
            return

        if (event.xdata is None):
            return

        if self.pan_active or self.zoom_active:
            return
            
        if event.inaxes:
            x = event.xdata
            y = event.ydata
            self.ax.scatter(x, y, s=10, c="black")
            self.statBar.push(1, ("Coordinates: x = " + str(round(x, 3)) + "; y = " + str(round(y, 3))))

    def on_revert_limits(self, widget):
        # size = numpy.max(self.simulation.norm) - numpy.min(self.simulation.norm)
        # mid = 0.5 * (numpy.max(self.simulation.norm) + numpy.min(self.simulation.norm))
        # self.min_val = mid - 0.5 * size
        # self.max_val = mid + 0.5 * size

        self.min_val = numpy.min(self.simulation.norm)
        self.max_val = self.min_val * 5
        
        self.txtMaxVal.set_property("text", self.format % self.max_val)
        self.txtMinVal.set_property("text", self.format % self.min_val)
        
        self.on_apply_limits(None)


    # def on_apply_limits(self, widget):
    #     self.copy_norm = self.simulation.norm.copy()

    #     self.txtMaxVal.set_property("text", self.format % eval(self.txtMaxVal.get_property("text")))
    #     self.txtMinVal.set_property("text", self.format % eval(self.txtMinVal.get_property("text")))

    #     self.max_val = float(self.txtMaxVal.get_property("text"))
    #     self.min_val = float(self.txtMinVal.get_property("text"))

    #     if self.max_val > self.min_val:
    #         # surpass is for set the >= symbol in case of norm >= max_val
    #         self.surpass = False
    #         if numpy.any(self.simulation.norm >= self.max_val):
    #             self.surpass = True
    #             self.copy_norm[self.simulation.norm >= self.max_val] = self.max_val

    #         # underpass is for set the <= symbol in case of norm <= max_val
    #         self.underpass = False
    #         if numpy.any(self.simulation.norm <= self.min_val):
    #             self.underpass = True
    #             self.copy_norm[self.simulation.norm <= self.min_val] = self.min_val

    #         self.plot()
    #     else:
    #         print("cómo chuchas")
    #     print(self.underpass, self.surpass)


    def quit(self, widget):
        if not self.parent.get_visible():
            Gtk.main_quit()
        else:
            self.window.close()


    def on_back(self, widget):
        self.parent.show()
        self.window.close()