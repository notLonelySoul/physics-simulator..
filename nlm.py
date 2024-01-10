import pygame
import sys
from math import *
from utils import *


class BoxSlide:
    def __init__(self, inclination: float, box_mass= 1, fric_coeff=0.5, gravity=0.0009) -> None:
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
        self.run = True
        self.start_point = None
        self.graph_start_coord = (550, 100)
        self.graph_x_coord = 552
        self.kinetic_energy = 0.5*self.box_mass*(self.box_vel**2)
        height = 0
        self.potential_energy = self.box_mass*self.gravity*height
        self.edit = False
        self.start_point = (self.hinge[0] - self.length*cos(self.inclination), self.hinge[1] - self.length*(sin(self.inclination)))
        self.lamb = 170/(self.box_mass*self.gravity*(self.hinge[1]-self.start_point[1])*1000)


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
        
        if self.run:
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


        height = (self.hinge[1] - self.box_pos[1])
        self.kinetic_energy = 0.5*self.box_mass*(self.box_vel**2)
        self.potential_energy = self.box_mass*self.gravity*height
    
        potential_y_coord = self.graph_start_coord[1]+size-20 - self.lamb*self.potential_energy*1000
        kinetic_y_coord = self.graph_start_coord[1]+size-20 - self.lamb*self.kinetic_energy*1000

        total_energy_coord = self.graph_start_coord[1]+size-20 - self.lamb*(self.kinetic_energy + self.potential_energy)*1000

        pygame.draw.circle(self.screen, (255, 0, 0), [self.graph_x_coord, potential_y_coord], radius=1)
        pygame.draw.circle(self.screen, (0, 0, 255), [self.graph_x_coord, kinetic_y_coord], radius=1)
        pygame.draw.circle(self.screen, (0, 255, 0), [self.graph_x_coord, total_energy_coord], radius=1)

        if self.inclination > radians(10) and self.coeff > 1:
            self.graph_x_coord += 0.1*(self.inclination/(pi/6))*(1 - self.coeff)
        elif self.inclination < radians(10):
            self.graph_x_coord += 0.1*(self.inclination/(pi/20))
        else:
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
                self.stats()

            else:
                self.run = False

            if not self.run:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        xp, yp = event.pos 

                        c = ((self.box_pos[0] + self.boxsize/sqrt(2)), self.box_pos[1])

                        if (xp - c[0])**2 + (yp - c[1])**2 <= (self.boxsize)**2 /2:
                            self.edit = True
                            
                            while self.edit: 

                                for event1 in pygame.event.get():
                                    if event1.type == pygame.MOUSEBUTTONUP:
                                        x = event1.pos[0]
                                        if x < self.start_point[0]:
                                            x = self.start_point[0]
                                        elif x+ self.boxsize*cos(self.inclination) > self.hinge[0]:
                                            x = self.hinge[0]-self.boxsize*cos(self.inclination)
                                        y = get_point_on_plane(self.start_point, self.hinge, x)
                                        self.run = True
                                        pygame.draw.polygon(self.screen, (0, 0, 0), points=[self.box_points[0], self.box_points[1], self.box_points[2], self.box_points[3]])
                                        self.box_pos = (x, y)
                                        self.box_vel = 0
                                        self.graph_x_coord = 550
                                        self.edit = False


                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

