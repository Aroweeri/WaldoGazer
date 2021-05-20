import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk

class ScaleImage(Gtk.DrawingArea):

	pixbuf = None
	filename = None
	
	def __init__(self, pixbuf, filename):
		Gtk.DrawingArea.__init__(self)
		self.pixbuf = pixbuf
		self.filename = filename

	def change_image(self, pixbuf, filename):
		self.pixbuf = pixbuf
		self.filename = filename
		self.queue_draw()

	def do_draw(self, cr):
		alloc, baseline = self.get_allocated_size()
		factor = min(alloc.width / self.pixbuf.get_width(), alloc.height / self.pixbuf.get_height())
		cr.scale(factor, factor)
		Gdk.cairo_set_source_pixbuf(cr, self.pixbuf, 0, 0)
		cr.paint()
