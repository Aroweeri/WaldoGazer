import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class OverviewImage(Gtk.DrawingArea):

	pixbuf = None
	rows = 0
	cols = 0

	def __init__(self, pixbuf):
		Gtk.DrawingArea.__init__(self)
		self.pixbuf = pixbuf

	def change_image(self, pixbuf):
		self.pixbuf = pixbuf
		self.queue_draw()

	def do_draw(self, cr):
		alloc, baseline = self.get_allocated_size()
		factor = min(alloc.width / self.pixbuf.get_width(), alloc.height / self.pixbuf.get_height())
		cr.scale(factor, factor)
		Gdk.cairo_set_source_pixbuf(cr, self.pixbuf, 0, 0)
		cr.paint()
