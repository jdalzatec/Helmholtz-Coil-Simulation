import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
# from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

class Zoom():
    def __init__(self, parent, simulation, colormap, zoom_value):
        self.parent = parent
        self.zoom_value = zoom_value
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./interfaces/zoom.glade")
        self.window = self.builder.get_object("wndZoom")
        

