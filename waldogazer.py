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
	pixbufToDisplay=None
	scaledPixbuf=None
	img=None
	scrolledWindow=None

	def __init__(self, pixbuf, img):
		Gtk.Window.__init__(self)

		self.set_default_size(1000,800)
		scrolledWindow = Gtk.ScrolledWindow()

		paned = Gtk.Paned.new(orientation=Gtk.Orientation.VERTICAL)
		file_chooser_button = Gtk.FileChooserButton()
		file_chooser_button.connect("file-set", self.on_file_selected)

		#build image placeholder
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file("image.jpg")
		self.pixbufToDisplay = self.pixbuf
		self.img = Gtk.Image.new_from_pixbuf(self.pixbuf)

		self.gridImage = gridimage.GridImage(self.pixbuf,
		                                     self.numRows,
		                                     self.numColumns);

		hbox = Gtk.HBox.new(Gtk.Orientation.HORIZONTAL, 10)
		nextButton = Gtk.Button.new_with_label("Next")
		nextButton.connect("clicked", self.on_next_clicked)
		prevButton = Gtk.Button.new_with_label("Previous")
		prevButton.connect("clicked", self.on_prev_clicked)

		scrolledWindow.add(self.img)
		hbox.add(file_chooser_button)
		hbox.add(nextButton)
		hbox.add(prevButton)
		paned.pack1(hbox, True, True)
		paned.pack2(scrolledWindow, True, True)

		self.connect("destroy", Gtk.main_quit)
		scrolledWindow.connect("size-allocate", self.on_size_allocated)

		self.add(paned)

	def on_file_selected(self, button):
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(button.get_filename())
		self.pixbufToDisplay = self.pixbuf
		self.gridImage = gridimage.GridImage(self.pixbuf,
		                                     self.numRows,
		                                     self.numColumns)
		self.img.set_from_pixbuf(self.pixbufToDisplay)

	def scale_image(self, pixbuf, width, height):
		return pixbuf.scale_simple(width,height,GdkPixbuf.InterpType.BILINEAR)

	def on_size_allocated(self, widget, allocation):
		imgWidth = self.pixbufToDisplay.get_width()
		imgHeight = self.pixbufToDisplay.get_height()

		parentWidth = allocation.width
		parentHeight = allocation.height

		aspectWidth = parentWidth/imgWidth
		aspectHeight= parentHeight/imgHeight

		aspect=0

		if(aspectWidth < aspectHeight):
			aspect = aspectWidth
		else:
			aspect = aspectHeight

		newWidth = imgWidth*aspect
		newHeight = imgHeight*aspect

		self.scaledPixbuf = self.scale_image(self.pixbufToDisplay, newWidth, newHeight)

		self.img.set_from_pixbuf(self.scaledPixbuf)

	def on_next_clicked(self, widget):
		self.pixbufToDisplay = self.gridImage.getNext()
		self.img.set_from_pixbuf(self.pixbufToDisplay)

	def on_prev_clicked(self, widget):
		self.pixbufToDisplay = self.gridImage.getPrev()
		self.img.set_from_pixbuf(self.pixbufToDisplay)
