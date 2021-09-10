import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf
import cyclemode
import tiletype
import random

class GridImage:

	def __init__(self, pixbuf, rows, columns, cycleMode, overlapPercent):
		self.width=pixbuf.get_width()
		self.height=pixbuf.get_height()
		self.numRows=rows
		self.numColumns=columns
		self.pixbuf = pixbuf
		self.subpixbufs = []
		self.numSubpixbufs = 0
		self.currSubpixbuf = 0
		self.rowHeight = 0
		self.columnWidth = 0
		self.overlapPercent = overlapPercent
		self.tileIndexes = [] #list containing ordered or random sequence of subpixbufs

		remainderWidth = self.width%columns
		remainderHeight = self.height%rows
		self.rowHeight = self.height//rows
		self.columnWidth = self.width//columns

		self.numSubpixbufs = rows * columns

		currX=0
		currY=0
		widthAdd=0
		heightAdd=0

		if(overlapPercent != 0):
			overlapWidth=self.columnWidth//overlapPercent
			overlapHeight=self.rowHeight//overlapPercent

		currentIndex=0
		for i in range(self.numRows):
			for j in range(self.numColumns):
				currentIndex = i*self.numColumns+j

				# While there is remainder remaining, add one more pixel to the
				# size of the next row/column. The remainder of a division
				# operation is always less than the divisor, so we'll always
				# run out of remainder before the end of the image.
				if(remainderWidth > 0):
					widthAdd=1
					remainderWidth-=1
				if(remainderHeight > 0):
					heightAdd=1
					remainderHeight-=1


				# For each tile scenario outlined in this block, we add pixels to
				# each side that can be expanded. (you can't expand outside the
				# image bounds). For example, a center tile can use pixels all
				# around it, but a corner tile can only use two sides, because
				# the other two sides are blank!
				if(overlapPercent != 0):
					pos = tiletype.tileType(currentIndex, self.numRows, self.numColumns)
					if(pos == tiletype.TileType.CENTER):
						subpixbuf = pixbuf.new_subpixbuf(currX-overlapWidth, currY-overlapHeight, self.columnWidth+widthAdd+overlapWidth*2, self.rowHeight+heightAdd+overlapHeight*2)
					elif(pos == tiletype.TileType.EDGE):
						pos = tiletype.edgeType(currentIndex, self.numRows, self.numColumns)
						if(pos == tiletype.EdgeType.TOP):
							subpixbuf = pixbuf.new_subpixbuf(currX-overlapWidth, currY, self.columnWidth+widthAdd+overlapWidth*2, self.rowHeight+heightAdd+overlapHeight)
						elif(pos == tiletype.EdgeType.RIGHT):
							subpixbuf = pixbuf.new_subpixbuf(currX-overlapWidth, currY-overlapHeight, self.columnWidth+widthAdd+overlapWidth, self.rowHeight+heightAdd+overlapHeight*2)
						elif(pos == tiletype.EdgeType.BOTTOM):
							subpixbuf = pixbuf.new_subpixbuf(currX-overlapWidth, currY-overlapHeight, self.columnWidth+widthAdd+overlapWidth*2, self.rowHeight+heightAdd+overlapHeight)
						elif(pos == tiletype.EdgeType.LEFT):
							subpixbuf = pixbuf.new_subpixbuf(currX, currY-overlapHeight, self.columnWidth+widthAdd+overlapWidth, self.rowHeight+heightAdd+overlapHeight*2)
					elif(pos == tiletype.TileType.CORNER):
						pos = tiletype.cornerType(currentIndex, self.numRows, self.numColumns)
						if(pos == tiletype.CornerType.TOPLEFT):
							subpixbuf = pixbuf.new_subpixbuf(currX, currY, self.columnWidth+widthAdd+overlapWidth, self.rowHeight+heightAdd+overlapHeight)
						elif(pos == tiletype.CornerType.TOPRIGHT):
							subpixbuf = pixbuf.new_subpixbuf(currX-overlapWidth, currY, self.columnWidth+widthAdd+overlapWidth, self.rowHeight+heightAdd+overlapHeight)
						elif(pos == tiletype.CornerType.BOTTOMRIGHT):
							subpixbuf = pixbuf.new_subpixbuf(currX-overlapWidth, currY-overlapHeight, self.columnWidth+widthAdd+overlapWidth, self.rowHeight+heightAdd+overlapHeight)
						elif(pos == tiletype.CornerType.BOTTOMLEFT):
							subpixbuf = pixbuf.new_subpixbuf(currX, currY-overlapHeight, self.columnWidth+widthAdd+overlapWidth, self.rowHeight+heightAdd+overlapHeight)
				else:
					subpixbuf = pixbuf.new_subpixbuf(currX, currY, self.columnWidth+widthAdd, self.rowHeight+heightAdd)

				self.subpixbufs.append(subpixbuf)
				widthAdd=0
				heightAdd=0
				currX+=self.columnWidth+widthAdd
			currY+=self.rowHeight+heightAdd
			currX=0

		if(cycleMode == cyclemode.CycleMode.random):
			for i in range(self.numSubpixbufs):
				self.tileIndexes.append(i)
			random.shuffle(self.tileIndexes)
		else:
			for i in range(self.numSubpixbufs):
				self.tileIndexes.append(i)

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
		pixbuf = self.subpixbufs[self.tileIndexes[self.currSubpixbuf]]
		return pixbuf

	def getPrev(self):
		self.currSubpixbuf-=1
		if(self.currSubpixbuf == -1):
			self.currSubpixbuf = self.numSubpixbufs-1
		pixbuf = self.subpixbufs[self.tileIndexes[self.currSubpixbuf]]
		return pixbuf

