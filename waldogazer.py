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

		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file("blank.png")
		self.img = scaleimage.ScaleImage(self.pixbuf)
		self.img.set_vexpand(True)
		self.reload()

		rowsScale = Gtk.Scale.new_with_range(Gtk.Orientation.VERTICAL, 1, 100, 1);
		colsScale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 100, 1);
		rowsScale.connect("value-changed", self.on_rows_changed); 
		colsScale.connect("value-changed", self.on_cols_changed); 
		rowsScale.set_value(self.numRows)
		colsScale.set_value(self.numCols)

		hbox = Gtk.HBox.new(Gtk.Orientation.HORIZONTAL, 3)
		hbox.pack_start(Gtk.Label.new("Recent:"), True, True, 0)

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
		grid.attach(hbox, 0, 1, 5, 1)
		grid.attach(self.img, 0, 2, 5, 1)

		self.connect("destroy", Gtk.main_quit)

		self.add(grid)

	def on_file_selected(self, button):
		filename = button.get_filename()
		self.append_recent_file(filename)
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
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

		if(self.pixbuf == None):
			return

		self.pixbufToDisplay = self.pixbuf
		self.gridImage = gridimage.GridImage(self.pixbuf, self.numRows, self.numCols)
		self.img.change_image(self.pixbufToDisplay)
	
	def append_recent_file(self, filename):
		maxRecentFiles=10
		recentFiles = []

		#store current contents
		recent_file = open("recent.txt", "r")
		for line in recent_file:
			if(line != "\n"):
				recentFiles.append(line.rstrip())
		recent_file.close()

		#shift lines backward one, add passed filename at end
		numRecentFiles=len(recentFiles)
		if(numRecentFiles >= maxRecentFiles):
			for i in range(numRecentFiles-1):
				recentFiles[i] = recentFiles[i+1]
			recentFiles[numRecentFiles-1] = filename
		else:
			recentFiles.append(filename)

		#write contents back
		recent_file = open("recent.txt", "w")
		for file in recentFiles:
			recent_file.write(file + str("\n"))
		recent_file.close()



