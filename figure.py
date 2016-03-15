from random import randint, random
from math import cos, sin, pi

from constants import *

# FIGURE


class Figure:
    used_points = []

    def __init__(self, game, vertices=None):
        self.game = game

        self.width = 1
        self.color = black
        self.vertices = [] #  vertices or None

        if vertices:
            self.vertices = vertices
        else:
            x, y = 0, 0
            while True:
                collide = False
                x = randint(MAX_FIGURE_RAD, DISPLAY_RES[0] - MAX_FIGURE_RAD)
                y = randint(MAX_FIGURE_RAD, DISPLAY_RES[1] - MAX_FIGURE_RAD)

                if len(Figure.used_points) == 0:
                    break
                else:
                    for used_x, used_y in Figure.used_points:
                        if (x - used_x)**2 + (y - used_y)**2 < 4 * MAX_FIGURE_RAD**2:
                            collide = True

                if not collide:
                    break

            Figure.used_points.append((x, y))
            self.__gen_figure((x, y))

    def __gen_figure(self, base_point):
        shapes_count = randint(MIN_SHAPES_COUNT, MAX_SHAPES_COUNT)

        fi = 0 # NEED MORE RANDOM
        for shape_number in range(shapes_count):
            r = randint(MIN_FIGURE_RAD, MAX_FIGURE_RAD)
            x = int(base_point[0] + r * cos(fi))
            y = int(base_point[1] + r * sin(fi))

            self.vertices.append([x, y])

            fi += 2 * pi/shapes_count

    def draw(self, surface):
        self.game.draw.polygon(surface, self.color, self.vertices, self.width)


    #def draw_circles(surface):
    #    for point in Figure.used_points:
    #        self.game.draw.circle(surface, red, point, MAX_FIGURE_RAD, 1)