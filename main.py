from math import cos, sin, sqrt, pi
from random import randint
import pygame

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

EPS = 0.001

MIN_SHAPES_COUNT = 3
MAX_SHAPES_COUNT = 7

MAX_FIGURE_RAD = 45
MIN_FIGURE_RAD = 20

FIGURES_COUNT = 10

FPS = 60
DISPLAY_RES = (800, 600)


# FIGURE


class Figure:
    used_points = []

    def __init__(self, vertices=None):
        self.width = 1
        self.color = black
        self.vertices = []

        if vertices:
            self.vertices = vertices
        else:
            x, y = 0, 0
            while True:
                collide = False
                x = randint(MAX_FIGURE_RAD, DISPLAY_RES[0] - MAX_FIGURE_RAD)
                y = randint(MAX_FIGURE_RAD, DISPLAY_RES[1] - MAX_FIGURE_RAD)

                if len(Figure.used_points) > 0:
                    for used_x, used_y in Figure.used_points:
                        if (x - used_x)**2 + (y - used_y)**2 < 4 * MAX_FIGURE_RAD**2:
                            collide = True
                else:
                    break

                if not collide:
                    break

            Figure.used_points.append((x, y))
            self.__gen_figure((x, y))

    def __gen_figure(self, base_point):  # TODO MORE RANDOM
        shapes_count = randint(MIN_SHAPES_COUNT, MAX_SHAPES_COUNT)

        fi = 0
        for shape_number in range(shapes_count):
            r = randint(MIN_FIGURE_RAD, MAX_FIGURE_RAD)
            x = int(base_point[0] + r * cos(fi))
            y = int(base_point[1] + r * sin(fi))

            self.vertices.append([x, y])

            fi += 2 * pi/shapes_count

    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.vertices, self.width)

    @staticmethod
    def draw_circles(surface):
        for point in Figure.used_points:
            pygame.draw.circle(surface, red, point, MAX_FIGURE_RAD, 1)


# ROBOT #


class Robot:
    def __init__(self, position, visor_angle):
        self.position = position
        self.visor_angle = visor_angle
        self.angle = 0
        self.tail_long = sqrt(DISPLAY_RES[0] ** 2 + DISPLAY_RES[1] ** 2) / 2
        self.tail = [0, 0]

    def update(self, da):
        self.visor_angle += da
        self.tail[0] = self.position[0] + self.tail_long * cos(self.visor_angle)
        self.tail[1] = self.position[1] + self.tail_long * sin(self.visor_angle)

    def move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

    def get_distance(self, figures):
        def how_far(p1, p2):
            return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

        vision_line = Line(self.position, self.tail)

        min_dist = 10000
        min_point = []
        find_intersect_point = False
        storage = []
        for figure in figures:
            vertices_count = len(figure.vertices)
            for i in range(vertices_count):
                line_segment = Line(figure.vertices[i], figure.vertices[(i + 1) % vertices_count])

                intersect_point = vision_line.intersect(line_segment)

                if intersect_point:
                    find_intersect_point = True
                    dist = how_far(self.position, intersect_point) # BAD

                    if dist < min_dist:
                        min_dist = dist
                        min_point = intersect_point
                    else:
                        storage.append(intersect_point)

        if find_intersect_point:
            return min_point

        return False

    def draw_vision(self, surface, figures):
        x, y = self.position
        pygame.draw.circle(surface, black, (int(x), int(y)), 10, 1)
        intersect_point = robot.get_distance(figures)
        if intersect_point:
            pygame.draw.line(gameDisplay, red, robot.position, intersect_point, 1)
        else:
            pygame.draw.line(surface, green, self.position, self.tail, 1)


# LINE #


class Line:
    '''
    some SO code
    http://stackoverflow.com/questions/20677795/find-the-point-of-intersecting-lines
    http://stackoverflow.com/questions/328107/how-can-you-determine-a-point-is-between-two-other-points-on-a-line-segment
    '''
    def __init__(self, p1, p2):
        self.begin = p1
        self.end = p2

        self.A = (p1[1] - p2[1])
        self.B = (p2[0] - p1[0])
        self.C = (p1[0] * p2[1] - p2[0] * p1[1])

    def intersect(self, line):
        def is_between(a, b, c):
            cross_product = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])
            if abs(cross_product) > EPS:
                return False

            dot_product = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1])*(b[1] - a[1])
            if dot_product < 0:
                return False

            squared_lengthba = (b[0] - a[0])*(b[0] - a[0]) + (b[1] - a[1])*(b[1] - a[1])
            if dot_product > squared_lengthba:
                return False

            return True

        D = self.A * line.B - self.B * line.A
        Dx = -self.C * line.B - self.B * -line.C
        Dy = self.A * -line.C + self.C * line.A

        if abs(D) > 0:
            x = Dx / D
            y = Dy / D

            if is_between(line.begin, line.end, (x, y)) and \
                    is_between(self.begin, self.end, (x, y)):
                return x, y

        return False


#############################


if __name__ == '__main__':
    pygame.init()
    gameDisplay = pygame.display.set_mode(DISPLAY_RES)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(500, 25)
    text = pygame.font.SysFont("monospace", 15)

    figures = [Figure() for i in range(FIGURES_COUNT)]

    robot = Robot([DISPLAY_RES[0] / 2, DISPLAY_RES[1] / 2], 0)

    delta_alpha = 0
    stop = False
    while not stop:
        # EVENTS #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop = True

                if event.key == pygame.K_DOWN:
                    delta_alpha += 0.001
                if event.key == pygame.K_UP:
                    delta_alpha -= 0.001

                if event.key == pygame.K_w:
                    robot.move(0, -5)
                if event.key == pygame.K_s:
                    robot.move(0, 5)
                if event.key == pygame.K_a:
                    robot.move(-5, 0)
                if event.key == pygame.K_d:
                    robot.move(5, 0)

        # DRAW #
        gameDisplay.fill(white)

        label = text.render('da: ' + str(round(delta_alpha, 4)), 1, black)
        gameDisplay.blit(label, (10, 10))

        robot.draw_vision(gameDisplay, figures)

        for figure in figures:
            figure.draw(gameDisplay)

        # UPDATE #

        pygame.display.update()
        clock.tick(FPS)
        robot.update(delta_alpha)
        pygame.display.set_caption('FPS: ' + str(int(clock.get_fps())))

    pygame.quit()
