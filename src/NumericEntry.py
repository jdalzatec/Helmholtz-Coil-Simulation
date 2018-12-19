import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class NumericEntry(Gtk.Entry):
    def __init__(self, kind=float, sign="both"):
        Gtk.Entry.__init__(self)

        if kind == float:
            self.chars = "0123456789.,"
        elif kind == int:
            self.chars = "0123456789"
        else:
            print("pailander")

        if sign == "both":
            self.chars += "-+"
        elif sign == "positive":
            self.chars += "+"
        elif sign == "negative":
            self.chars += "-"
        else:
            print("pailander")

    def do_insert_text(self, new_text, new_text_length, position):
        text = ""
        for c in new_text:
            if c in self.chars:
                if c not in ".,":
                    text += c
                else:
                    if "." not in self.get_text() and "," not in self.get_text():
                        text += c

        self.get_buffer().insert_text(position, text, len(text))
        return position + len(text)
