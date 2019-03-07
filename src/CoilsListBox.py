import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from CoilListRow import CoilListRow


class CoilsListBox(Gtk.ListBox):
    def __init__(self, btnSimulate):
        Gtk.ListBox.__init__(self)
        self.set_property("selection-mode", Gtk.SelectionMode(0))
        self.btnSimulate = btnSimulate

        self.btnAddInList = Gtk.Button.new_from_icon_name("list-add", Gtk.IconSize(2))
        self.btnAddInList.connect("clicked", self.create_coil_row)

        row = Gtk.Box()
        row.pack_start(self.btnAddInList, True, True, 0)
        self.add(row)


    def create_coil_row(self, widget):
        row = CoilListRow()
        self.insert(row, 0)
        self.show_all()
        row.txtRadius.grab_focus()

    def remove_all_coils(self, widget):
        for row in list(self)[:-1]:
            self.remove(row)

    def remove_coil(self, row):
        self.remove(row)

    def update(self, preset):
        for row in list(self)[:-1]:
            self.remove(row)

        for row in preset:
            self.insert(row, 0)

        self.show_all()