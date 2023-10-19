import pygame
import sys
from utils import *


class BoxSlide:
    def __init__(self, inclination: float, box_mass= 1, fric_coeff = 0.5, gravity = 0.0009) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))
        self.length = 300  # length of the inclined plane
        self.box_mass = box_mass
        self.inclination = radians(inclination)
        self.coeff = fric_coeff
        self.gravity = gravity
        self.boxsize = 50
        self.box_pos = None
        self.box_vel = 0
        self.box_acc = None
        self.hinge = (350, 350)
        self.prev_box_points = None
        self.prev_box_pos = None
        self.main_run = False
        self.start_point = None
        self.graph_start_coord = (550, 100)
        self.graph_x_coord = 550
        self.kinetic_energy = 0.5*self.box_mass*(self.box_vel**2)
        height = 0
        self.potential_energy = self.box_mass*self.gravity*height

    def create_environment(self, surface):
        
        self.screen.fill((0,0,0))
        # plane
        self.start_point = (self.hinge[0] - self.length*cos(self.inclination), self.hinge[1] - self.length*(sin(self.inclination)))
        pygame.draw.polygon(surface, (150, 150, 150), points=[self.start_point, self.hinge, (self.start_point[0], self.hinge[1])])

        #box
        if self.box_pos is None:
            self.box_pos = self.start_point
        
        self.box_points = generate_box_points(self.box_pos, self.inclination, self.boxsize)
       
        pygame.draw.polygon(surface, (255, 255, 255), points=[self.box_pos, self.box_points[1], self.box_points[2], self.box_points[3]])
        

    def update_position(self):
        
        if not self.main_run:
            a_g = self.gravity*sin(self.inclination)
            a_f = -self.coeff*self.gravity*sin(self.inclination)

            self.box_acc = a_g + a_f
            self.box_vel += self.box_acc

            self.box_pos = (self.box_pos[0] + self.box_vel*cos(self.inclination), self.box_pos[1] + self.box_vel*sin(self.inclination))
            

    def stats(self):
        
        size = 200

        #grids
        for i in range(self.graph_start_coord[0], self.graph_start_coord[0]+size+1, 20):
            pygame.draw.line(self.screen, (50, 50, 50), (i, self.graph_start_coord[1]), (i, self.graph_start_coord[1]+size))
        
        for i in range(self.graph_start_coord[1], self.graph_start_coord[1]+size, 20):
            pygame.draw.line(self.screen, (50, 50, 50), (self.graph_start_coord[0], i), (self.graph_start_coord[0]+size, i))

        #axis
        '''pygame.draw.line(self.screen, (140, 140, 140), ((2*self.graph_start_coord[0]+size)/2, self.graph_start_coord[1]), ((2*self.graph_start_coord[0]+size)/2, self.graph_start_coord[1]+size))
        pygame.draw.line(self.screen, (140, 140, 140), (self.graph_start_coord[0], (2*self.graph_start_coord[1]+size)/2), (self.graph_start_coord[0]+size, (2*self.graph_start_coord[1]+size)/2))'''

        height = (self.hinge[1] - self.box_pos[1])
        self.kinetic_energy = 0.5*self.box_mass*(self.box_vel**2)
        self.potential_energy = self.box_mass*self.gravity*height
        
        potential_y_coord = self.graph_start_coord[1]+size-20 - self.potential_energy*1000
        kinetic_y_coord = self.graph_start_coord[1]+size-20 - self.kinetic_energy*1000

        total_energy_coord = self.graph_start_coord[1]+size-20 -(self.kinetic_energy + self.potential_energy)*1000

        pygame.draw.circle(self.screen, (255, 0, 0), [self.graph_x_coord, potential_y_coord], radius=1)
        pygame.draw.circle(self.screen, (0, 0, 255), [self.graph_x_coord, kinetic_y_coord], radius=1)
        pygame.draw.circle(self.screen, (0, 255, 0), [self.graph_x_coord, total_energy_coord], radius=1)

        self.graph_x_coord += 0.1

        #container
        pygame.draw.rect(self.screen, (200, 200, 200), rect=pygame.Rect(self.graph_start_coord[0], self.graph_start_coord[1], size, size), border_radius=4, width=2)

    def keep_alive(self):
        while True:

            self.create_environment(surface=self.screen)

            if self.box_points[3][0] <= self.hinge[0]:
                self.update_position()
                print(round(self.kinetic_energy, 3), round(self.potential_energy, 3), round(self.kinetic_energy, 3) + round(self.potential_energy))
                self.stats()

            else:
                self.main_run = True

            if self.main_run:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.main_run = False
                        pygame.draw.polygon(self.screen, (0, 0, 0), points=[self.box_points[0], self.box_points[1], self.box_points[2], self.box_points[3]])
                        self.box_pos = self.start_point
                        self.box_vel = 0

                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            
            pygame.display.update()

dabba = BoxSlide(inclination=30)
dabba.keep_alive()