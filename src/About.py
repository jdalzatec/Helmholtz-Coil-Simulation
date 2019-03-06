import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class AboutWindow():
    def __init__(self, parent):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interfaces/about.glade")

        self.window = self.builder.get_object("wndAbout")
        self.btnClose = self.builder.get_object("btnClose")
        self.window.set_transient_for(parent)

        self.btnClose.connect("clicked", lambda _: self.window.close())
        self.window.show_all()