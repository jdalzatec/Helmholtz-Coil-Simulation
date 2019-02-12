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

        self.simulation = simulation

        self.colormap = "jet"

        self.window.set_transient_for(self.parent)

        self.window.connect("destroy", self.quit)
        self.btnBack.connect("clicked", self.on_back)
        self.btnZoom.connect("clicked", self.on_zoom)
        self.btnHomogeneity.connect("clicked", self.on_homogeneity)

        z_arr = [coil.pos_z for coil in self.simulation.coils]
        radius_arr = [coil.radius for coil in self.simulation.coils]
        
        xlims = (min(z_arr), max(z_arr))
        ylims = (-max(radius_arr), max(radius_arr))

        self.plot = PlotBox(self, self.simulation,
            self.colormap, self.statBar, xlims, ylims)
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
        self.window.maximize()

        self.populate_input_parameters()

        self.zooms = []

    def on_zoom(self, widget):
        self.plot.clear_rectangle()
        zoom = ZoomWindow(self, self.simulation, self.colormap)

    def on_homogeneity(self, widget):
        homogeneity = HomogeneityWindow(self, self.simulation, self.colormap)

    def populate_input_parameters(self):
        text = ""
        text += "{:12} =\t\t {}\n".format("Min Z", str(self.simulation.z_min))
        text += "{:12} =\t\t {}\n".format("Max Z", str(self.simulation.z_max))
        text += "{:12} =\t\t {}\n".format("Points Z", str(self.simulation.z_points))
        text += "{:12} =\t\t {}\n".format("Min Y", str(self.simulation.y_min))
        text += "{:12} =\t\t {}\n".format("Max Y", str(self.simulation.y_max))
        text += "{:12} =\t\t {}\n".format("Points Y", str(self.simulation.y_points))

        text += "\n"

        text += "{:15}{:15}{:15}{:15}\n".format(
            "Radius [m]", "Turns", "Current [A]", "Position [m]")

        for coil in self.simulation.coils:
            text += "{:<20f}{:<20d}{:<20f}{:<20f}\n".format(
                coil.radius, coil.num_turns, coil.I, coil.pos_z)

        self.txtInputParameters.get_buffer().set_text(text)



    def on_color_bar_menu(self, widget, name):
        self.colormap = name
        self.plot.update_plot(name)


    def quit(self, widget):
        if not self.parent.get_visible():
            Gtk.main_quit()
        else:
            self.window.close()


    def on_back(self, widget):
        self.parent.show()
        self.window.close()