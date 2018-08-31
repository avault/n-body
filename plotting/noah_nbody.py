# -*- coding: utf-8 -*-

import numpy as np

def calculate_force(m1, m2, pos1, pos2, G):
    #Distance between two particles
    r = np.sqrt((((pos2[0]-pos1[0])*(pos2[0]-pos1[0]))+((pos2[1]-pos1[1])*(pos2[1]-pos1[1]))))
    
    #Force of gravity
    Fg = (G*m1*m2)/r
    
    #Components
    theta = np.arctan(((pos2[1]-pos1[1])/((pos2[1]-pos1[1]))))
    Fx = Fg*np.cos(theta)
    Fy = Fg*np.sin(theta)
    
    return Fx
    return Fy
    
import n_body_checks
n_body_checks.plot_force_of_gravity(calculate_force)

    
