import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from NumericEntry import NumericEntry


class CoilListRow(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)
        self.possibleShapes = ("Circular", "Squared", "Triangular")

        self.shapeComboBox = Gtk.ComboBoxText()
        self.shapeComboBox.set_entry_text_column(0)
        self.shapeComboBox.set_size_request(120, 10)
        for s in self.possibleShapes:
            self.shapeComboBox.append_text(s)

        self.btnRemove = Gtk.Button.new_from_icon_name("list-remove", Gtk.IconSize(2))
        self.btnRemove.set_size_request(80, 10)

        self.btnRemove.set_can_focus(False)


        self.txtRadius = NumericEntry(float, "positive")
        self.txtTurns = NumericEntry(int, "positive")
        self.txtCurrent = NumericEntry(float, "both")
        self.txtPosition = NumericEntry(float, "both")
        
        self.txtRadius.set_property("width-chars", 5)
        self.txtTurns.set_property("width-chars", 5)
        self.txtCurrent.set_property("width-chars", 5)
        self.txtPosition.set_property("width-chars", 5)
        
        self.shapeComboBox.set_active(0)
        self.txtRadius.set_property("placeholder-text", "R = ")
        self.txtTurns.set_property("placeholder-text", "N = ")
        self.txtCurrent.set_property("placeholder-text", "I = ")
        self.txtPosition.set_property("placeholder-text", "Z = ")

        self.txtRadius.set_property("input-purpose", Gtk.InputPurpose.NUMBER)

        self.pack_start(self.btnRemove, False, False, 0)
        self.pack_start(self.shapeComboBox, False, False, 0)
        self.pack_start(self.txtRadius, True, True, 0)
        self.pack_start(self.txtTurns, True, True, 0)
        self.pack_start(self.txtCurrent, True, True, 0)
        self.pack_start(self.txtPosition, True, True, 0)

        self.btnRemove.connect("clicked", self.remove_from_parent)

    def remove_from_parent(self, widget):
        self.get_parent().get_parent().remove(self.get_parent())
    
    
    def set_values(self, shape, radius, turns, current, position):
        self.shapeComboBox.set_active(self.possibleShapes.index(shape))
        self.txtRadius.set_property("text", str(radius))
        self.txtTurns.set_property("text", str(turns))
        self.txtCurrent.set_property("text", str(current))
        self.txtPosition.set_property("text", str(position))

