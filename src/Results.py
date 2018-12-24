import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

class Results():
    def __init__(self):
        
        self.window = Gtk.Window()

        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()