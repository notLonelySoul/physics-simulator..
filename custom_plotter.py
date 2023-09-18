import pygame
import math


class CustomPlotter:
    def __init__(self, box_top_point, box_left_point, size=200) -> None:
        self.box_top_point = box_top_point
        self.box_left_point = box_left_point
        self.size = size

    def set_plane(self, surface):
        for i in range(self.box_left_point, self.box_left_point+self.size+1, 20):
            pygame.draw.line(surface, (50, 50, 50), (i, self.box_top_point), (i, self.box_top_point+self.size))
        
        for i in range(self.box_top_point, self.box_top_point+self.size, 20):
            pygame.draw.line(surface, (50, 50, 50), (self.box_left_point, i), (self.box_left_point+self.size, i))

         #axis
        pygame.draw.line(surface, (140, 140, 140), ((2*self.box_left_point+self.size)/2, self.box_top_point ), ((2*self.box_left_point+self.size)/2, self.box_top_point +self.size))

        pygame.draw.line(surface, (140, 140, 140), (self.box_left_point, (2*self.box_top_point +self.size)/2), (self.box_left_point+self.size, (2*self.box_top_point +self.size)/2))

        #container
        pygame.draw.rect(surface, (200, 200, 200), rect=pygame.Rect(self.box_left_point, self.box_top_point , self.size, self.size), border_radius=4, width=2)

