import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class CoilListRow(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)

        self.btnRemove = Gtk.Button.new_from_icon_name("list-remove", Gtk.IconSize(2))
        self.btnRemove.set_size_request(80, 10)

        self.btnRemove.set_can_focus(False)


        self.txtRadius = Gtk.Entry()
        self.txtTurns = Gtk.Entry()
        self.txtCurrent = Gtk.Entry()
        self.txtPosition = Gtk.Entry()
        
        self.txtRadius.set_property("width-chars", 5)
        self.txtTurns.set_property("width-chars", 5)
        self.txtCurrent.set_property("width-chars", 5)
        self.txtPosition.set_property("width-chars", 5)
        
        self.txtRadius.set_property("placeholder-text", "R = ")
        self.txtTurns.set_property("placeholder-text", "N = ")
        self.txtCurrent.set_property("placeholder-text", "I = ")
        self.txtPosition.set_property("placeholder-text", "Z = ")

        self.txtRadius.set_property("input-purpose", Gtk.InputPurpose.NUMBER)

        self.txtRadius.connect("key-press-event", self.on_key_press_event)
        self.txtTurns.connect("key-press-event", self.on_key_press_event)
        self.txtCurrent.connect("key-press-event", self.on_key_press_event)
        self.txtPosition.connect("key-press-event", self.on_key_press_event)

        self.pack_start(self.btnRemove, False, False, 0)
        self.pack_start(self.txtRadius, True, True, 0)
        self.pack_start(self.txtTurns, True, True, 0)
        self.pack_start(self.txtCurrent, True, True, 0)
        self.pack_start(self.txtPosition, True, True, 0)

        self.btnRemove.connect("clicked", self.remove_from_parent)


    def on_key_press_event(self, widget, event):


        # check the event modifiers (can also use SHIFTMASK, etc)
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)

        # see if we recognise a keypress
        if Gdk.keyval_name(event.keyval) == 'Return':
            self.get_parent().get_parent().btnSimulate.emit("clicked")


    def remove_from_parent(self, widget):
        self.get_parent().get_parent().remove(self.get_parent())
    
    
    def set_values(self, radius, turns, current, position):
        self.txtRadius.set_property("text", str(radius))
        self.txtTurns.set_property("text", str(turns))
        self.txtCurrent.set_property("text", str(current))
        self.txtPosition.set_property("text", str(position))

    def isNumeric(self, val, func=float):
        try:
            func(val)
            return True
        except Exception as e:
            return False

    def get_values(self):
        params = {
            "shape": "Circular",
            "radius": float(self.txtRadius.get_text()) if self.isNumeric(self.txtRadius.get_text()) else False,
            "turns": int(self.txtTurns.get_text()) if self.isNumeric(self.txtTurns.get_text(), int) else False,
            "current": float(self.txtCurrent.get_text()) if self.isNumeric(self.txtCurrent.get_text()) else False,
            "position": float(self.txtPosition.get_text()) if self.isNumeric(self.txtPosition.get_text()) else False
        }
        return params

    def validate_values(self):
        radius = self.txtRadius.get_text()

        if radius == "":
            raise Exception("paila")
            return False

        radius = float(radius)

        if radius <= 0:
            raise Exception("paila")
            return False

        turns = self.txtTurns.get_text()

        if turns == "":
            raise Exception("paila")
            return False

        turns = int(turns)

        if turns <= 0:
            raise Exception("paila")
            return False

        current = self.txtCurrent.get_text()

        if current == "":
            raise Exception("paila")
            return False

        current = float(current)

        position = self.txtPosition.get_text()

        if position == "":
            raise Exception("paila")
            return False

        position = float(position)

        return True
