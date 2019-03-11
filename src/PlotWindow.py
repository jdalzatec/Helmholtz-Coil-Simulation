import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

import matplotlib
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
# from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
import matplotlib.patches as patches

import numpy
from functions import *
from ErrorMessage import ErrorMessage


class PlotBox():
    def __init__(self, parent, simulation, colormap, statBar, z_lims=None, y_lims=None, binary_colors=False):
        self.parent = parent
        self.simulation = simulation
        self.colormap = colormap
        self.format = '%.2E'
        self.statBar = statBar

        self.builder = Gtk.Builder()
        self.builder.add_from_file("./interfaces/toolbar.glade")
        wnd = self.builder.get_object("wndToolBar")
        self.toolbar = self.builder.get_object("boxToolBar")
        self.boxLimits = self.builder.get_object("boxLimits")
        wnd.remove(self.toolbar)
        self.btnApplyLimits = self.builder.get_object("btnApplyLimits")
        self.txtMinLimit = self.builder.get_object("txtMinLimit")
        self.txtMaxLimit = self.builder.get_object("txtMaxLimit")
        self.btnRestore = self.builder.get_object("btnRestore")
        self.btnSave = self.builder.get_object("btnSave")
        self.btnHideShowCoils = self.builder.get_object("btnHideShowCoils")
        self.lblHideShowCoils = self.builder.get_object("lblHideShowCoils")

        self.txtMaxLimit.connect("key-press-event", self.on_key_press_event)
        self.txtMinLimit.connect("key-press-event", self.on_key_press_event)


        self.boxPlot = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)

        self.fig = Figure(figsize=(10, 10), dpi=80)
        self.fig.patch.set_facecolor((242 / 255, 241 / 255, 240 / 255))
        self.canvas = FigureCanvas(self.fig)
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        
        self.boxPlot.pack_start(self.canvas, True, True, 0)
        self.boxPlot.pack_start(self.toolbar, False, True, 0)

        self.btnRestore.connect("clicked", self.on_initial_plot)
        self.btnApplyLimits.connect("clicked", self.on_apply_limits)
        self.btnSave.connect("clicked", self.on_save)
        self.btnHideShowCoils.connect("clicked", self.on_hide_show_coils)

        self.z_lims = (self.simulation.z_min, self.simulation.z_max)
        self.y_lims = (self.simulation.y_min, self.simulation.y_max)
        
        if z_lims:
            self.z_lims = z_lims
        if y_lims:
            self.y_lims = y_lims

        self.initial_norm = self.simulation.norm.copy()

        self.binary_colors = binary_colors
        self.selected_point = [[], []]
        self.rect = None
        
        self.plot_coils = False

        self.on_initial_plot(None)

    def on_key_press_event(self, widget, event):

        print("Key press on widget: ", widget)
        print("          Modifiers: ", event.state)
        print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))

        # check the event modifiers (can also use SHIFTMASK, etc)
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)

        # see if we recognise a keypress
        if Gdk.keyval_name(event.keyval) == 'Return':
            print("Enter")
            self.on_apply_limits(None)


    def on_save(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self.parent.window,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        filters = Gtk.FileFilter()
        filters.set_name("Images files")
        filters.add_pattern("*.png")
        filters.add_pattern("*.pdf")
        dialog.add_filter(filters)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            print("Open clicked")
            print("File selected: " + filename)
            if "." not in filename:
                filename += ".pdf"

            self.fig.savefig(filename)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def compute_zoom(self, zoom):
        z = self.simulation.z_max - self.simulation.z_min
        y = self.simulation.y_max - self.simulation.y_min
        mid_z = 0.5 * (self.simulation.z_max + self.simulation.z_min)
        mid_y = 0.5 * (self.simulation.y_max + self.simulation.y_min)

        new_z = z * 100 / zoom
        new_y = y * 100 / zoom

        zmin = mid_z - (0.5 * new_z)
        zmax = mid_z + (0.5 * new_z)

        ymin = mid_y - (0.5 * new_y)
        ymax = mid_y + (0.5 * new_y)

        left = numpy.where(self.simulation.z_grid[:, 0] >= (zmin - numpy.finfo(numpy.float32).eps))[0][0]
        right = numpy.where(self.simulation.z_grid[:, 0] <= (zmax + numpy.finfo(numpy.float32).eps))[0][-1]
        down = numpy.where(self.simulation.y_grid[0, :] >= (ymin - numpy.finfo(numpy.float32).eps))[0][0]
        up = numpy.where(self.simulation.y_grid[0, :] <= (ymax + numpy.finfo(numpy.float32).eps))[0][-1]

        self.z_grid = self.simulation.z_grid[left:(right + 1), down:(up + 1)]
        self.y_grid = self.simulation.y_grid[left:(right + 1), down:(up + 1)]
        self.norm = self.initial_norm[left:(right + 1), down:(up + 1)]

        self.z_lims = (zmin, zmax)
        self.y_lims = (ymin, ymax)

        self.compute_color_limits()
        return zmin, zmax, ymin, ymax

    def on_initial_plot(self, widget):

        self.z_grid = self.simulation.z_grid.copy()
        self.y_grid = self.simulation.y_grid.copy()
        self.norm = self.initial_norm.copy()

        self.z_lims = (self.simulation.z_min, self.simulation.z_max)
        self.y_lims = (self.simulation.y_min, self.simulation.y_max)


        print(self.parent, hasattr(self.parent, "on_apply_zoom"))
        if hasattr(self.parent, "on_apply_zoom"):
            self.parent.parent.plot.clear_rectangle()

            self.parent.zoom = 100.0
            self.parent.txtZoomValue.set_text("100.0")

        self.rect = None
        self.statBar.push(1, (""))
        self.compute_color_limits()
        self.points.set_data([], [])
        self.selected_point = [[], []]
        self.fig.canvas.draw()

    def compute_color_limits(self):
        if self.binary_colors:
            vmin = 0
        else:
            vmin = self.simulation.norm_center * 0.9

        
        if self.binary_colors:
            vmax = 1
        else:
            vmax = self.simulation.norm_center * 1.1
        
        self.min_val = vmin
        self.max_val = vmax

        self.txtMinLimit.set_property("text", self.format % self.min_val)
        self.txtMaxLimit.set_property("text", self.format % self.max_val)
        
        self.on_apply_limits(None)


    def on_click(self, event):
        if event.button != 1:
            return

        if (event.xdata is None):
            return

        x, y = event.xdata, event.ydata
        self.draw_point((x, y))


    def draw_point(self, point):
        z, y = point
        self.points.set_data([], [])
        self.selected_point = [[z], [y]]
        self.points.set_data(*self.selected_point)
        self.fig.canvas.draw()
        val = compute_norm(self.simulation.coils, abs(y), z, self.simulation.mu0)
        print(val)
        self.statBar.push(1, ("Coordinates: z = {:.3f}; y = {:.3f}; B = {:.2E} mT".format(
            z, y, val)))

    def isNumeric(self, val, func=float):
        try:
            func(self.format % eval(val))
            return True
        except Exception as e:
            return False

    def on_apply_limits(self, widget):
        if not self.isNumeric(self.txtMaxLimit.get_property("text")):
            ErrorMessage(self.parent.window, "Invalid input parameters", "Colorbar limits must be real numbers.")
            return

        if not self.isNumeric(self.txtMinLimit.get_property("text")):
            ErrorMessage(self.parent.window, "Invalid input parameters", "Colorbar limits must be real numbers.")
            return
        
        self.max_val = float(self.format % eval(self.txtMaxLimit.get_property("text")))
        self.min_val = float(self.format % eval(self.txtMinLimit.get_property("text")))


            

        
        if self.max_val > self.min_val:
            self.txtMaxLimit.set_property("text", self.format % self.max_val)
            self.txtMinLimit.set_property("text", self.format % self.min_val)
            # surpass is for set the >= symbol in case of norm >= max_val
            self.surpass = False
            if numpy.any(self.norm >= self.max_val):
                self.surpass = True

            # underpass is for set the <= symbol in case of norm <= max_val
            self.underpass = False
            if numpy.any(self.norm <= self.min_val):
                self.underpass = True

            self.update_plot()
        else:
            ErrorMessage(self.parent.window, "Invalid input parameters", "Min. value must be lower than Max. value")
        

    def update_plot(self, colormap=None):
        if colormap:
            self.colormap = colormap

        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        
        self.points, = self.ax.plot(*self.selected_point, "x", c="black", ms=10)

        self.ax.grid(True)
        cmap = pyplot.get_cmap(self.colormap)
        mesh = self.ax.pcolormesh(self.z_grid, self.y_grid, self.norm,
            shading="gouraud", cmap=cmap, vmin=self.min_val, vmax=self.max_val, zorder=-1)

        if self.plot_coils:
            for coil in self.simulation.coils:
                self.draw_coil(coil)

        if not self.binary_colors:
            cbar = self.fig.colorbar(mesh, format=self.format)
            cbar.set_label("B [mT]", fontsize=30)

            # set the ticks and ticks labels for the color bar
            labels = numpy.linspace(self.min_val, self.max_val, 5)
            cbar.set_ticks(labels)
            labels = ['%.2e' % s for s in labels]


            # in case of surpass is true, the last label is modified
            if self.surpass:
                labels[-1] = "≥" + labels[-1]

            # in case of underpass is true, the first label is modified
            if self.underpass:
                labels[0] = "≤" + labels[0]

            cbar.ax.set_yticklabels(labels)

        self.ax.set_xlabel("z [m]", fontsize=30)
        self.ax.set_ylabel("y [m]", fontsize=30)
        
        self.ax.set_xlim(self.z_lims)
        self.ax.set_ylim(self.y_lims)

        self.ax.set_aspect("equal")

        self.fig.tight_layout()
        self.fig.canvas.draw()


    def on_hide_show_coils(self, widget):
        self.plot_coils = not self.plot_coils

        if not self.plot_coils:
            self.lblHideShowCoils.set_text("Show coils")
        else:
            self.lblHideShowCoils.set_text("Hide coils")

        self.update_plot()



    def draw_coil(self, coil):
        gauge, diameter, section, resist, Inominal = numpy.loadtxt("awg.dat", unpack=True)
        Imax = abs(coil.I)
        index = numpy.argmin(Inominal > Imax) - 1
        diameter = diameter[index] / 1000

        width = numpy.sqrt(coil.num_turns) * diameter

        rect = patches.Rectangle(
            (coil.pos_z - width * 0.5, - coil.radius - width / 2),
            width, 2 * coil.radius + width,
            linewidth=0, facecolor="darkorange", edgecolor="black", hatch=r"|||||", )
        self.ax.add_patch(rect)


    def update_cursor_position(self, event):
        if event.button != 1:
            return

        if (event.xdata is None):
            return

        if self.pan_active or zoom_active:
            return


    def draw_rectangle(self, xmin, xmax, ymin, ymax):
        if self.rect:
            self.rect.remove()
        
        self.rect = patches.Rectangle((xmin, ymin), (xmax - xmin), (ymax - ymin), 
            linewidth=2, edgecolor='black', facecolor='none', zorder=100)
        self.ax.add_patch(self.rect)
        self.fig.canvas.draw()


    def clear_rectangle(self):
        if self.rect:
            self.rect.remove()
            self.rect = None
            self.fig.canvas.draw()