class Pendulum:
    def __init__(self, theta: float, ball_mass= 1, gravity = 0.0009, rope_length: float = 1) -> None:
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
        self.prev_ang_vel = 0
        self.kinetic_energy = 0.5*self.mass*((self.ang_bal_vel*self.rope_length)**2)
        height = 0
        self.potential_energy = self.mass*self.gravity*height
        self.lamb = 150/(self.mass*self.rope_length*self.gravity*1000)
        self.edit = False

    def create_environment(self):
        ceiling_points = [(100, 50), (350, 50)]
        self.joint = ((ceiling_points[0][0] + ceiling_points[1][0])/2, ceiling_points[0][1])
        
        self.init_pos = (self.joint[0] + self.rope_length*sin(self.init_theta), self.joint[1] + self.rope_length*cos(self.init_theta))

        pygame.draw.line(self.screen, (255, 255, 255), ceiling_points[0], ceiling_points[1], width=5)

    def update_position(self):
        
        if not self.edit:
            self.ang_bal_acc = -self.gravity*sin(self.inst_theta)/self.rope_length
            self.prev_ang_vel = self.ang_bal_vel
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
        pygame.draw.line(self.screen, (140, 140, 140), ((2*self.graph_start_coord[0]+size)/2, self.graph_start_coord[1]), ((2*self.graph_start_coord[0]+size)/2, self.graph_start_coord[1]+size), width=1)
        pygame.draw.line(self.screen, (140, 140, 140), (self.graph_start_coord[0], self.graph_start_coord[1]+size-40), (self.graph_start_coord[0]+size, self.graph_start_coord[1]+size-40), width=1)

        prev_graph_x_coord = self.graph_start_coord[0] -10 + (self.joint[0]+(self.prev_ball_pos[0]-self.joint[0]))/2

        # current stats
        height = self.rope_length-(self.ball_pos[1]-self.joint[1])
        self.potential_energy = self.mass * self.gravity * height
        self.kinetic_energy = 0.5 * self.mass * self.rope_length**2 * self.ang_bal_vel**2
        
        potential_y_coord = self.graph_start_coord[1]+size-40 - self.lamb*round(self.potential_energy, 4)*1000
        kinetic_y_coord = self.graph_start_coord[1]+size-40 - self.lamb*round(self.kinetic_energy, 4)*1000

        total_energy_coord = self.graph_start_coord[1]+size-40 - self.lamb*(round(self.kinetic_energy, 4) + round(self.potential_energy, 4))*1000
        self.graph_x_coord = self.graph_start_coord[0] -10 + (self.joint[0]+(self.ball_pos[0]-self.joint[0]))/2

        pygame.draw.circle(self.screen, (255, 0, 0), [self.graph_x_coord, potential_y_coord], radius=1.8)
        pygame.draw.circle(self.screen, (0, 0, 255), [self.graph_x_coord, kinetic_y_coord], radius=1.8)
        pygame.draw.circle(self.screen, (0, 255, 255), [self.graph_x_coord, total_energy_coord], radius=1.8)

        #container
        pygame.draw.rect(self.screen, (200, 200, 200), rect=pygame.Rect(self.graph_start_coord[0], self.graph_start_coord[1], size, size), border_radius=4, width=2)

        # pendulum-position-indicator.
        pygame.draw.circle(self.screen, (0, 0, 0), (prev_graph_x_coord, self.graph_start_coord[1]+size+40), radius=5)
        pygame.draw.line(self.screen, (100, 100, 100), (self.graph_start_coord[0], self.graph_start_coord[1]+size+40), (self.graph_start_coord[0]+size, self.graph_start_coord[1]+size+40))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.graph_x_coord, self.graph_start_coord[1]+size+40),radius=5)

    def keep_alive(self):
        while True:
            
            if self.prev_ball_pos is not None:
                pygame.draw.line(self.screen, (0, 0, 0), self.joint, self.prev_ball_pos, width=2)
                pygame.draw.circle(self.screen, (0, 0, 0), center=self.prev_ball_pos, radius=15)

            self.create_environment()
            self.update_position()
            self.stats()                
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x1,y1 = event.pos

                    if sqrt((x1-self.ball_pos[0])**2 + (y1 - self.ball_pos[1])**2) <= 15:
                        self.edit = True 
                    
                        while self.edit:
                            for event1 in pygame.event.get():
                                if event1.type == pygame.MOUSEBUTTONUP:
                                    x = event1.pos[0]

                                    if x > 225 + self.rope_length*sin(self.init_theta):
                                        x = 225 + self.rope_length*sin(self.init_theta)
                                    elif x < 225 - self.rope_length*sin(self.init_theta):
                                        x = 225 - self.rope_length*sin(self.init_theta)

                                    t = asin((x - 225)/self.rope_length)
                                    self.ang_bal_vel = 0
                                    self.inst_theta = t
                                    self.edit = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


