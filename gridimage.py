import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf

class GridImage:

	width = 0
	height = 0
	numRows = 0
	numColumns = 0
	subpixbufs = []
	numSubpixbufs = 0
	currSubpixbuf = 0
	pixbuf = None
	rowHeight = 0
	columnWidth = 0

	def __init__(self, pixbuf, rows, columns):
		self.width=pixbuf.get_width()
		self.height=pixbuf.get_height()
		self.numRows=rows
		self.numColumns=columns
		self.pixbuf = pixbuf

		remainderWidth = self.width%columns
		remainderHeight = self.height%rows
		self.rowHeight = self.height//rows
		self.columnWidth = self.width//columns

		self.numSubpixbufs = rows * columns

		currX=0
		currY=0
		widthAdd=0
		heightAdd=0
		for i in range(self.numRows):
			for j in range(self.numColumns):
				if(remainderWidth > 0):
					widthAdd=1
					remainderWidth-=1
				if(remainderHeight > 0):
					heightAdd=1
					remainderHeight-=1
				subpixbuf = pixbuf.new_subpixbuf(currX, currY, self.columnWidth+widthAdd, self.rowHeight+heightAdd)
				self.subpixbufs.append(subpixbuf)
				widthAdd=0
				heightAdd=0
				currX+=self.columnWidth+widthAdd
			currY+=self.rowHeight+heightAdd
			currX=0

	def getNumRows(self):
		return self.numRows
	
	def getNumColumns(self):
		return self.numColumns

	def getNumSubpixbufs(self):
		return self.numSubpixbufs

	def getSubpixbufs(self):
		return self.subpixbufs

	def getPixbuf(self):
		return self.pixbuf

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def getRowHeight(self):
		return self.rowHeight

	def getColumnWidth(self):
		return self.columnWidth

	def getCurrSubpixbuf(self):
		return self.currSubpixbuf

	def getNext(self):
		self.currSubpixbuf+=1
		if(self.currSubpixbuf == self.numSubpixbufs):
			self.currSubpixbuf = 0
		pixbuf = self.subpixbufs[self.currSubpixbuf]
		return pixbuf

	def getPrev(self):
		self.currSubpixbuf-=1
		if(self.currSubpixbuf == -1):
			self.currSubpixbuf = self.numSubpixbufs-1
		pixbuf = self.subpixbufs[self.currSubpixbuf]
		return pixbuf

