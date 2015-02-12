from gi.repository import Gtk, GLib
import time
import math
import coloring

SIZE = 500
start = time.time()

class PointerPainter():

    def __init__(self, darea):
        self.circles = []
        self.darea = darea

        self.darea.set_size_request(SIZE, SIZE)
        GLib.timeout_add(50, self._draw)

    def draw(self, cr):
        for circle in self.circles:
            if circle.is_alive():
                circle.draw(cr)
            else:
                self.circles.remove(circle)

    def motion(self, darea, event):
        self.circles.append(Circle(event.x, event.y, time.time()))

    def quit(self, window, event):
        Gtk.main_quit()

    def _draw(self):
        self.darea.queue_draw()
        return True

class Circle():

    def __init__(self, pos_x, pos_y, birth):
        self.pos_x, self.pos_y = pos_x, pos_y
        self.birth = birth

    def draw(self, cr):
        time_alive = (time.time() - self.birth)
        color_index = ((time.time() - start) * 10 - time_alive * 10) * 10
        cr.set_source_rgb(*coloring.rainbow(color_index))
        cr.arc(self.pos_x, self.pos_y, int(time_alive*10), 0, 2*math.pi)
        cr.stroke()

    def is_alive(self):
        now = time.time()
        if now > self.birth + 4:
            return False
        return True
