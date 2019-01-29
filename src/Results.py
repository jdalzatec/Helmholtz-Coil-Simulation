import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
# from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

import numpy


class Results():
    def __init__(self, parent):
        self.parent = parent
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./interfaces/results.glade")
        self.window = self.builder.get_object("wndResults")
        self.boxPlot = self.builder.get_object("boxPlot")
        self.btnBack = self.builder.get_object("btnBack")
        self.txtMinVal = self.builder.get_object("txtMinVal")
        self.txtMaxVal = self.builder.get_object("txtMaxVal")
        self.btnRevertLimits = self.builder.get_object("btnRevertLimits")
        self.btnApplyLimits = self.builder.get_object("btnApplyLimits")
        self.statBar = self.builder.get_object("statBar")
        self.menuColorMap = self.builder.get_object("menuColorMap")
        self.treeData = self.builder.get_object("treeData")
        self.treeGridInfo = self.builder.get_object("treeGridInfo")
        self.treeCoilsInfo = self.builder.get_object("treeCoilsInfo")

        self.copy_norm = self.parent.norm.copy()

        self.format = '%.2e'

        self.colormap = "jet"

        self.window.set_transient_for(self.parent.window)
        self.window.maximize()

        self.window.connect("destroy", self.quit)
        self.btnBack.connect("clicked", self.on_back)
        self.btnRevertLimits.connect("clicked", self.on_revert_limits)
        self.btnApplyLimits.connect("clicked", self.on_apply_limits)


        self.fig = Figure(figsize=(10, 10), dpi=80)
        self.canvas = FigureCanvas(self.fig)
        self.fig.canvas.mpl_connect("motion_notify_event", self.update_cursor_position)
        self.fig.canvas.mpl_connect("button_press_event", self.plot_point)
        
        self.boxPlot.pack_start(self.canvas, True, True, 0)
        self.toolbar = NavigationToolbar(self.canvas, self.window)
        self.boxPlot.pack_start(self.toolbar, False, True, 0)


        self.toolbar_buttons = {}
        for item in self.toolbar.get_children():
            if hasattr(item, "get_label"):
                self.toolbar_buttons[item.get_label()] = item
                print(item.get_label())

        self.toolbar_buttons["Home"].connect("clicked", self.on_home)
        self.toolbar_buttons["Pan"].connect("clicked", self.on_pan)
        self.toolbar_buttons["Zoom"].connect("clicked", self.on_zoom)


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


        # self.fig.canvas.flush_events()
        self.on_revert_limits(None)
        self.window.show_all()
        self.toolbar.remove(self.toolbar_buttons["Subplots"])

        self.pan_active = False
        self.zoom_active = False


        self.populate_input_params_trees()

    def on_home(self, widget):
        while self.zoom_active:
            self.toolbar_buttons["Zoom"].emit("clicked")

        while self.pan_active:
            self.toolbar_buttons["Pan"].emit("clicked")

    def on_pan(self, widget):
        if (not self.pan_active and not self.zoom_active):
            self.pan_active = True
        elif (self.pan_active and not self.zoom_active):
            self.pan_active = False
        elif (not self.pan_active and self.zoom_active):
            self.pan_active = True
            self.zoom_active = False

    
    def on_zoom(self, widget):
        if (not self.pan_active and not self.zoom_active):
            self.zoom_active = True
        elif (not self.pan_active and self.zoom_active):
            self.zoom_active = False
        elif (self.pan_active and not self.zoom_active):
            self.pan_active = False
            self.zoom_active = True

    def populate_input_params_trees(self):
        coilsList = Gtk.ListStore(str, float, int, float, float)
        for coil in self.parent.coils:
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


        lblMinZ.set_label(str(self.parent.z_min))
        lblMaxZ.set_label(str(self.parent.z_max))
        lblPointsZ.set_label(str(self.parent.z_points))
        lblMinRho.set_label(str(self.parent.rho_min))
        lblMaxRho.set_label(str(self.parent.rho_max))
        lblPointsRho.set_label(str(self.parent.rho_points))



                
    def on_color_bar_menu(self, widget, name, first=False):
        self.colormap = name
        self.plot()

    def plot_point(self, event):
        if event.button != 1:
            return

        if (event.xdata is None):
            return

        if self.pan_active or self.zoom_active:
            return

        x, y = event.xdata, event.ydata
        self.ax.scatter(x, y, s=10, c="black")
        self.statBar.push(1, ("Coordinates: x = " + str(round(x, 3)) + "; y = " + str(round(y, 3))))
        

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
        self.min_val = numpy.min(self.parent.norm)
        # self.max_val = numpy.max(self.parent.norm)
        self.max_val = self.min_val * 5
        
        self.txtMaxVal.set_property("text", self.format % self.max_val)
        self.txtMinVal.set_property("text", self.format % self.min_val)
        
        self.on_apply_limits(None)


    def on_apply_limits(self, widget):
        self.copy_norm = self.parent.norm.copy()

        self.txtMaxVal.set_property("text", self.format % eval(self.txtMaxVal.get_property("text")))
        self.txtMinVal.set_property("text", self.format % eval(self.txtMinVal.get_property("text")))

        self.max_val = float(self.txtMaxVal.get_property("text"))
        self.min_val = float(self.txtMinVal.get_property("text"))

        if self.max_val > self.min_val:
            # surpass is for set the >= symbol in case of norm >= max_val
            self.surpass = False
            if numpy.any(self.parent.norm >= self.max_val):
                self.surpass = True
                self.copy_norm[self.parent.norm >= self.max_val] = self.max_val

            # underpass is for set the <= symbol in case of norm <= max_val
            self.underpass = False
            if numpy.any(self.parent.norm <= self.min_val):
                self.underpass = True
                self.copy_norm[self.parent.norm <= self.min_val] = self.min_val

            self.plot()
        else:
            print("cómo chuchas")
        print(self.underpass, self.surpass)

    def plot(self):
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        self.ax.grid(True)
        cmap = pyplot.get_cmap(self.colormap)
        mesh = self.ax.pcolormesh(self.parent.z_grid, self.parent.rho_grid, self.copy_norm,
            shading="gouraud", cmap=cmap, vmin=self.min_val, vmax=self.max_val)
        mesh = self.ax.pcolormesh(self.parent.z_grid, -self.parent.rho_grid, self.copy_norm,
            shading="gouraud", cmap=cmap, vmin=self.min_val, vmax=self.max_val)

        for coil in self.parent.coils:
            self.ax.plot([coil.pos_z, coil.pos_z], [-coil.radius, coil.radius],
                lw=coil.num_turns / 10, color=coil.color)

        cbar = self.fig.colorbar(mesh, format=self.format)

        # set the ticks and ticks labels for the color bar
        labels = numpy.linspace(self.min_val, self.max_val, 5)
        cbar.set_ticks(labels)
        labels = ['%.2e' % s for s in labels]


        # in case of surpass is true, the last label is modified
        if self.surpass:
            labels[-1] = r"$\geq$ " + labels[-1]

        # in case of underpass is true, the first label is modified
        if self.underpass:
            labels[0] = r"$\leq$ " + labels[0]

        cbar.ax.set_yticklabels(labels)

        self.ax.set_xlabel(r"$z \ \rm [m]$", fontsize=30)
        self.ax.set_ylabel(r"$y \ \rm [m]$", fontsize=30)
        
        self.ax.set_xlim(self.parent.z_min, self.parent.z_max)
        self.ax.set_ylim(-self.parent.rho_max, self.parent.rho_max)

        # self.fig.tight_layout()
        self.fig.canvas.draw()



    def quit(self, widget):
        if not self.parent.parent.get_visible():
            Gtk.main_quit()
        else:
            self.window.close()


    def on_back(self, widget):
        self.parent.parent.show()
        self.window.close()