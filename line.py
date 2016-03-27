from settings_storage import settings


class Line:
    '''
    Line class, implement math short line
    Класс, реализующий отрезок

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
            if abs(cross_product) > settings.EPS:
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
