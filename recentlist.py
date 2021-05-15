import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf
import scaleimage

class RecentList(Gtk.Box):

	filename=None
	
	def __init__(self, filename):
		Gtk.Box.__init__(self, Gtk.Orientation.HORIZONTAL)
		self.filename = filename
		self.update()

	def update(self):
		file = open(self.filename, "r")
		self.pack_start(Gtk.Label.new("Recent: "), True, True, 0)
		for line in file:
			pixbuf = GdkPixbuf.Pixbuf.new_from_file(line.strip())
			img = scaleimage.ScaleImage(pixbuf)
			img.set_hexpand(True)
			self.pack_start(img, True, True, 0)
		file.close()
