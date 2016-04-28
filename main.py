import pygame
from robot import Robot
from figure import Figure
from settings_storage import settings

SETTINGS_FILE = 'settings_\\test_settings'


class Environment:
    def __init__(self):
        self.settings = settings
        self.settings.load(SETTINGS_FILE)

        pygame.init()
        pygame.key.set_repeat(500, 25)

        self.surface = pygame.display.set_mode(settings.DISPLAY_RES)
        self.clock = pygame.time.Clock()
        self.text = pygame.font.SysFont("monospace", 15)

        self.figures = [Figure(pygame, i, self.surface, False) for i in range(settings.FIGURES_COUNT)]
        self.robot = Robot(pygame, self.surface, settings.SPAWN_POINT, 0)

    def save(self):
        pass

    def load(self):
        pass



    def run(self):
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
                        self.robot.move(0, -5)
                    if event.key == pygame.K_s:
                        self.robot.move(0, 5)
                    if event.key == pygame.K_a:
                        self.robot.move(-5, 0)
                    if event.key == pygame.K_d:
                        self.robot.move(5, 0)

            # DRAW #
            self.surface.fill(settings.white)

            label = self.text.render('da: ' + str(round(delta_alpha, 4)), 1, settings.black)
            self.surface.blit(label, (10, 10))

            self.robot.draw_vision(self.figures)

            for figure in self.figures:
                figure.draw()

            # UPDATE #

            pygame.display.update()
            self.clock.tick(settings.FPS)
            self.robot.update(delta_alpha)
            pygame.display.set_caption('FPS: ' + str(int(self.clock.get_fps())))

        for f in self.figures:
            f.save()

        pygame.quit()


if __name__ == '__main__':
    env = Environment()
    env.run()
