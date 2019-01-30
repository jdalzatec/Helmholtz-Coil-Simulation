import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class GridWindow():
    def __init__(self, parent, glade_file, initial_grid):
        self.initial_grid = initial_grid

        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)

        self.window = self.builder.get_object("wndGrid")
        self.window.set_transient_for(parent)

        self.txtMinZ = self.builder.get_object("txtMinZ")
        self.txtMaxZ = self.builder.get_object("txtMaxZ")
        self.txtPointsZ = self.builder.get_object("txtPointsZ")
        self.txtMinY = self.builder.get_object("txtMinY")
        self.txtMaxY = self.builder.get_object("txtMaxY")
        self.txtPointsY = self.builder.get_object("txtPointsY")
        self.btnRevert = self.builder.get_object("btnRevert")

        self.txtMinZ.set_property("text", str(self.initial_grid["z_min"]))
        self.txtMaxZ.set_property("text", str(self.initial_grid["z_max"]))
        self.txtPointsZ.set_property("text", str(self.initial_grid["z_points"]))
        self.txtMinY.set_property("text", str(self.initial_grid["y_min"]))
        self.txtMaxY.set_property("text", str(self.initial_grid["y_max"]))
        self.txtPointsY.set_property("text", str(self.initial_grid["y_points"]))


        self.btnRevert.connect("clicked", self.on_revert)

        self.window.show_all()


    def on_revert(self, widget):
        self.txtMinZ.set_property("text", str(self.initial_grid["z_min"]))
        self.txtMaxZ.set_property("text", str(self.initial_grid["z_max"]))
        self.txtPointsZ.set_property("text", str(self.initial_grid["z_points"]))
        self.txtMinY.set_property("text", str(self.initial_grid["y_min"]))
        self.txtMaxY.set_property("text", str(self.initial_grid["y_max"]))
        self.txtPointsY.set_property("text", str(self.initial_grid["y_points"]))
