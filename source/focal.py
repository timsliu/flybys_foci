# focal.py
#
# This program is used to calculate the sun's focal length
# as a function of how close light passes to the sun
#
# Table of contents
#
# Revision history
# 03/18/19    Tim Liu    created file; began writing documentation
# 03/18/19    Tim Liu    wrote calc_foci
# 03/18/19    Tim Liu 


import math
import matplotlib.pyplot as plt
import os
import numpy as np

HOME = os.getcwd()

# import astronomical constants
from astro_constants import *

def calc_foci(r):
    '''calculates the focal distance based on r, the distance
    light passes from the sun
    inputs: r - distance from the sun of the passing light'''

    theta = 4 * G * M_S/C**2/r    # angle of deflection
    f_d = r * math.tan(math.pi/2-theta)     # focal distance in meters

    return f_d/AU                 # return focal distance in AU

def plot_foci(r_max):
    '''plots the focal distance from the sun as a function
    of r. Plots from r = radius of sun to r_max
    inputs: r_max - maximum distance from the sun of the passing light
                    in solar radii; must be greater than 1'''

    assert(r_max > 1)
    r_array = np.linspace(1, r_max, num = 25)
    f_d_array = [calc_foci(r * R_S) for r in r_array]

    # set up graph
    plt.xlabel("Distance between deflected light and sun (solar radii)")
    plt.ylabel("Focal distance (AU)")
    plt.title("Focal distance of light deflected by sun")
    plt.grid(True)
    plt.plot(r_array, f_d_array)

    # go to graph directory and save
    os.chdir(HOME + "/../graphs")
    plt.savefig("fd_" + str(r_max) + "R_S.png", format="png", dpi = 800)
    plt.close()
    os.chdir(HOME)


    return
