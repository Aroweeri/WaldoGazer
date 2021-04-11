import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import waldogazer

win = waldogazer.WaldoGazer(None, None)
win.show_all()

Gtk.main()
