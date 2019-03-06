import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ErrorMessage():
    def __init__(self, parent, title, message):
        dialog = Gtk.MessageDialog(parent, 1, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.CANCEL, title)
        dialog.format_secondary_text(
            message)
        dialog.run()
        dialog.destroy()