from random import randint, random
from math import cos, sin, pi

from settings_storage import settings


class Figure:
    '''
    implement randoms figures on field
    реализует фигуры на поле
    '''
    used_points = []

    def __init__(self, game, vertices=None):
        self.game = game

        self.width = 1
        self.color = settings.black
        self.vertices = [] #  vertices or None

        if vertices:
            self.vertices = vertices
        else:
            x, y = 0, 0
            while True:
                collide = False
                x = randint(settings.MAX_FIGURE_RAD, settings.DISPLAY_RES[0] - settings.MAX_FIGURE_RAD)
                y = randint(settings.MAX_FIGURE_RAD, settings.DISPLAY_RES[1] - settings.MAX_FIGURE_RAD)

                if len(Figure.used_points) == 0:
                    break
                else:
                    for used_x, used_y in Figure.used_points:
                        if (x - used_x)**2 + (y - used_y)**2 < 4 * settings.MAX_FIGURE_RAD**2:
                            collide = True

                if not collide:
                    break

            Figure.used_points.append((x, y))
            self.__gen_figure((x, y))

    def __gen_figure(self, base_point):
        shapes_count = randint(settings.MIN_SHAPES_COUNT, settings.MAX_SHAPES_COUNT)

        fi = 0 # NEED MORE RANDOM
        for shape_number in range(shapes_count):
            r = randint(settings.MIN_FIGURE_RAD, settings.MAX_FIGURE_RAD)
            x = int(base_point[0] + r * cos(fi))
            y = int(base_point[1] + r * sin(fi))

            self.vertices.append([x, y])

            fi += 2 * pi/shapes_count

    def draw(self, surface):
        self.game.draw.polygon(surface, self.color, self.vertices, self.width)


    #def draw_circles(surface):
    #    for point in Figure.used_points:
    #        self.game.draw.circle(surface, red, point, MAX_FIGURE_RAD, 1)