import pymunk
import pymunk.pygame_util
import pygame
import sys
from math import *
from utils import *


class BoxSlide:
    def __init__(self, inclination: float, box_mass= 1, fric_coeff = 0.5, gravity = 0.0009) -> None:
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
        
        # plane
        self.start_point = (self.hinge[0] - self.length*cos(self.inclination), self.hinge[1] - self.length*(sin(self.inclination)))
        pygame.draw.polygon(surface, (150, 150, 150), points=[self.start_point, self.hinge, (self.start_point[0], self.hinge[1])])

        #box
        if self.box_pos is None:
            self.box_pos = self.start_point
        
        self.box_points = generate_box_points(self.box_pos, self.inclination, self.boxsize)
        
        if self.prev_box_pos is not None:
            self.prev_box_points = generate_box_points(self.prev_box_pos, self.inclination, self.boxsize)

        
        pygame.draw.polygon(surface, (255, 255, 255), points=[self.box_pos, self.box_points[1], self.box_points[2], self.box_points[3]])
        

    def update_position(self):
        
        if not self.main_run:
            a_g = self.gravity*sin(self.inclination)
            a_f = -self.coeff*self.gravity*sin(self.inclination)

            self.box_acc = a_g + a_f
            self.box_vel += self.box_acc

            self.prev_box_pos = self.box_pos

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

            if self.prev_box_points is not None:
                pygame.draw.polygon(self.screen, (0, 0, 0), points=[self.prev_box_points[0], self.prev_box_points[1], self.prev_box_points[2], self.prev_box_points[3]])

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


class Pendulum:
    def __init__(self, theta: float, ball_mass= 1, gravity = 0.0009, rope_length = 1) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))

        self.mass = ball_mass
        self.gravity = gravity
        self.joint = None
        self.init_theta = radians(theta)
        self.rope_length = rope_length*100
        self.prev_ball_pos = None
        self.init_pos = None
        self.ball_pos = None
        self.inst_theta = self.init_theta
        self.ang_bal_acc = self.gravity*self.inst_theta/self.rope_length
        self.ang_bal_vel = 0
        self.graph_start_coord = (550, 100)
        self.graph_x_coord = 550
        self.kinetic_energy = 0.5*self.mass*((self.ang_bal_vel*self.rope_length)**2)
        height = 0
        self.potential_energy = self.mass*self.gravity*height

    def create_environment(self):
        ceiling_points = [(100, 50), (350, 50)]
        self.joint = ((ceiling_points[0][0] + ceiling_points[1][0])/2, ceiling_points[0][1])
        
        self.init_pos = (self.joint[0] + self.rope_length*sin(self.init_theta), self.joint[1] + self.rope_length*cos(self.init_theta))

        pygame.draw.line(self.screen, (255, 255, 255), ceiling_points[0], ceiling_points[1], width=5)

    def update_position(self):
        
        self.ang_bal_acc = -self.gravity*self.inst_theta/self.rope_length
        self.ang_bal_vel += self.ang_bal_acc
        self.inst_theta += self.ang_bal_vel
        
        if self.ball_pos is None:
            self.prev_ball_pos = self.init_pos
        else:
            self.prev_ball_pos = self.ball_pos

        self.ball_pos = (self.joint[0] + self.rope_length*sin(self.inst_theta), self.joint[1] + self.rope_length*cos(self.inst_theta))

        pygame.draw.line(self.screen, (100, 100, 100), self.joint, self.ball_pos, width=2)
        pygame.draw.circle(self.screen, (255, 255, 255), center=self.ball_pos, radius=15)

    def stats(self):
        
        size = 200

        #grids
        for i in range(self.graph_start_coord[0], self.graph_start_coord[0]+size+1, 20):
            pygame.draw.line(self.screen, (50, 50, 50), (i, self.graph_start_coord[1]), (i, self.graph_start_coord[1]+size))

        for i in range(self.graph_start_coord[1], self.graph_start_coord[1]+size, 20):
            pygame.draw.line(self.screen, (50, 50, 50), (self.graph_start_coord[0], i), (self.graph_start_coord[0]+size, i))

        #axis
        pygame.draw.line(self.screen, (140, 140, 140), ((2*self.graph_start_coord[0]+size)/2, self.graph_start_coord[1]), ((2*self.graph_start_coord[0]+size)/2, self.graph_start_coord[1]+size))
        pygame.draw.line(self.screen, (140, 140, 140), (self.graph_start_coord[0], (2*self.graph_start_coord[1]+size)/2), (self.graph_start_coord[0]+size, (2*self.graph_start_coord[1]+size)/2))

        height = (self.rope_length-(self.ball_pos[1]-self.joint[1]))
        self.kinetic_energy = 0.5*self.mass*((self.ang_bal_vel*self.rope_length)**2)
        self.potential_energy = self.mass*self.gravity*height
        
        potential_y_coord = self.graph_start_coord[1]+size-40 - round(self.potential_energy, 4)*1000
        kinetic_y_coord = self.graph_start_coord[1]+size-40 - round(self.kinetic_energy, 4)*1000

        total_energy_coord = self.graph_start_coord[1]+size-40 -(round(self.kinetic_energy, 4) + round(self.potential_energy, 4))*1000
        self.graph_x_coord = self.graph_start_coord[0] -10 + (self.joint[0]+(self.ball_pos[0]-self.joint[0]))/2

        pygame.draw.circle(self.screen, (255, 0, 0), [self.graph_x_coord, potential_y_coord], radius=1)
        pygame.draw.circle(self.screen, (0, 0, 255), [self.graph_x_coord, kinetic_y_coord], radius=1)
        pygame.draw.circle(self.screen, (0, 255, 0), [self.graph_x_coord, total_energy_coord], radius=1)

        #container
        pygame.draw.rect(self.screen, (200, 200, 200), rect=pygame.Rect(self.graph_start_coord[0], self.graph_start_coord[1], size, size), border_radius=4, width=2)

    def keep_alive(self):
        while True:
            
            if self.prev_ball_pos is not None:
                pygame.draw.line(self.screen, (0, 0, 0), self.joint, self.prev_ball_pos, width=2)
                pygame.draw.circle(self.screen, (0, 0, 0), center=self.prev_ball_pos, radius=15)

            self.create_environment()
            self.update_position()
            self.stats()

            
                
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

pundu = Pendulum(theta=80, rope_length=1.5, gravity=0.0007)
pundu.keep_alive()