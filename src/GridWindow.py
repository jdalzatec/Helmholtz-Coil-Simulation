import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from NumericEntry import NumericEntry

class GridWindow(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Grid", parent)


        self.set_modal(True)
        self.set_default_size(150, 100)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        # FUCKING LEFT BOX
        boxLeft = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label()
        label.set_markup('<b>Z grid</b>')
        
        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl1 = Gtk.Label("Min. Z [m] =")
        lbl1.set_halign(Gtk.Align.END)
        self.txtMinZ = NumericEntry(float)
        self.txtMinZ.set_width_chars(10)
        row1.pack_start(lbl1, True, True, 0)
        row1.pack_start(self.txtMinZ, False, False, 0)

        row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl2 = Gtk.Label("Max. Z [m] =")
        lbl2.set_halign(Gtk.Align.END)
        self.txtMaxZ = NumericEntry(float)
        self.txtMaxZ.set_width_chars(10)
        row2.pack_start(lbl2, True, True, 0)
        row2.pack_start(self.txtMaxZ, False, False, 0)
        
        row3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl3 = Gtk.Label("Points =")
        lbl3.set_halign(Gtk.Align.END)
        self.txtPointsZ = NumericEntry(int, "positive")
        self.txtPointsZ.set_width_chars(10)
        row3.pack_start(lbl3, True, True, 0)
        row3.pack_start(self.txtPointsZ, False, False, 0)

        boxLeft.pack_start(label, True, True, 0)
        boxLeft.pack_start(row1, True, True, 0)
        boxLeft.pack_start(row2, True, True, 0)
        boxLeft.pack_start(row3, True, True, 0)




        # FUCKING RIGHT BOX
        boxRight = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label()
        label.set_markup('<b>ρ grid</b>')
        
        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl1 = Gtk.Label("Min. ρ [m] =")
        lbl1.set_halign(Gtk.Align.END)
        self.txtMinRho = NumericEntry(float, "positive")
        self.txtMinRho.set_width_chars(10)
        row1.pack_start(lbl1, True, True, 0)
        row1.pack_start(self.txtMinRho, False, False, 0)

        row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl2 = Gtk.Label("Max. ρ [m] =")
        lbl2.set_halign(Gtk.Align.END)
        self.txtMaxRho = NumericEntry(float, "positive")
        self.txtMaxRho.set_width_chars(10)
        row2.pack_start(lbl2, True, True, 0)
        row2.pack_start(self.txtMaxRho, False, False, 0)
        
        row3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl3 = Gtk.Label("Points =")
        lbl3.set_halign(Gtk.Align.END)
        self.txtPointsRho = NumericEntry(int, "positive")
        self.txtPointsRho.set_width_chars(10)
        row3.pack_start(lbl3, True, True, 0)
        row3.pack_start(self.txtPointsRho, False, False, 0)

        boxRight.pack_start(label, True, True, 0)
        boxRight.pack_start(row1, True, True, 0)
        boxRight.pack_start(row2, True, True, 0)
        boxRight.pack_start(row3, True, True, 0)

        box.pack_start(boxLeft, True, True, 0)
        box.pack_start(boxRight, True, True, 0)

        content = self.get_content_area()
        content.pack_start(box, False, False, 10)

        self.add_button("Revert", Gtk.ResponseType.HELP)
        self.add_button("Run", Gtk.ResponseType.OK)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)


        self.show_all()

window = GridWindow(None)
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()