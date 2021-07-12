import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf
import gridimage
import scaleimage
import recentlist
import overviewimage
import cyclemode
import os

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
		self.overviewImage = None
		self.filename = None
		self.mainBox = None
		self.leftPanel = None
		self.centerPanel = None
		self.rightPanel = None
		self.cycleMode = cyclemode.CycleMode.sequential;
		self.overlapAmount = 0;

		Gtk.Window.__init__(self)

		self.set_default_size(1000,800)
		self.set_title("WaldoGazer")
	
		self.menubar = self.buildMenu()

		self.vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.mainBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		self.leftPanel = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.centerPanel = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.rightPanel = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
		self.mainBox.pack_start(self.leftPanel, False, False, 5)
		self.mainBox.pack_start(self.centerPanel, True, True, 5)
		self.mainBox.pack_start(self.rightPanel, True, True, 5)
		self.vbox.pack_start(self.menubar, False, False, 0);
		self.vbox.pack_start(self.mainBox, True, True, 1);

		self.filename = "blank.png"
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.filename)
		self.img = scaleimage.ScaleImage(self.pixbuf, self.filename)

		rowsSpin = Gtk.SpinButton.new_with_range(1,50,1)
		colsSpin = Gtk.SpinButton.new_with_range(1,50,1)
		rowsSpin.set_value(self.numRows)
		colsSpin.set_value(self.numCols)
		rowsLabel = Gtk.Label.new("Rows")
		colsLabel = Gtk.Label.new("Columns")
		spinGrid = Gtk.Grid()
		spinGrid.attach(rowsLabel, 0,0,1,1)
		spinGrid.attach(rowsSpin, 1,0,1,1)
		spinGrid.attach(colsLabel,0,1,1,1)
		spinGrid.attach(colsSpin,1,1,1,1)

		nextButton = Gtk.Button.new_with_label("Next")
		nextButton.connect("clicked", self.on_next_clicked)
		prevButton = Gtk.Button.new_with_label("Previous")
		prevButton.connect("clicked", self.on_prev_clicked)
		self.positionIndicator = Gtk.Label("0/0")
		buttonHBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 5)
		buttonHBox.pack_start(prevButton, True, True, 0)
		buttonHBox.pack_start(nextButton, True, True, 0)
		buttonHBox.pack_start(self.positionIndicator, False, False, 0)

		self.recentList = recentlist.RecentList(self.recentFile)
		self.recentList.connect("recent_file_selected", self.on_recent_file_selected);

		self.overviewImage = overviewimage.OverviewImage(self.gridImage)
		self.overviewImage.set_vexpand(True)
		self.overviewImage.set_hexpand(True)

		self.reload()

		rowsSpin.connect("value-changed", self.on_rows_changed); 
		colsSpin.connect("value-changed", self.on_cols_changed); 

		radioLabel = Gtk.Label.new("Cycle Type")
		self.sequentialRadio = Gtk.RadioButton.new_with_label(None, "Sequential")
		self.randomRadio = Gtk.RadioButton.new_with_label_from_widget(self.sequentialRadio, "Random")

		self.sequentialRadio.connect("toggled", self.cycleRadioToggled)
		self.randomRadio.connect("toggled", self.cycleRadioToggled)

		radioBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		radioBox.pack_start(radioLabel, False, False, 0)
		radioBox.pack_start(self.sequentialRadio, False, False, 0)
		radioBox.pack_start(self.randomRadio, False, False, 0)

		overlapCheckBox = Gtk.CheckButton.new_with_label("Overlap Tiles")
		overlapCheckBox.connect("toggled", self.on_overlap_check_clicked)

		self.leftPanel.pack_start(self.recentList, False, True, 0)
		self.centerPanel.pack_start(self.img, True, True, 0)
		self.rightPanel.pack_start(self.overviewImage, True, True, 0)
		self.rightPanel.pack_start(buttonHBox, False, False, 0)
		self.rightPanel.pack_start(spinGrid, False, False, 0)
		self.rightPanel.pack_start(radioBox, False, False, 0)
		self.rightPanel.pack_start(overlapCheckBox, False, False, 0)

		self.connect("destroy", Gtk.main_quit)

		self.add(self.vbox)

	def on_next_clicked(self, widget):
		self.pixbufToDisplay = self.gridImage.getNext()
		self.img.change_image(self.pixbufToDisplay, None)
		self.overviewImage.queue_draw()
		self.updatePositionIndicator()

	def on_prev_clicked(self, widget):
		self.pixbufToDisplay = self.gridImage.getPrev()
		self.img.change_image(self.pixbufToDisplay, None)
		self.overviewImage.queue_draw()
		self.updatePositionIndicator()

	def on_rows_changed(self, scale):
		self.numRows = int(scale.get_value())
		self.reload()

	def on_cols_changed(self, scale):
		self.numCols = int(scale.get_value())
		self.reload()

	def reload(self):
		if(self.pixbuf == None):
			return
		self.gridImage = gridimage.GridImage(self.pixbuf, self.numRows, self.numCols, self.cycleMode, self.overlapAmount)
		self.pixbufToDisplay = self.gridImage.getSubpixbufs()[self.gridImage.tileIndexes[self.gridImage.getCurrSubpixbuf()]]
		self.img.change_image(self.pixbufToDisplay, None)
		self.overviewImage.change(self.gridImage)
		self.updatePositionIndicator()
		self.set_title(os.path.basename(self.filename) + " - WaldoGazer")

	def reload_recentlist(self):
		self.leftPanel.remove(self.recentList)
		self.recentList = recentlist.RecentList(self.recentFile)
		self.recentList.connect("recent_file_selected", self.on_recent_file_selected);
		self.leftPanel.pack_end(self.recentList, True, True, 0)
		self.show_all()

	def insert_recent_file(self, filename):
		maxRecentFiles=10
		recentFiles = []

		#store current contents
		try:
			recent_file = open(self.recentFile, "r")
			for line in recent_file:
				stripped = line.strip()
				#don't copy any entries that match passed filename
				if(stripped != "\n" and stripped != filename):
					recentFiles.append(stripped)
			recent_file.close()

			#shift lines backward one, add passed filename at end
			numRecentFiles=len(recentFiles)
			if(numRecentFiles >= maxRecentFiles):
				for i in range(numRecentFiles-1):
					recentFiles[i] = recentFiles[i+1]
				recentFiles[numRecentFiles-1] = filename
			else:
				recentFiles.insert(0,filename)

		except FileNotFoundError:
			recentFiles.insert(0,filename)

		#write contents back
		recent_file = open("recent.txt", "w")
		for file in recentFiles:
			recent_file.write(file + str("\n"))
		recent_file.close()

	def on_recent_file_selected(self, widget, filename):
		self.filename = filename
		self.insert_recent_file(self.filename)
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.filename)
		self.reload()
		self.reload_recentlist()

	def cycleRadioToggled(self, widget):
		if(widget == self.sequentialRadio and self.sequentialRadio.get_active()):
			self.cycleMode = cyclemode.CycleMode.sequential
		elif (widget == self.randomRadio and self.randomRadio.get_active()):
			self.cycleMode = cyclemode.CycleMode.random
		self.reload()

	def fileOpenClicked(self, widget):
		dialog = Gtk.FileChooserDialog( title="Open...", parent=self, action=Gtk.FileChooserAction.OPEN)
		dialog.add_buttons( Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.filename = dialog.get_filename() 
			self.insert_recent_file(self.filename)
			self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.filename)
			self.reload()
			self.reload_recentlist()
		dialog.destroy()


	def buildMenu(self):

		mb = Gtk.MenuBar()

		filemenu = Gtk.Menu()

		filem = Gtk.MenuItem("File")
		filem.set_submenu(filemenu)

		fileOpen = Gtk.MenuItem("Open...")

		fileOpen.connect("activate", self.fileOpenClicked)

		filemenu.append(fileOpen)

		mb.append(filem)

		return mb

	def updatePositionIndicator(self):
		self.positionIndicator.set_text(str(self.gridImage.getCurrSubpixbuf()+1) + "/" + str(self.numCols * self.numRows))
	
	def on_overlap_check_clicked(self, widget):
		if(widget.get_active()):
			self.overlapAmount = 0.10
		else:
			self.overlapAmount = 0
