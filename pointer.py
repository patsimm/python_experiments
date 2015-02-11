import time
import math

class PointerPainter():

    def __init__(self):
        self.circles = []

    def draw_circles(self, cr):
        for circle in self.circles:
            if circle.is_alive():
                circle.draw(cr)
            else:
                self.circles.remove(circle)

    def motion(self, darea, event):
        self.circles.append(Circle(event.x, event.y, time.time()))


class Circle():

    def __init__(self, pos_x, pos_y, birth):
        self.pos_x, self.pos_y = pos_x, pos_y
        self.birth = birth

    def draw(self, cr):
        time_alive = (time.time() - self.birth)*1.5
        cr.set_source_rgb(
            (time_alive/4),
            (time_alive/8)+0.5,
            0.5-(time_alive/8)+0.25
        )
        cr.arc(self.pos_x, self.pos_y, int(time_alive*10), 0, 2*math.pi)
        cr.stroke()

    def is_alive(self):
        now = time.time()
        if now > self.birth + 4:
            return False
        return True
