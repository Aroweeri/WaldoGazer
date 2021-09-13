import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import cairo
import tiletype

class OverviewImage(Gtk.DrawingArea):

	def __init__(self, gridimage):
		self.gridimage = None
		self.pixbuf = None
		Gtk.DrawingArea.__init__(self)
		self.gridimage = gridimage
		if(self.gridimage != None):
			self.pixbuf = self.gridimage.getPixbuf()

	def change(self, gridimage):
		self.queue_draw()
		self.gridimage = gridimage
		self.pixbuf = self.gridimage.getPixbuf()

	def do_draw(self, cr):

		if(self.gridimage == None):
			return

		startx = 0
		starty = 0

		alloc, baseline = self.get_allocated_size()
		factor = min(alloc.width / self.pixbuf.get_width(), alloc.height / self.pixbuf.get_height())
		cr.scale(factor, factor)
		Gdk.cairo_set_source_pixbuf(cr, self.pixbuf, 0, 0)
		cr.paint()

		#darken parts not shown
		mask = cairo.ImageSurface(cairo.Format.ARGB32, self.pixbuf.get_width(), self.pixbuf.get_height())
		mask_cr = cairo.Context(mask)

		mask_cr.set_source_rgba(1,1,1,1);
		mask_cr.rectangle(0,0,self.pixbuf.get_width(), self.pixbuf.get_height())
		mask_cr.fill()

		mask_cr.set_source_rgba(1,1,1,0);
		mask_cr.set_operator(cairo.OPERATOR_CLEAR)
		starty = ((self.gridimage.tileIndexes[self.gridimage.getCurrSubpixbuf()])//self.gridimage.getNumColumns()) * self.gridimage.getRowHeight()
		startx = (self.gridimage.tileIndexes[self.gridimage.getCurrSubpixbuf()]%self.gridimage.getNumColumns()) * self.gridimage.getColumnWidth()

		if(self.gridimage.overlapPercent != 0):

			overlapWidth=self.gridimage.columnWidth//self.gridimage.overlapPercent
			overlapHeight=self.gridimage.rowHeight//self.gridimage.overlapPercent

			pos = tiletype.tileType(self.gridimage.tileIndexes[self.gridimage.getCurrSubpixbuf()], self.gridimage.numRows, self.gridimage.numColumns)
			if(pos == tiletype.TileType.CENTER):
				mask_cr.rectangle(startx-overlapWidth, starty-overlapHeight, self.gridimage.getColumnWidth()+overlapWidth*2, self.gridimage.getRowHeight()+overlapHeight*2)
			elif(pos == tiletype.TileType.EDGE):
				pos = tiletype.edgeType(self.gridimage.tileIndexes[self.gridimage.getCurrSubpixbuf()], self.gridimage.numRows, self.gridimage.numColumns)
				if(pos == tiletype.EdgeType.TOP):
					mask_cr.rectangle(startx-overlapWidth, starty, self.gridimage.getColumnWidth()+overlapWidth*2, self.gridimage.getRowHeight()+overlapHeight)
				elif(pos == tiletype.EdgeType.RIGHT):
					mask_cr.rectangle(startx-overlapWidth, starty-overlapHeight, self.gridimage.getColumnWidth()+overlapWidth, self.gridimage.getRowHeight()+overlapHeight*2)
				elif(pos == tiletype.EdgeType.BOTTOM):
					mask_cr.rectangle(startx-overlapWidth, starty-overlapHeight, self.gridimage.getColumnWidth()+overlapWidth*2, self.gridimage.getRowHeight()+overlapHeight)
				elif(pos == tiletype.EdgeType.LEFT):
					mask_cr.rectangle(startx, starty-overlapHeight, self.gridimage.getColumnWidth()+overlapWidth, self.gridimage.getRowHeight()+overlapHeight*2)
			elif(pos == tiletype.TileType.CORNER):
				pos = tiletype.cornerType(self.gridimage.tileIndexes[self.gridimage.getCurrSubpixbuf()], self.gridimage.numRows, self.gridimage.numColumns)
				if(pos == tiletype.CornerType.TOPLEFT):
					mask_cr.rectangle(startx, starty, self.gridimage.getColumnWidth()+overlapWidth, self.gridimage.getRowHeight()+overlapHeight)
				elif(pos == tiletype.CornerType.TOPRIGHT):
					mask_cr.rectangle(startx-overlapWidth, starty, self.gridimage.getColumnWidth()+overlapWidth, self.gridimage.getRowHeight()+overlapHeight)
				elif(pos == tiletype.CornerType.BOTTOMRIGHT):
					mask_cr.rectangle(startx-overlapWidth, starty-overlapHeight, self.gridimage.getColumnWidth()+overlapWidth, self.gridimage.getRowHeight()+overlapHeight)
				elif(pos == tiletype.CornerType.BOTTOMLEFT):
					mask_cr.rectangle(startx, starty-overlapHeight, self.gridimage.getColumnWidth()+overlapWidth, self.gridimage.getRowHeight()+overlapHeight)
		else:
			mask_cr.rectangle(startx, starty, self.gridimage.getColumnWidth(), self.gridimage.getRowHeight())

		mask_cr.fill()
		mask_cr.set_operator(cairo.OPERATOR_OVER)

		cr.set_source_rgba(0,0,0,0.7)
		cr.mask_surface(mask, 0, 0)

		#draw horizontal lines
		cr.set_source_rgb(255,255,255)
		cr.set_line_width(3)
		for i in range(1,self.gridimage.getNumRows()):
			y = i*self.gridimage.getRowHeight()
			cr.move_to(0, y)
			cr.line_to(self.gridimage.getWidth(), y)
		cr.stroke()

		#draw vertical lines
		for i in range(1,self.gridimage.getNumColumns()):
			x = i*self.gridimage.getColumnWidth()
			cr.move_to(x, 0)
			cr.line_to(x, self.gridimage.getHeight())
		cr.stroke()

