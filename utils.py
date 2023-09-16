from math import *

def generate_box_points(rp: tuple, inclination, boxsize):
    point1 = (rp[0] + boxsize*sin(inclination), rp[1] - boxsize*cos(inclination))
    point2 = (point1[0] + boxsize*cos(inclination), point1[1] + boxsize*sin(inclination))
    point3 = (point2[0] - boxsize*sin(inclination), point2[1] + boxsize*cos(inclination))

    return (rp, point1, point2, point3)
