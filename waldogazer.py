import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf

class WaldoGazer(Gtk.Window):
	def __init__(self, pixbuf, img):
		Gtk.Window.__init__(self);

		self.set_default_size(800,600)

		paned = Gtk.Paned.new(orientation=Gtk.Orientation.VERTICAL)
		self.add(paned)
		file_chooser_button = Gtk.FileChooserButton()
		file_chooser_button.connect("file-set", self.load_image)

		#build image placeholder
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file("image.jpg")
		self.pixbuf = self.pixbuf.scale_simple(200,200,GdkPixbuf.InterpType.BILINEAR)
		self.img = Gtk.Image.new_from_pixbuf(self.pixbuf)

		#Add to box
		paned.add1(file_chooser_button)
		paned.add2(self.img)

		self.connect("destroy", Gtk.main_quit)

	def load_image(self, button):
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(button.get_filename())
		self.pixbuf = self.pixbuf.scale_simple(200,200,GdkPixbuf.InterpType.BILINEAR)
		self.img.set_from_pixbuf(self.pixbuf)
