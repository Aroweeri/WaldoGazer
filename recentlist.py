import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject
from gi.repository import GdkPixbuf
import scaleimage

class RecentList(Gtk.Box):

	__gsignals__ = {
		'recent_file_selected' : (GObject.SignalFlags.RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_STRING,))
	}

	def __init__(self, filename):
		Gtk.Box.__init__(self, Gtk.Orientation.HORIZONTAL)
		self.filename = filename
		self.update()

	def update(self):
		try:
			file = open(self.filename, "r")
		except FileNotFoundError:
			return
		self.pack_start(Gtk.Label.new("Recent: "), True, True, 0)
		for line in file:
			ev = Gtk.EventBox()
			pixbuf = GdkPixbuf.Pixbuf.new_from_file(line.strip())
			ev.connect("button_press_event", self.clicked)
			img = scaleimage.ScaleImage(pixbuf, line.strip())
			img.set_hexpand(True)
			ev.add(img)
			self.pack_start(ev, True, True, 0)
		file.close()

	def clicked(self, widget, event):
		pixbuf = widget.get_children()[0]
		self.emit("recent_file_selected", pixbuf.filename)
