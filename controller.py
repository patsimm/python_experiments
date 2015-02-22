from gi.repository import Gtk, Gdk, GLib
import math
import time
import pointer
import prims
import randomtraversal


def create():
    win = ColorWindow()


class ColorWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self._init_ui()
        self.set_resizable(False)
        Gtk.main()

    def _init_ui(self):
        self.darea = Gtk.DrawingArea()

        self.painter = prims.PrimsPainter(self.darea)
        # self.painter = randomtraversal.RandomTraversalPainter(self.darea)
        # self.painter = pointer.PointerPainter(self.darea)

        self.darea.connect("draw", self.on_draw)
        self.darea.set_events(Gdk.EventMask.POINTER_MOTION_MASK |
                              Gdk.EventMask.POINTER_MOTION_HINT_MASK)
        self.darea.connect("motion-notify-event", self.painter.motion)
        self.add(self.darea)

        self.set_title("Python Experiments")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", self.painter.quit)
        self.show_all()

    def on_draw(self, wid, cr):
        self.painter.draw(cr)
