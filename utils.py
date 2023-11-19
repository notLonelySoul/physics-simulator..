from math import *

def generate_box_points(rp: tuple, inclination: float, boxsize: float):
    point1 = (rp[0] + boxsize*sin(inclination), rp[1] - boxsize*cos(inclination))
    point2 = (point1[0] + boxsize*cos(inclination), point1[1] + boxsize*sin(inclination))
    point3 = (point2[0] - boxsize*sin(inclination), point2[1] + boxsize*cos(inclination))

    return (rp, point1, point2, point3)

def generate_rectangle_points(rp: tuple, inclination: float, boxsize: float, width: float):
    point1 = (rp[0] + boxsize*sin(inclination), rp[1] - boxsize*cos(inclination))
    point2 = (point1[0] + width*cos(inclination), point1[1] + width*sin(inclination))
    point3 = (point2[0] - boxsize*sin(inclination), point2[1] + boxsize*cos(inclination))

    return (rp, point1, point2, point3)

def get_point_on_plane(p1: tuple, p2: tuple, x: float):
    x1, y1 = p1
    x2, y2 = p2
    y = ((y2-y1)/(x2-x1))*(x - x1) + y1

    return y

def get_point_on_pend_locus(cp: tuple, r: float, x: float):
    y = cp[1] + sqrt(r**2 - (x - cp[0])**2)
    return y