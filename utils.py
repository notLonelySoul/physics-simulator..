from math import *
import pickle

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

def show_history():

    with open('simulation.hist', 'rb') as f:
        try: 
            hist = pickle.load(f)
            # convert into reaadable format            
            out = [] 
            for i in hist:
                if i[0] == "Box Slide":
                    s = f"{i[0]} :  Mass = {i[1][0]}, Friction coefficient = {i[1][1]}, Inclination = {i[1][2]}"

                elif i[0] == "Pendulum":
                    s = f"{i[0]} :  Angluar Amplitude = {i[1][0]}, Ball mass = {i[1][1]}, Rope length = {i[1][2]}"

                elif i[0] == "Spring":
                    s = f"{i[0]} :  Spring Constant = {i[1][0]}, Box mass = {i[1][1]}, Amplitude = {i[1][2]}"
                
                out.append(s)
            
            print("\nHISTORY:\n")

            for i in enumerate(out, start=1):
                print(f"{i[0]}) {i[1]}")
        
        except EOFError:
            print("No history.")
            
def print_info():
    print("\nGraph-info:\n[Red] : Potential energy\n[Blue] : Kinetic energy\n[Green] : Total energy.")
    
    
    