class Spring:
    def __init__(self, spring_constant: float, box_mass= 1, fric_coeff=0, gravity=0.0009, amplitude=3) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))

        self.box_mass = box_mass
        self.fric_coeff = fric_coeff
        self.gravity = gravity
        self.k = spring_constant
        
        self.length = 300  # length of the plane
        self.boxsize = 50
        self.box_pos = None
        self.v = 0
        self.a = None
        self.hinge = (350, 350)
        self.main_run = False
        self.start_point = None
        self.slength = 50
        self.graph_start_coord = (550, 100)
        self.graph_x_coord = 550
        self.kinetic_energy = 0.5*self.box_mass*(self.v**2)
        self.amplitude = amplitude
        self.x = amplitude*10
        self.potential_energy = 0.5*self.k*(self.x/100)**2
        self.lamb = 500/(0.5*self.k*(amplitude*10)**2)
        self.edit = False
        self.init_pos = (self.hinge[0]-self.length+120-self.x, self.hinge[1])

    def create_environment_1(self):
        
        screenpoints = generate_box_points((40, 400), 0, 300)
        pygame.draw.polygon(self.screen, (0, 0, 0), screenpoints)

        miniscpts = generate_rectangle_points((self.graph_x_coord-10, self.graph_start_coord[1]+300), 0, 90, 220)
        pygame.draw.polygon(self.screen, (0, 0, 0), miniscpts)

        # rectangle
        self.box_pos = (self.hinge[0]-self.length+120-self.x, self.hinge[1])
        box_points = generate_box_points(self.box_pos, 0, self.boxsize)

        wallstart = (self.hinge[0]-self.length, self.hinge[1])
        wallpoints = generate_rectangle_points(wallstart, 0, self.boxsize, 10)

        pygame.draw.polygon(self.screen, (255, 255, 255), box_points)
        pygame.draw.polygon(self.screen, (150, 150, 150), wallpoints)

        pygame.draw.line(self.screen, (150, 150, 150), (self.hinge[0]-self.length, self.hinge[1]), (self.hinge[0], self.hinge[1]), width=4)

        springstart = (wallstart[0]+10, wallstart[1]-self.boxsize/2)
        springend =  (self.box_pos[0], self.box_pos[1]-self.boxsize/2)

        pygame.draw.line(self.screen, (50, 50, 50), springstart, springend)
        pygame.draw.circle(self.screen, (100, 100, 100), springstart, radius=2)
        pygame.draw.circle(self.screen, (100, 100, 100), springend, radius=2)

    def update_movement(self):
        if not self.edit:
            self.a = -(self.k*self.x/self.box_mass)*0.000100
            self.v += self.a
            self.x += self.v

    def stats(self):
        
        size = 200

        # grids
        for i in range(self.graph_start_coord[0], self.graph_start_coord[0]+size+1, 20):
            pygame.draw.line(self.screen, (50, 50, 50), (i, self.graph_start_coord[1]), (i, self.graph_start_coord[1]+size))

        for i in range(self.graph_start_coord[1], self.graph_start_coord[1]+size, 20):
            pygame.draw.line(self.screen, (50, 50, 50), (self.graph_start_coord[0], i), (self.graph_start_coord[0]+size, i))

        # axis
        pygame.draw.line(self.screen, (140, 140, 140), ((2*self.graph_start_coord[0]+size)/2, self.graph_start_coord[1]), ((2*self.graph_start_coord[0]+size)/2, self.graph_start_coord[1]+size), width=1)
        pygame.draw.line(self.screen, (140, 140, 140), (self.graph_start_coord[0], self.graph_start_coord[1]+size-40), (self.graph_start_coord[0]+size, self.graph_start_coord[1]+size-40), width=1)

        # current stats
        self.kinetic_energy = 0.5*self.box_mass*(self.v**2)
        self.potential_energy = 0.5*self.k*(self.x/100)**2

        potential_y_coord = self.graph_start_coord[1]+size-40 - self.lamb*self.potential_energy*1000
        kinetic_y_coord = self.graph_start_coord[1]+size-40 - self.lamb*self.kinetic_energy*1000

        total_energy_coord = self.graph_start_coord[1]+size-40 - self.lamb*(self.kinetic_energy*1000 + self.potential_energy*1000)
        self.graph_x_coord = self.graph_start_coord[0] + size/2 - (self.x)/1.5

        pygame.draw.circle(self.screen, (255, 0, 0), [self.graph_x_coord, potential_y_coord], radius=1.4)
        pygame.draw.circle(self.screen, (0, 0, 255), [self.graph_x_coord, kinetic_y_coord], radius=1.4)
        pygame.draw.circle(self.screen, (0, 255, 0), [self.graph_x_coord, total_energy_coord], radius=1.4)

        # container
        pygame.draw.rect(self.screen, (200, 200, 200), rect=pygame.Rect(self.graph_start_coord[0], self.graph_start_coord[1], size, size), border_radius=4, width=2)

        # pendulum-position-indicator.
        pygame.draw.line(self.screen, (100, 100, 100), (self.graph_start_coord[0], self.graph_start_coord[1]+size+40), (self.graph_start_coord[0]+size, self.graph_start_coord[1]+size+40))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.graph_x_coord, self.graph_start_coord[1]+size+40),radius=5)

    def keep_alive(self):
        while True:

            self.create_environment_1()
            self.update_movement()
            self.stats()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
