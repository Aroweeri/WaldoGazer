import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf

class WaldoGazer(Gtk.Window):
	def __init__(self, pixbuf, img):
		Gtk.Window.__init__(self, title="WaldoGazer")

		box = Gtk.Box()
		label = Gtk.Label.new("Hello")

		#build image
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file("image.jpg")
		
		self.img = Gtk.Image.new_from_pixbuf(self.pixbuf)

		#Add to box
		box.pack_start(label, True, True, 0)
		box.pack_start(self.img, True, True, 0)

		self.add(box)

	def scale_image(self, widget, allocation):
		self.pixbuf = self.pixbuf.scale_simple(200,200,GdkPixbuf.InterpType.BILINEAR)
		self.img.set_from_pixbuf(self.pixbuf)
