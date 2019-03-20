# flight_time.py
#
# program for calculating the flight time to the focal point
#
# Table of contents
# calc_exhaust_velocity - calculates the exhausts velocity from a particle's
#                         energy and mass
# calc_flight_time - calculates the flight time of Einstein
#
# Revision history
# 03/19/19    Tim Liu    created file and wrote calc_exhaust_velocity 
#

from astro_constants import *

import math

def calc_exhaust_velocity(mass, energy_ev):
    '''calculates the exhaust velocity of a particle
    inputs: mass - mass of the particle
            energy - kinetic energy of the particle in MeV
    outputs: ve - exhaust velocity in meters per second'''

    energy_ev *= 1000000                    # convert MeV to EV

    energy_j = energy_ev * J_PER_EV         # convert energy to joules
    velocity = math.sqrt(2 * energy_j/mass) # calculate velocity in m/s
    return velocity


# TODO
def calc_flight_time():
    '''calculates the flight time through numerical integration'''

    return
