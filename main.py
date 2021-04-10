import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import waldogazer

win = waldogazer.WaldoGazer(None, None)
win.connect("destroy", Gtk.main_quit)
win.connect("size-allocate", win.scale_image)
win.show_all()
Gtk.main()
