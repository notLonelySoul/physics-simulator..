import pymunk
import pymunk.pygame_util 
import pygame
import sys

class PlayGround:
    def __init__(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((640, 240))
        draw_options = pymunk.pygame_util.DrawOptions(screen)

    def add_objects(self):
        pass

    def keep_alive(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

