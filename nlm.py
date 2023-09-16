import pymunk
import pymunk.pygame_util
import matplotlib
import pygame
import sys
from math import *
from utils import *

class BoxSlide:
    def __init__(self,inclination: float, box_mass= 1, fric_coeff = 0.5, gravity = 0.0009) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))
        draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.length = 300  # length of the inclined plane
        self.box_mass = box_mass
        self.inclination = radians(inclination)
        self.coeff = fric_coeff
        self.gravity = gravity
        self.boxsize = 50
        self.box_pos = None
        self.box_vel = 0
        self.box_acc = None
        self.hinge = (400, 350)
        self.prev_box_points = None
        self.prev_box_pos = None

    def create_environment(self, surface):
        
        # plane
        other_point = (self.hinge[0] - self.length*cos(self.inclination), self.hinge[1] - self.length*(sin(self.inclination)))
        pygame.draw.line(surface, (255, 255, 255), other_point, self.hinge)

        #box
        if self.box_pos is None:
            self.box_pos = other_point
        
        self.box_points = generate_box_points(self.box_pos, self.inclination, self.boxsize)
        
        if self.prev_box_pos is not None:
            self.prev_box_points = generate_box_points(self.prev_box_pos, self.inclination, self.boxsize)
    
        pygame.draw.polygon(surface, (255, 255, 255), points=[self.box_pos, self.box_points[1], self.box_points[2], self.box_points[3]])
        

    def update_position(self):

        a_g = self.gravity*sin(self.inclination)
        a_f = -self.coeff*self.gravity*sin(self.inclination)

        self.box_acc = a_g + a_f
        self.box_vel += self.box_acc

        self.prev_box_pos = self.box_pos

        self.box_pos = (self.box_pos[0] + self.box_vel*cos(self.inclination), self.box_pos[1] + self.box_vel*sin(self.inclination))

    def keep_alive(self):
        while True:
            if self.prev_box_points is not None:
                pygame.draw.polygon(self.screen, (0, 0, 0), points=[self.prev_box_points[0], self.prev_box_points[1], self.prev_box_points[2], self.prev_box_points[3]])

            self.create_environment(surface=self.screen)

            if self.box_points[3][0] <= self.hinge[0]:
                self.update_position()
            else:
                print(self.box_vel)
                break
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

boxslide = BoxSlide(inclination=60, fric_coeff=0)
boxslide.keep_alive()