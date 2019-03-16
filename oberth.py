# oberth.py
# program for calculating hyperbolic excess velocity under
# different mission profiles and plotting Einstein's trajectory
#
# Note - consider splitting several files into helper 
# "orbit.py" library

# Revision History
# 03/10/19    Tim Liu    started file; wrote main and skeleton functions
# 03/12/19    Tim Liu    wrote main_two_burns and several helper functions
# 03/13/19    Tim Liu    wrote calc_dv and table of contents


# Table of Contents
# one_burn - main function to calculate v_infinity from one burn
# two_burns - main function to calculate v_infinity from two burns
# calc_vi - calculates v_infinity for a two burn manuever
# calc_peri - calculates the perihelion after one retrograde burn
# calc_dv - calcuates the delta v of a retrograde burn that will result
#           in a given perihelion
# plot_vi - plots v_infinities for a two burn manuever

import math
import numpy as np


# constants

G = 6.674e-11                         # universal gravity constant in MKS
M_S = 1.99e30                         # mass of the sun in kilogram
AU = 1.496e11                         # astronomical unit in meters
JUPITER_R = 5 * AU                    # approximate Jupiter's distance from sun in meters (5AU)
JUPITER_V = (G*M_S/JUPITER_R) ** 0.5  # approximate orbital velocity of Jupiter
MIN_R = 0.1 * AU                      # closest approach to sun allowed
                                      # Parker Solar Probe MIN_R ~0.05 AU
DV_STEP = 50                          # delta_v increment between calculated combinations in m/s


def one_burn(max_dv):
    '''calculates the hyperbolic escape velocity from single
    prograde burn '''


    # TODO

    return


def two_burns(max_dv2, r0 = JUPITER_R, v0 = JUPITER_V):
    '''main function that calls other functions to calculate and plot the
    hyperbolic escape velocity
    inputs: maximum delta_v of second burn
            r0 - starting orbital distance
            v0 - starting orbital velocity'''

    # display parameters
    print("Begin two burn calculation")
    print("Maximum Delta v of burn 2: ", max_dv2, " m/s")
    print("Starting radial distance: %.2f" %(r0/1e9), "  million km")
    print("Starting radial distance: %.2f" %(r0/1e9), " million km")
    print("Starting radial velocity: %.2f" %(v0/1e3), " km/s\n")

    # calculate maximum delta_v for first burn - required to meet MIN_R
    max_dv1 = calc_dv(MIN_R, JUPITER_R, v0)

    # display calculated maximum delta_v
    print("maximum delta_v for first burn: %.2f" %(max_dv1/1e3), " km/s\n")

    # array of possible DV1 values
    v1_values = np.arange(0.0, max_dv1, step = DV_STEP)
    # array of possible DV2 values
    v2_values = np.arange(0.0, max_dv2, step = DV_STEP)
    # array of (dv1, dv2, v_infinity)
    v_infinities = np.zeros(((len(v1_values) * len(v2_values)), 3))
    # print number of delta v combinations to calculate
    print("Number of delta_v combinations: ", len(v_infinities))

    # calculate v_infinity for every combination of dv_1 and dv_2
    for dv_i in range(len(v_infinities)):
        # look up delta_v of first burn
        dv1 = v1_values[int(math.floor(dv_i/len(v2_values)))]
        # look up delta_v of second burn
        dv2 = v2_values[dv_i % len(v2_values)]
        # fill in v1 values
        v_infinities[dv_i][0] = dv1
        # fill in v2_values
        v_infinities[dv_i][1] = dv2
        # call function to calculate v_infinity
        v_infinities[dv_i][2] = calc_vi(dv1, dv2, r0, v0)

    print(v_infinities)

    print("Delta_v calculations complete!")

    print(v_infinities[3])

    # plot plotting function 
    plot_vi(v_infinities)
    # plot curve for single given velocity repeatedly
    plot_single_dv(v_infinities, 4000)
    return

def calc_vi(dv1, dv2, r0, v0):
    '''calculates v_infinity based on the delta v
    of two burns. The starting distance from the sun and
    starting velocity are by default Jupiter's
    inputs: dv1 - change in velocity of retrograde burn
            dv2 - change in velocity of escape burn
            r0 - starting distance from sun
            v0 - starting velocity
    outputs: v_infinity - hyperbolic excess velocity'''

    # calculate perihelion and velocity at perihelion
    rp, vp = calc_perihelion(dv1, r0, v0)

    v_infinity = ((vp + dv2)**2 - 2*M_S*G/rp)**0.5

    print("rp: %.2f" %(rp/1e9), " million km")
    print("vp: %.2f" %(vp/1e3), " km/s")
    print("vi: %.2f" %(v_infinity/1e3), " km/s")

    return v_infinity


def calc_perihelion(dv1, r0, v0):
    '''helper function for calc_vi. Calculates the perihelion
    and velocity at perihelion
    inputs: dv1 - delta v from first burn
            r0 - starting distance from the sun
            v0 - starting velocity'''
    a = (2/r0 - ((v0-dv1) ** 2)/G/M_S) ** -1  # calculate semi-major axis
    rp = 2*a - r0                           # calculate perihelion distance
    vp = r0*v0/rp                           # calculate velocity at perihelion



    return rp, vp                           # return perihelion and velocity

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

def plot_vi(data):
    '''plots v_infinity as a function of dv1 and dv2
    inputs: data - data to plot. List of lists with each
                   sublist made of triples (dv1, dv2, v_infinity)
                   Each sublist has the same total delta v'''

    print("plot_vi does nothing! XD")
    return

def plot_single_dv(data, dv):
    '''plots v_infinity for a single constant dv
    inputs: data - array with all v_i data given all dv combinations'''

    print("plot_single_dv does nothing!! XD")

    return
