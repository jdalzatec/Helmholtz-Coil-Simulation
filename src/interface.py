import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


from CoilsListBox import CoilsListBox
from CoilListRow import CoilListRow
from Presets import HelmholtzCoilPreset

builder = Gtk.Builder()
builder.add_from_file("./interfaces/input2.glade")

btnDeleteAll = builder.get_object("btnDeleteAll")
btnAddCoil = builder.get_object("btnAddCoil")
btnHelmholtzConfig = builder.get_object("btnHelmholtzConfig")

scrListBox = builder.get_object("scrListBox")


listBox = CoilsListBox()
scrListBox.add_with_viewport(listBox)

btnAddCoil.connect("clicked", listBox.create_coil_row)
btnDeleteAll.connect("clicked", listBox.remove_all_coils)


def on_helmholtz_config(widget):
    listBox.update(HelmholtzCoilPreset())


btnHelmholtzConfig.connect("activate", on_helmholtz_config)



window = builder.get_object("wndInput")
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()

