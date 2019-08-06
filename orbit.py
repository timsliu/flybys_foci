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

from astro_constants import *


# TODO - generalize to calc_orbital_height
# for burns at perihelion OR aphelion to calculate the 
# next perihelion/aphelion
def calc_perihelion(dv1, r0, v0):
    '''helper function for calc_vi. Calculates the perihelion
    and velocity at perihelion
    inputs: dv1 - delta v from first burn
            r0 - starting distance from the sun
            v0 - starting velocity'''
    a = (2/r0 - ((v0-dv1) ** 2)/G/M_S) ** -1  # calculate semi-major axis
    rp = 2*a - r0                             # calculate perihelion distance
    vp = r0 *(v0 - dv1)/rp                    # calculate velocity at perihelion

    return rp, vp                           # return perihelion and velocity

# TODO - generalize to calc_dv() but allow prograde
# or retrograde burns
def calc_dv(rp, r0, v0):
    '''calculate delta v to reach a given perihelion
    inputs: rp - desired perihelion
            r0 - starting radius
            v0 - starting velocity'''

    # calculate semi-major axis
    a = (rp + r0)/2   
    # calculate dv; rearrangement of vis-viva equation
    dv = v0 - math.sqrt(-1* (1/a - 2/r0) * G * M_S)

    return dv


# TODO update to apply to points other than periapsis - 
# will need to update documentation
def calc_dv_escape(v_inf, vp, rp, m):
    '''calculates the delta v necessary to reach a given v_infinity
    based on the periapsis velocity, periapsis radial distance, and
    mass of parent body
    inputs: v_inf - desired v_inf (set to 0 to calculate escape velocity)
            vp - velocity at periapsis
            rp - periapsis distance
            m - mass of parent body
    outputs: dv - delta v needed for given v_infinity'''

    pe = -1*m*G/rp             # potential energy
    dv = (v_inf**2 - 2*pe)**0.5 - vp

    return dv

# change to calc_velocity_1 - calculating velocity based on 
# 3 inputs
def calc_v_1(a, r, m):
    '''calculates the velocity of an object in orbit based on the
    semi major axis, the distance from object to parent body, and
    mass of parent body
    inputs: a - semimajor axis (m)
            r - distance from object to parent body (m)
            m - mass of parent body (kg)
    outputs: v - object velocity (m/s)'''

    # calculate specific orbital energy
    soe = -1 * m * G / 2 / a
    v = (2 * (soe + m * G / r))**0.5

    return v

# change to calc_velocity_2 - calculating velocity based
# on different inputs
# TODO - generalize for different parent bodies
def calc_v_2(v0, r0, rf):
    '''calculates the final velocity vf of a spacecraft by
    conservation of energy
    inputs: v0 - initial velocity
            r0 - initial distance from parent body
            rf - final distance from parent body'''
            
    # calculate C3 - kinetic energy plus potential energy per mass
    C3 = 0.5 * v0 **2 - M_S * G / r0
    # calculate vf - C3 is unchanged
    vf = (2 * (C3 + M_S * G /rf)) ** 0.5
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
