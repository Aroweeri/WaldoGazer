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

		grid = Gtk.Grid.new()

		file_chooser_button = Gtk.FileChooserButton()
		file_chooser_button.connect("file-set", self.on_file_selected)

		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file("image.jpg")
		self.img = scaleimage.ScaleImage(self.pixbuf)
		self.img.set_vexpand(True)
		self.reload()

		rowsScale = Gtk.Scale.new_with_range(Gtk.Orientation.VERTICAL, 1, 100, 1);
		colsScale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 100, 1);
		rowsScale.connect("value-changed", self.on_rows_changed); 
		colsScale.connect("value-changed", self.on_cols_changed); 
		rowsScale.set_value(self.numRows)
		colsScale.set_value(self.numCols)

		nextButton = Gtk.Button.new_with_label("Next")
		nextButton.connect("clicked", self.on_next_clicked)
		prevButton = Gtk.Button.new_with_label("Previous")
		prevButton.connect("clicked", self.on_prev_clicked)

		file_chooser_button.set_hexpand(True)
		rowsScale.set_hexpand(True)
		colsScale.set_hexpand(True)
		nextButton.set_hexpand(True)
		prevButton.set_hexpand(True)

		grid.attach(file_chooser_button, 0, 0, 1, 1)
		grid.attach(nextButton, 1, 0, 1, 1)
		grid.attach(prevButton, 2, 0, 1, 1)
		grid.attach(rowsScale, 3, 0, 1, 1)
		grid.attach(colsScale, 4, 0, 1, 1)
		grid.attach(self.img, 0, 1, 5, 1)

		self.connect("destroy", Gtk.main_quit)

		self.add(grid)

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
