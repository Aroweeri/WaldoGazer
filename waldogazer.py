import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf
import gridimage
import scaleimage


class WaldoGazer(Gtk.Window):

	gridImage = None
	numRows=3
	numCols=3
	pixbuf=None
	pixbufToDisplay=None
	img=None

	def __init__(self, pixbuf, img):
		Gtk.Window.__init__(self)

		self.set_default_size(1000,800)
		self.set_title("WaldoGazer")

		paned = Gtk.Paned.new(orientation=Gtk.Orientation.VERTICAL)

		file_chooser_button = Gtk.FileChooserButton()
		file_chooser_button.connect("file-set", self.on_file_selected)

		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file("image.jpg")
		self.img = scaleimage.ScaleImage(self.pixbuf)
		self.reload()

		rowsScale = Gtk.Scale.new_with_range(Gtk.Orientation.VERTICAL, 1, 100, 1);
		colsScale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 100, 1);
		rowsScale.connect("value-changed", self.on_rows_changed); 
		colsScale.connect("value-changed", self.on_cols_changed); 
		rowsScale.set_value(self.numRows)
		colsScale.set_value(self.numCols)

		hbox = Gtk.HBox.new(Gtk.Orientation.HORIZONTAL, 10)
		nextButton = Gtk.Button.new_with_label("Next")
		nextButton.connect("clicked", self.on_next_clicked)
		prevButton = Gtk.Button.new_with_label("Previous")
		prevButton.connect("clicked", self.on_prev_clicked)

		hbox.add(file_chooser_button)
		hbox.add(nextButton)
		hbox.add(prevButton)
		hbox.add(rowsScale);
		hbox.add(colsScale);
		paned.pack1(hbox, True, True)
		paned.pack2(self.img, True, True)

		self.connect("destroy", Gtk.main_quit)

		self.add(paned)

	def on_file_selected(self, button):
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(button.get_filename())
		self.reload()

	def on_next_clicked(self, widget):
		self.pixbufToDisplay = self.gridImage.getNext()
		self.img.change_image(self.pixbufToDisplay)

	def on_prev_clicked(self, widget):
		self.pixbufToDisplay = self.gridImage.getPrev()
		self.img.change_image(self.pixbufToDisplay)

	def on_rows_changed(self, scale):
		self.numRows = int(scale.get_value())
		self.reload()

	def on_cols_changed(self, scale):
		self.numCols = int(scale.get_value())
		self.reload()

	def reload(self):
		self.pixbufToDisplay = self.pixbuf
		self.gridImage = gridimage.GridImage(self.pixbuf, self.numRows, self.numCols)
		self.img.change_image(self.pixbufToDisplay)
