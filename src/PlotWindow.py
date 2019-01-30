import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
# from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

import numpy


class PlotBox():
    def __init__(self, parent, simulation, colormap, statBar, z_lims=None, y_lims=None, txtZoomValue=None):
        self.parent = parent
        self.simulation = simulation
        self.colormap = colormap
        self.format = '%.2e'
        self.statBar = statBar

        self.builder = Gtk.Builder()
        self.builder.add_from_file("./interfaces/toolbar.glade")
        wnd = self.builder.get_object("wndToolBar")
        self.toolbar = self.builder.get_object("boxToolBar")
        wnd.remove(self.toolbar)
        self.btnApplyLimits = self.builder.get_object("btnApplyLimits")
        self.txtMinLimit = self.builder.get_object("txtMinLimit")
        self.txtMaxLimit = self.builder.get_object("txtMaxLimit")
        self.btnRestore = self.builder.get_object("btnRestore")
        self.btnSave = self.builder.get_object("btnSave")

        self.boxPlot = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.fig = Figure(figsize=(10, 10), dpi=80)
        self.canvas = FigureCanvas(self.fig)
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        
        self.boxPlot.pack_start(self.canvas, True, True, 0)
        self.boxPlot.pack_start(self.toolbar, False, True, 0)

        self.btnRestore.connect("clicked", self.on_initial_plot)
        self.btnApplyLimits.connect("clicked", self.on_apply_limits)
        self.btnSave.connect("clicked", self.on_save)

        self.z_lims = (self.simulation.z_min, self.simulation.z_max)
        self.y_lims = (self.simulation.y_min, self.simulation.y_max)
        
        if z_lims:
            self.z_lims = z_lims
        if y_lims:
            self.y_lims = y_lims

        self.txtZoomValue = txtZoomValue
        self.initial_norm = self.simulation.norm.copy()
        
        self.on_initial_plot(None)

    def on_save(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self.parent,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        filters = Gtk.FileFilter()
        filters.set_name("Images files")
        filters.add_pattern("*.png")
        filters.add_pattern("*.jpg")
        filters.add_pattern("*.pdf")
        dialog.add_filter(filters)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            print("Open clicked")
            print("File selected: " + filename)

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

    def on_initial_plot(self, widget):
        self.z_grid = self.simulation.z_grid.copy()
        self.y_grid = self.simulation.y_grid.copy()
        self.norm = self.initial_norm.copy()

        self.z_lims = (self.simulation.z_min, self.simulation.z_max)
        self.y_lims = (self.simulation.y_min, self.simulation.y_max)

        if self.txtZoomValue:
            self.txtZoomValue.set_text("100.0")

        self.compute_color_limits()

    def compute_color_limits(self):
        vmax = numpy.max(self.norm)
        vmin = numpy.min(self.norm)
        if vmax > 3 * vmin and vmin != 0.0:
            self.min_val = vmin
            self.max_val = vmin * 3
        else:
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
        print(x, y)
        self.points.set_data([x], [y])
        self.fig.canvas.draw()
        self.statBar.push(1, ("Coordinates: x = " + str(round(x, 3)) + "; y = " + str(round(y, 3))))

    def on_apply_limits(self, widget):
        self.txtMaxLimit.set_property("text", self.format % eval(self.txtMaxLimit.get_property("text")))
        self.txtMinLimit.set_property("text", self.format % eval(self.txtMinLimit.get_property("text")))

        self.max_val = float(self.txtMaxLimit.get_property("text"))
        self.min_val = float(self.txtMinLimit.get_property("text"))
        print(self.max_val, self.min_val)
        if self.max_val >= self.min_val:
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
            print("cómo chuchas")
        print(self.underpass, self.surpass)
        

    def update_plot(self, colormap=None):
        if colormap:
            self.colormap = colormap

        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        
        self.points, = self.ax.plot([], [], "x", c="black", ms=10)

        self.ax.grid(True)
        cmap = pyplot.get_cmap(self.colormap)
        mesh = self.ax.pcolormesh(self.z_grid, self.y_grid, self.norm,
            shading="gouraud", cmap=cmap, vmin=self.min_val, vmax=self.max_val)

        for coil in self.simulation.coils:
            self.ax.plot([coil.pos_z, coil.pos_z], [-coil.radius, coil.radius],
                lw=coil.num_turns / 10, color=coil.color)

        cbar = self.fig.colorbar(mesh, format=self.format)

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

    def update_cursor_position(self, event):
        if event.button != 1:
            return

        if (event.xdata is None):
            return

        if self.pan_active or zoom_active:
            return