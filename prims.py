from gi.repository import GLib
import random
import time

MAZE_SIZE = 100
CELL_WIDTH = 3
WALL_WIDTH = 5

class PrimsPainter():

    def __init__(self, darea):
        self.darea = darea

        self.cells = []
        self.walls = []
        self.edges = []

        self.cells.append(dict(x=0, y=0))
        self._add_walls(dict(x=0, y=0))

        self.step_number = 0

        GLib.idle_add(self._step)
        GLib.timeout_add(50, self._draw)

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

        if cell_n is not None:
            if (cell_n, cell) not in self.walls:
                self.walls.append((cell, cell_n))
        if cell_e is not None:
            if (cell_e, cell) not in self.walls:
                self.walls.append((cell, cell_e))
        if cell_s is not None:
            if (cell_s, cell) not in self.walls:
                self.walls.append((cell, cell_s))
        if cell_w is not None:
            if (cell_w, cell) not in self.walls:
                self.walls.append((cell, cell_w))

    def _step(self):
        if len(self.walls) != 0:
            random_index = random.randint(0, len(self.walls)-1)
            wall = self.walls[random_index]
            if wall[1] in self.cells:
                del self.walls[random_index]
            else:
                del self.walls[random_index]
                self.edges.append(wall)
                self.cells.append(wall[1])
                self._add_walls(wall[1])
            return True
        else:
            return False

    def _draw(self):
        self.darea.queue_draw()
        return True

    def motion(self, darea, event):
        pass
