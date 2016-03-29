from random import randint, random
from math import cos, sin, pi

import shelve

from settings_storage import settings


class Figure:
    '''
    implement randoms figures on field
    реализует фигуры на поле
    '''
    _used_points = []

    def __init__(self, id, pygame, surface, load=False):
        self.id = id
        self.pygame = pygame
        self.surface = surface
        self.width = 1
        self.color = settings.black
        self.vertices = []  # vertices

        Figure._used_points.append(settings.SPAWN_POINT)

        if not load:  # if self.vertices is None:
            x, y = 0, 0
            while True:
                collide = False
                x = randint(settings.MAX_FIGURE_RAD,
                            settings.DISPLAY_RES[0] - settings.MAX_FIGURE_RAD)

                y = randint(settings.MAX_FIGURE_RAD,
                            settings.DISPLAY_RES[1] - settings.MAX_FIGURE_RAD)

                for used_x, used_y in Figure._used_points:
                    if (x - used_x)**2 + (y - used_y)**2 < 4 * settings.MAX_FIGURE_RAD**2:
                        collide = True

                if not collide:
                    break

            Figure._used_points.append((x, y))
            self.__gen_figure((x, y))

        else: # LOAD
            pass

    def __gen_figure(self, base_point):
        shapes_count = randint(settings.MIN_SHAPES_COUNT, settings.MAX_SHAPES_COUNT)

        fi = 0  # NEED MORE RANDOM
        for shape_number in range(shapes_count):
            r = randint(settings.MIN_FIGURE_RAD, settings.MAX_FIGURE_RAD)
            x = int(base_point[0] + r * cos(fi))
            y = int(base_point[1] + r * sin(fi))

            self.vertices.append([x, y])

            fi += 2 * pi/shapes_count

    def draw(self):
        self.pygame.draw.polygon(self.surface, self.color, self.vertices, self.width)

    def draw_circles(self):
        for point in Figure._used_points:
            self.pygame.draw.circle(self.surface, settings.red, point, settings.MAX_FIGURE_RAD, 1)

    def save(self):
        with shelve.open(settings.SHELVE_FILE_NAME) as db:
            db[str(self.id)] = self.vertices
        db.close()

    def load(self):
        with shelve.open(settings.SHELVE_FILE_NAME) as db:
            self.vertices = db[str(self.id)]
        db.close()