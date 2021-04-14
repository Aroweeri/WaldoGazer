import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf

class GridImage:

	def __init__(self, pixbuf, rows, columns):
		self.width=pixbuf.get_width()
		self.height=pixbuf.get_height()
		self.numRows=rows
		self.numColumns=columns
		self.subpixbufs=[]
		self.numSubpixbufs=0
		self.currSubpixbuf=0

		remainderWidth = self.width%columns
		remainderHeight = self.height%rows
		rowHeight = self.height//rows
		columnWidth = self.width//columns

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
				subpixbuf = pixbuf.new_subpixbuf(currX, currY, columnWidth+widthAdd, rowHeight+heightAdd)
				subpixbuf = subpixbuf.scale_simple(700,700,GdkPixbuf.InterpType.BILINEAR)
				self.subpixbufs.append(subpixbuf)
				widthAdd=0
				heightAdd=0
				currX+=columnWidth+widthAdd
			currY+=rowHeight+heightAdd
			currX=0

	def getNumRows(self):
		return self.numRows
	
	def getNumColumns(self):
		return self.numColumns

	def getNumSubpixbufs(self):
		return self.numSubpixbufs

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def getNext(self):
		if(self.currSubpixbuf == self.numSubpixbufs):
			self.currSubpixbuf = 0
		pixbuf = self.subpixbufs[self.currSubpixbuf]
		self.currSubpixbuf+=1
		return pixbuf
