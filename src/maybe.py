import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file("./interfaces/input.glade")

treeCoils = builder.get_object("treeCoils")
btnDeleteAll = builder.get_object("btnDeleteAll")
btnDeleteCoil = builder.get_object("btnDeleteCoil")
btnAddCoil = builder.get_object("btnAddCoil")
btnHelmholtzConfig = builder.get_object("btnHelmholtzConfig")


treeCoils.set_property("enable-grid-lines", Gtk.TreeViewGridLines(3))

def add_coil(_):
    model = treeCoils.get_model()
    model.append(["", 0.0, 0, 0.0, 0.0])

btnAddCoil.connect("clicked", add_coil)

def delete_row(_):
    tree_selection = treeCoils.get_selection()
    (model, pathlist) = tree_selection.get_selected_rows()
    for path in pathlist :
        tree_iter = model.get_iter(path)
        model.remove(tree_iter)

btnDeleteCoil.connect("clicked", delete_row)


def delete_all(button):
    treeCoils.get_model().clear()

btnDeleteAll.connect("clicked", delete_all)


def helmholtz_config(_):
    model = treeCoils.get_model()
    model.clear()
    model.append(["Circular", 0.5, 100, 1.0, -0.25])
    model.append(["Circular", 0.5, 100, 1.0, 0.25])



btnHelmholtzConfig.connect("activate", helmholtz_config)


# treeCoils.connect("key-release-event", delete_row)


shapesList = Gtk.ListStore(str)
for item in ["Circular", "Squared", "Triangular"]:
    shapesList.append([item])

coilsList = Gtk.ListStore(str, float, int, float, float)
coilsList.append(["Circular", 0.5, 100, 1.0, -0.25])
coilsList.append(["Circular", 0.5, 100, 1.0, 0.25])

treeCoils.set_model(coilsList)

def on_shape_changed(widget, path, text):
    coilsList[path][0] = text

shapeComboCell = Gtk.CellRendererCombo()
shapeComboCell.set_property("editable", True)
shapeComboCell.set_property("model", shapesList)
shapeComboCell.set_property("text-column", 0)
shapeComboCell.set_property("has-entry", False)
shapeComboCell.connect("edited", on_shape_changed)
shapeColumn = Gtk.TreeViewColumn("Shape", shapeComboCell, text=0)
shapeColumn.set_expand(True)
treeCoils.append_column(shapeColumn)


def radius_edited(widget, path, text):
    text = text.replace(",", ".")
    coilsList[path][1] = float(text)

radiusEntryCell = Gtk.CellRendererText()
radiusEntryCell.set_property("editable", True)
radiusColumn = Gtk.TreeViewColumn("Radius [m]", radiusEntryCell, text=1)
radiusColumn.set_expand(True)
treeCoils.append_column(radiusColumn)
radiusEntryCell.connect("edited", radius_edited)


def turns_edited(widget, path, text):
    coilsList[path][2] = int(text)

turnsEntryCell = Gtk.CellRendererText()
turnsEntryCell.set_property("editable", True)
turnsColumn = Gtk.TreeViewColumn("Turns", turnsEntryCell, text=2)
turnsColumn.set_expand(True)
treeCoils.append_column(turnsColumn)
turnsEntryCell.connect("edited", turns_edited)


def current_edited(widget, path, text):
    text = text.replace(",", ".")
    coilsList[path][3] = float(text)

currentEntryCell = Gtk.CellRendererText()
currentEntryCell.set_property("editable", True)
currentColumn = Gtk.TreeViewColumn("Current [A]", currentEntryCell, text=3)
currentColumn.set_expand(True)
treeCoils.append_column(currentColumn)
currentEntryCell.connect("edited", current_edited)


def position_edited(widget, path, text):
    text = text.replace(",", ".")
    coilsList[path][4] = float(text)

positionEntryCell = Gtk.CellRendererText()
positionEntryCell.set_property("editable", True)
positionColumn = Gtk.TreeViewColumn("Position [m]", positionEntryCell, text=4)
positionColumn.set_expand(True)
treeCoils.append_column(positionColumn)
positionEntryCell.connect("edited", position_edited)





window = builder.get_object("wndInput")
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()

