import sys

is_frozen = getattr(sys, 'frozen', False)
frozen_temp_path = getattr(sys, '_MEIPASS', '')

import os

# This is needed to find resources when using pyinstaller
if is_frozen:
    basedir = frozen_temp_path
else:
    basedir = os.path.dirname(os.path.abspath(__file__))
resource_dir = os.path.join(basedir, 'resources')



import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class AboutWindow():
    def __init__(self, parent):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(resource_dir + "/about.glade")

        self.window = self.builder.get_object("wndAbout")
        self.btnClose = self.builder.get_object("btnClose")
        self.window.set_transient_for(parent)

        self.btnClose.connect("clicked", lambda _: self.window.close())
        self.window.show_all()