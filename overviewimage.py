import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import cairo

class OverviewImage(Gtk.DrawingArea):

	gridimage = None
	pixbuf = None

	def __init__(self, gridimage):
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

		#darken parts not shown
		mask = cairo.ImageSurface(cairo.Format.ARGB32, self.pixbuf.get_width(), self.pixbuf.get_height())
		mask_cr = cairo.Context(mask)

		mask_cr.set_source_rgba(1,1,1,1);
		mask_cr.rectangle(0,0,self.pixbuf.get_width(), self.pixbuf.get_height())
		mask_cr.fill()

		mask_cr.set_source_rgba(1,1,1,0);
		mask_cr.set_operator(cairo.OPERATOR_CLEAR)
		starty = self.gridimage.getCurrSubpixbuf()//self.gridimage.getNumRows() * self.gridimage.getRowHeight()
		startx = self.gridimage.getCurrSubpixbuf()%self.gridimage.getNumColumns() * self.gridimage.getColumnWidth()
		mask_cr.rectangle(startx, starty, self.gridimage.getColumnWidth(), self.gridimage.getRowHeight())
		mask_cr.fill()
		mask_cr.set_operator(cairo.OPERATOR_OVER)

		cr.set_source_rgba(0,0,0,0.5)
		cr.mask_surface(mask, 0, 0)
