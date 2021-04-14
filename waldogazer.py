import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf
import gridimage


class WaldoGazer(Gtk.Window):

	gridImage = None
	numRows=4
	numColumns=4
	pixbuf=None
	img=None

	def __init__(self, pixbuf, img):
		Gtk.Window.__init__(self)

		self.set_default_size(1000,800)

		paned = Gtk.Paned.new(orientation=Gtk.Orientation.VERTICAL)
		self.add(paned)
		file_chooser_button = Gtk.FileChooserButton()
		file_chooser_button.connect("file-set", self.on_file_selected)

		#build image placeholder
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file("image.jpg")
		self.img = Gtk.Image.new_from_pixbuf(self.scale_image(self.pixbuf, 700, 700))

		self.gridImage = gridimage.GridImage(self.pixbuf,
		                                     self.numRows,
		                                     self.numColumns);

		hbox = Gtk.HBox.new(Gtk.Orientation.HORIZONTAL, 10)
		button = Gtk.Button.new_with_label("Next portion")

		button.connect("clicked", self.on_next_clicked)

		#Add to paned
		hbox.add(file_chooser_button)
		hbox.add(button)
		paned.add1(hbox)
		paned.add2(self.img)

		self.connect("destroy", Gtk.main_quit)
		paned.connect("size-allocate", self.paned_allocated)

	def on_file_selected(self, button):
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(button.get_filename())
		self.gridImage = gridimage.GridImage(self.pixbuf,
		                                     self.numRows,
		                                     self.numColumns)
		self.img.set_from_pixbuf(self.scale_image(self.pixbuf, 700, 700))

	def scale_image(self, pixbuf, width, height):
		return self.pixbuf.scale_simple(width,height,GdkPixbuf.InterpType.BILINEAR)

	def paned_allocated(self, widget, allocation):
		width = widget.get_child2().get_allocated_width()
		height = widget.get_child2().get_allocated_height()
		self.pixbuf = self.scale_image(self.pixbuf, width, height)

	def on_next_clicked(self, widget):
		self.img.set_from_pixbuf(self.gridImage.getNext())
