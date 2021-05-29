import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf
import gridimage
import scaleimage
import recentlist
import overviewimage


class WaldoGazer(Gtk.Window):

	def __init__(self, pixbuf, img):
		self.gridImage = None
		self.numRows=3
		self.numCols=3
		self.pixbuf=None
		self.pixbufToDisplay=None
		self.img=None
		self.recentFile="recent.txt"
		self.recentList = None
		self.grid = None
		self.overviewImage = None
		self.filename = None

		Gtk.Window.__init__(self)

		self.set_default_size(1000,800)
		self.set_title("WaldoGazer")

		self.grid = Gtk.Grid.new()

		file_chooser_button = Gtk.FileChooserButton()
		file_chooser_button.connect("file-set", self.on_file_selected)

		self.filename = "blank.png"
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.filename)
		self.img = scaleimage.ScaleImage(self.pixbuf, self.filename)
		self.img.set_vexpand(True)

		rowsScale = Gtk.Scale.new_with_range(Gtk.Orientation.VERTICAL, 1, 100, 1);
		colsScale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 100, 1);
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

		self.recentList = recentlist.RecentList(self.recentFile)
		self.recentList.connect("recent_file_selected", self.on_recent_file_selected);

		self.overviewImage = overviewimage.OverviewImage(self.gridImage)
		self.overviewImage.set_vexpand(True)
		self.overviewImage.set_hexpand(True)

		self.reload()

		rowsScale.connect("value-changed", self.on_rows_changed); 
		colsScale.connect("value-changed", self.on_cols_changed); 

		self.grid.attach(file_chooser_button, 0, 0, 1, 1)
		self.grid.attach(nextButton, 1, 0, 1, 1)
		self.grid.attach(prevButton, 2, 0, 1, 1)
		self.grid.attach(rowsScale, 3, 0, 1, 1)
		self.grid.attach(colsScale, 4, 0, 1, 1)
		self.grid.attach(self.recentList, 0, 1, 5, 1)
		self.grid.attach(self.img, 0, 2, 5, 1)
		self.grid.attach(self.overviewImage, 5,0,1,1)

		self.connect("destroy", Gtk.main_quit)

		self.add(self.grid)

	def on_file_selected(self, button):
		self.filename = button.get_filename()
		self.append_recent_file(self.filename)
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.filename)
		self.reload()
		self.reload_recentlist()

	def on_next_clicked(self, widget):
		self.pixbufToDisplay = self.gridImage.getNext()
		self.img.change_image(self.pixbufToDisplay, None)
		self.overviewImage.queue_draw()

	def on_prev_clicked(self, widget):
		self.pixbufToDisplay = self.gridImage.getPrev()
		self.img.change_image(self.pixbufToDisplay, None)
		self.overviewImage.queue_draw()

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
		self.img.change_image(self.pixbufToDisplay, None)
		self.overviewImage.change(self.gridImage)

	def reload_recentlist(self):
		self.grid.remove(self.recentList)
		self.recentList = recentlist.RecentList(self.recentFile)
		self.grid.attach(self.recentList, 0, 1, 5, 1)
		self.show_all()

	def append_recent_file(self, filename):
		maxRecentFiles=10
		recentFiles = []

		#store current contents
		recent_file = open(self.recentFile, "r")
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

	def on_recent_file_selected(self, widget, filename):
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
		self.reload()
