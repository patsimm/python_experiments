from gi.repository import Gtk, Gdk, GLib
import math
import time
import pointer
import prims

def create():
    win = ColorWindow()


class ColorWindow(Gtk.Window):

    def __init__(self):
        super(ColorWindow, self).__init__()
        self._init_ui()
        Gtk.main()

    def _init_ui(self):
        self.darea = Gtk.DrawingArea()
        self.painter = prims.PrimsPainter(self.darea)
        self.darea.connect("draw", self.on_draw)
        self.darea.set_events(Gdk.EventMask.POINTER_MOTION_MASK |
                              Gdk.EventMask.POINTER_MOTION_HINT_MASK)
        self.darea.connect("motion-notify-event", self.painter.motion)
        self.add(self.darea)

        self.set_title("Fractals")
        self.resize(500, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_draw(self, wid, cr):
        self.painter.draw(cr)
