import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


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

        self.txtMinZ.connect("key-press-event", self.on_key_press_event)
        self.txtMaxZ.connect("key-press-event", self.on_key_press_event)
        self.txtPointsZ.connect("key-press-event", self.on_key_press_event)
        self.txtMinY.connect("key-press-event", self.on_key_press_event)
        self.txtMaxY.connect("key-press-event", self.on_key_press_event)
        self.txtPointsY.connect("key-press-event", self.on_key_press_event)

        self.window.show_all()

    def on_key_press_event(self, widget, event):

        # print("Key press on widget: ", widget)
        # print("          Modifiers: ", event.state)
        # print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))

        # check the event modifiers (can also use SHIFTMASK, etc)
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)

        # see if we recognise a keypress
        if Gdk.keyval_name(event.keyval) == 'Return':
            print("Enter")
            self.window.response(Gtk.ResponseType.OK)



    def on_revert(self, widget):
        self.txtMinZ.set_property("text", str(self.initial_grid["z_min"]))
        self.txtMaxZ.set_property("text", str(self.initial_grid["z_max"]))
        self.txtPointsZ.set_property("text", str(self.initial_grid["z_points"]))
        self.txtMinY.set_property("text", str(self.initial_grid["y_min"]))
        self.txtMaxY.set_property("text", str(self.initial_grid["y_max"]))
        self.txtPointsY.set_property("text", str(self.initial_grid["y_points"]))
