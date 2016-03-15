import pygame
from constants import *
from figure import Figure
from robot import Robot


if __name__ == '__main__':
    pygame.init()
    gameDisplay = pygame.display.set_mode(DISPLAY_RES)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(500, 25)
    text = pygame.font.SysFont("monospace", 15)

    figures = [Figure(pygame) for i in range(FIGURES_COUNT)]

    robot = Robot(pygame, gameDisplay, [DISPLAY_RES[0] / 2, DISPLAY_RES[1] / 2], 0)

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
