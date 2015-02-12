from gi.repository import Gtk, GLib, Gdk
import random
import threading
import time
Gdk.threads_init()
GLib.threads_init()

MAZE_SIZE = 75
CELL_WIDTH = 4
WALL_WIDTH = 4


class PrimsPainter():

    def __init__(self, darea):
        self.darea = darea

        width = (CELL_WIDTH + WALL_WIDTH) * MAZE_SIZE + WALL_WIDTH
        self.darea.set_size_request(width, width)

        self.cells = []
        self.walls = []
        self.edges = []

        self.last_cells = []

        half_size = MAZE_SIZE / 2
        self.cells.append(dict(x=half_size, y=half_size))
        self.last_cells.append(dict(x=half_size, y=half_size))
        self._add_walls(dict(x=half_size, y=half_size))

        self.step_number = 0

        self.finished = False
        threading.Thread(target=self._step).start()
        GLib.timeout_add(100, self._draw)

    def draw(self, cr):
        cr.set_source_rgb(0, 0, 0)
        width = (CELL_WIDTH + WALL_WIDTH) * MAZE_SIZE + WALL_WIDTH
        cr.rectangle(0, 0, width, width)
        cr.fill()
        cr.set_source_rgb(0.5, 0.9, 0)
        for cell in self.cells:
            x1 = cell['x'] * (CELL_WIDTH + WALL_WIDTH) + WALL_WIDTH
            y1 = cell['y'] * (CELL_WIDTH + WALL_WIDTH) + WALL_WIDTH
            cr.rectangle(x1, y1, CELL_WIDTH, CELL_WIDTH)
            cr.fill()
        cr.set_source_rgb(0.75, 0, 0.75)
        for wall in self.walls:
            if wall[0]['x'] == wall[1]['x']:
                x1 = wall[0]['x'] * (CELL_WIDTH + WALL_WIDTH) + WALL_WIDTH
                min_y = min(wall[0]['y'], wall[1]['y'])
                y1 = (min_y + 1) * (CELL_WIDTH + WALL_WIDTH)
                cr.rectangle(x1, y1, WALL_WIDTH, WALL_WIDTH)
            if wall[0]['y'] == wall[1]['y']:
                min_x = min(wall[0]['x'], wall[1]['x'])
                x1 = (min_x + 1) * (CELL_WIDTH + WALL_WIDTH)
                y1 = wall[0]['y'] * (CELL_WIDTH + WALL_WIDTH) + WALL_WIDTH
                cr.rectangle(x1, y1, WALL_WIDTH, WALL_WIDTH)
        cr.fill()
        cr.set_source_rgb(1, 1, 1)
        for edge in self.edges:
            if edge[0]['x'] == edge[1]['x']:
                x1 = edge[0]['x'] * (CELL_WIDTH + WALL_WIDTH) + WALL_WIDTH
                min_y = min(edge[0]['y'], edge[1]['y'])
                y1 = min_y * (CELL_WIDTH + WALL_WIDTH) + WALL_WIDTH
                cr.rectangle(x1, y1, CELL_WIDTH, CELL_WIDTH*2+WALL_WIDTH)
                cr.fill()
            elif edge[0]['y'] == edge[1]['y']:
                min_x = min(edge[0]['x'], edge[1]['x'])
                x1 = min_x * (CELL_WIDTH + WALL_WIDTH) + WALL_WIDTH
                y1 = edge[0]['y'] * (CELL_WIDTH + WALL_WIDTH) + WALL_WIDTH
                cr.rectangle(x1, y1, CELL_WIDTH*2+WALL_WIDTH, CELL_WIDTH)
        cr.fill()

    def quit(self, window, event):
        self.finished = False
        time.sleep(0.5)
        Gtk.main_quit()

    def _add_walls(self, cell):
        xn, yn = cell['x'], cell['y']+1
        xe, ye = cell['x']+1, cell['y']
        xs, ys = cell['x'], cell['y']-1
        xw, yw = cell['x']-1, cell['y']
        cell_n = cell_w = cell_e = cell_s = None

        if 0 <= xn < MAZE_SIZE and 0 <= yn < MAZE_SIZE:
            cell_n = dict(x=xn, y=yn)
        if 0 <= xe < MAZE_SIZE and 0 <= ye < MAZE_SIZE:
            cell_e = dict(x=xe, y=ye)
        if 0 <= xs < MAZE_SIZE and 0 <= ys < MAZE_SIZE:
            cell_s = dict(x=xs, y=ys)
        if 0 <= xw < MAZE_SIZE and 0 <= yw < MAZE_SIZE:
            cell_w = dict(x=xw, y=yw)

        Gdk.threads_enter()
        if cell_n is not None:
            if (cell_n, cell) not in self.walls:
                self.walls.append((cell, cell_n, random.randint(0, 1000)))
        if cell_e is not None:
            if (cell_e, cell) not in self.walls:
                self.walls.append((cell, cell_e, random.randint(0, 1000)))
        if cell_s is not None:
            if (cell_s, cell) not in self.walls:
                self.walls.append((cell, cell_s, random.randint(0, 1000)))
        if cell_w is not None:
            if (cell_w, cell) not in self.walls:
                self.walls.append((cell, cell_w, random.randint(0, 1000)))
        Gdk.threads_leave()

    def _get_smallest_wall(self):
        smallest_wall = self.walls[0]
        for wall in self.walls[1:]:
            if wall[2] < smallest_wall[2]:
                smallest_wall = wall
        return smallest_wall

    def _step(self):
        while not self.finished:
            wall = self._get_smallest_wall()
            if wall[1] in self.cells:
                Gdk.threads_enter()
                self.walls.remove(wall)
                Gdk.threads_leave()
            else:
                Gdk.threads_enter()
                self.walls.remove(wall)
                self.edges.append(wall)
                self.cells.append(wall[1])
                Gdk.threads_leave()
                self._add_walls(wall[1])
            if len(self.walls) == 0:
                self.finished = True

    def _draw(self):
        self.darea.queue_draw()
        return True

    def motion(self, darea, event):
        pass
