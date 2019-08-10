# orbit.py
#
# library of equations for calculating orbital parameters
#
# Table of contents
# calc_exhaust_velocity - calculates the exhausts velocity from a particle's
#                         energy and mass
# calc_flight_time - calculates the flight time of Einstein
#
# Revision history
# 04/??/19    Tim Liu    copied equations from oberth.py
# 06/26/19    Tim Liu    moved calc_velocity from flight_time.py 
# 07/02/19    Tim Liu    fixed calc_v2 to return v2
# 08/09/19    Tim Liu    generalized calc_perihelion to calc_orbital_height
# 08/09/19    Tim Liu    updated calc_dv_escape to handle starting at 
# 08/09/19    Tim Liu    tested calc_v_1
# 08/10/19    Tim Liu    updated calc_v_2 to handle any parent body mass and tested

from astro_constants import *
import math


def calc_orbital_height(dv1, r0, v0, M  = M_S):
    '''Calcuates the opposite apsis height and velocity following
    a burn given the current orbital height (must be at an apsis), the
    current velocity, and magnitude of burn. All units MUST be passed
    as MKS. If the body escapes then r_op and v_op will both be returned
    as zero.

    function tested 08/09/19

    inputs: dv1 - delta v from burn; positive denotes prograde
                  burn and negative is retrograde burn
            r0 - starting distance from the parent body
            v0 - starting velocity
            m - parent body mass; default to the sun'''
    a = (2/r0 - ((v0+dv1) ** 2)/G/M) ** -1    # calculate semi-major axis
    r_op = 2*a - r0                           # calculate opposite apsis distance
    v_op = r0 *(v0+dv1)/r_op                  # calculate velocity at perihelion

    if dv1 + v0 > math.sqrt(2 * M * G / r0):  # body exceeds escape velocity
        v_op = 0
        r_op = 0
        print("calc_orbital_height: object escaped")


    return r_op, v_op                         # return perihelion and velocity


def calc_dv(rf, r0, v0, m = M_S):
    '''calculate delta v to reach a given orbital height. Must start
    and end at an apsis. All units MUST be passed as MKS

    # function tested 08/09/19

    inputs: rf - desired final orbital height (apsis)
            r0 - starting orbital height
            v0 - starting velocity
            m -  mass of parent body; defaults to sun'''

    # calculate semi-major axis
    a = (rf + r0)/2   
    # calculate dv; rearrangement of vis-viva equation
    dv = math.sqrt(-1* (1/a - 2/r0) * G * m) - v0

    return dv



def calc_dv_escape(v_inf, v0, r0, m = M_S):
    '''calculates the delta v necessary to reach a given v_infinity
    based on the current velocity, radial distance, and
    mass of parent body

    # function tested 08/09/19

    inputs: v_inf - desired v_inf (set to 0 to calculate escape velocity)
            vp - velocity at periapsis
            rp - periapsis distance
            m - mass of parent body
    outputs: dv - delta v needed for given v_infinity'''

    pe = -1 * m * G/r0                # potential energy
    dv = (v_inf**2 - 2*pe)**0.5 - v0  # delta-v necessary

    return dv


def calc_v_1(a, r, m = M_S):
    '''calculates the velocity of an object in orbit based on the
    semi major axis, the distance from object to parent body, and
    mass of parent body

    # function tested 08/09/19

    inputs: a - semimajor axis (m)
            r - distance from object to parent body (m)
            m - mass of parent body (kg)
    outputs: v - object velocity (m/s)'''

    # calculate specific orbital energy
    soe = -1 * m * G / 2 / a
    v = (2 * (soe + m * G / r))**0.5

    return v

def calc_v_2(v0, r0, rf, m = M_S):
    '''calculates the velocity vf of a spacecraft by
    conservation of energy given its current radial distance
    and velocity. Inputs must be in MKS units.
    inputs: v0 - initial velocity
            r0 - initial distance from parent body
            rf - final distance from parent body
            m - mass of parent body'''
            
    # calculate C3 - kinetic energy plus potential energy per mass
    C3 = 0.5 * v0 **2 - m * G / r0
    # calculate vf - C3 is unchanged
    vf = (2 * (C3 + m * G /rf)) ** 0.5
    return vf

def calc_exhaust_velocity(mass, energy_ev):
    '''calculates the exhaust velocity of a particle
    inputs: mass - mass of the particle
            energy - kinetic energy of the particle in MeV
    outputs: ve - exhaust velocity in meters per second'''

    energy_ev *= EV_PER_MEV                 # convert MeV to EV

    energy_j = energy_ev * J_PER_EV         # convert energy to joules
    velocity = math.sqrt(2 * energy_j/mass) # calculate velocity in m/s
    return velocity
