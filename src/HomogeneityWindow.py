import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
# from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

from PlotWindow import PlotBox
from functions import uniformity
from About import AboutWindow
from ErrorMessage import ErrorMessage
import numpy

class HomogeneityWindow():
    def __init__(self, parent, simulation, colormap, zoom_value=0, homogeneity=0.0):
        self.zoom = 100.0
        self.homo = 50.0

        self.parent = parent
        self.simulation = simulation
        self.colormap = colormap
        self.zoom_value = zoom_value
        self.homogeneity = homogeneity

        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./interfaces/homogeneity.glade")
        self.window = self.builder.get_object("wndHomo")
        self.statBar = self.builder.get_object("statBar")
        self.btnApplyHomo = self.builder.get_object("btnApplyHomo")
        self.btnApplyZoom = self.builder.get_object("btnApplyZoom")
        self.txtZoomValue = self.builder.get_object("txtZoomValue")
        self.txtHomoValue = self.builder.get_object("txtHomoValue")
        self.boxPlot = self.builder.get_object("boxPlot")
        self.menuColorMap = self.builder.get_object("menuColorMap")
        self.btnQuit = self.builder.get_object("btnQuit")
        self.btnAbout = self.builder.get_object("btnAbout")


        self.window.set_transient_for(self.parent.window)

        self.txtZoomValue.connect("key-press-event", self.on_key_press_event_zoom)
        self.txtHomoValue.connect("key-press-event", self.on_key_press_event_homo)


        self.btnApplyZoom.connect("clicked", self.on_apply_zoom)
        self.btnApplyHomo.connect("clicked", self.on_apply_homo)
        self.btnQuit.connect("activate", lambda _: self.window.close())
        self.btnAbout.connect("activate", lambda _: AboutWindow(self.window))

        self.plot = PlotBox(self, self.simulation, self.colormap, self.statBar, binary_colors=True)
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

        self.txtZoomValue.set_text(str(self.zoom))
        self.txtHomoValue.set_text(str(self.homo))
        self.btnApplyHomo.emit("clicked")

        self.plot.boxLimits.hide()

    def on_key_press_event_zoom(self, widget, event):

        print("Key press on widget: ", widget)
        print("          Modifiers: ", event.state)
        print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))

        # check the event modifiers (can also use SHIFTMASK, etc)
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)

        # see if we recognise a keypress
        if Gdk.keyval_name(event.keyval) == 'Return':
            print("Enter")
            self.on_apply_zoom(None)

    def on_key_press_event_homo(self, widget, event):

        print("Key press on widget: ", widget)
        print("          Modifiers: ", event.state)
        print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))

        # check the event modifiers (can also use SHIFTMASK, etc)
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)

        # see if we recognise a keypress
        if Gdk.keyval_name(event.keyval) == 'Return':
            print("Enter")
            self.on_apply_homo(None)

    def isNumeric(self, val, func=float):
        try:
            func(val)
            return True
        except Exception as e:
            return False

    def on_apply_zoom(self, widget):
        self.zoom = float(self.txtZoomValue.get_text()) if self.isNumeric(self.txtZoomValue.get_text()) else False

        if not (self.zoom and self.zoom > 0):
            ErrorMessage(self.window, "Invalid input parameters", "Zoom value must be a positive real.")
            return

        print(self.zoom)
        zmin, zmax, ymin, ymax = self.plot.compute_zoom(self.zoom)

        self.parent.plot.draw_rectangle(zmin, zmax, ymin, ymax)


    def on_apply_homo(self, widget):
        self.homo = float(self.txtHomoValue.get_text()) if self.isNumeric(self.txtHomoValue.get_text()) else False

        if not (self.homo and self.homo > 0 and self.homo <= 100):
            ErrorMessage(self.window, "Invalid input parameters", "Homogeneity value must be a positive real lower than 100.")
            return


        self.txtZoomValue.set_text("100.0")
        

        self.zoom = float(self.txtZoomValue.get_text()) if self.isNumeric(self.txtZoomValue.get_text()) else False

        if not (self.zoom and self.zoom > 0):
            ErrorMessage(self.window, "Invalid input parameters", "Zoom value must be a positive real.")
            return

        center, uniformity_grid = self.compute_uniformity()
        homo_grid = numpy.where(uniformity_grid >= (self.homo / 100), 1, 0)

        self.plot.initial_norm = homo_grid.copy()
        zmin, zmax, ymin, ymax = self.plot.compute_zoom(self.zoom)


        self.parent.plot.draw_rectangle(zmin, zmax, ymin, ymax)



    def compute_uniformity(self):
        zmid = (self.simulation.z_max + self.simulation.z_min) * 0.5
        ymid = (self.simulation.y_max + self.simulation.y_min) * 0.5
        center = (zmid, ymid)
        return center, uniformity(
            self.simulation.coils, self.simulation.norm, self.simulation.mu0, center)

    def on_color_bar_menu(self, widget, name):
        self.colormap = name
        self.plot.update_plot(name)