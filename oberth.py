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
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pandas as pd
import datetime as dt
import os

HOME = os.getcwd()


# constants

G = 6.674e-11                         # universal gravity constant in MKS
M_S = 1.99e30                         # mass of the sun in kilogram
AU = 1.496e11                         # astronomical unit in meters
JUPITER_R = 5 * AU                    # approximate Jupiter's distance from sun in meters (5AU)
JUPITER_V = (G*M_S/JUPITER_R) ** 0.5  # approximate orbital velocity of Jupiter
MIN_R = 0.1 * AU                      # closest approach to sun allowed
                                      # Parker Solar Probe MIN_R ~0.05 AU
DV_STEP = 50                          # delta_v increment between calculated combinations in m/s


def compare(max_dv, r0 = JUPITER_R, v0 = JUPITER_V):
    '''calculates v_infinity from a single burn and from two burns.
       plots chart comparing v_infinities
       inputs: max_dv - maximum delta_v available'''

    # calculates vi from a single burn; perihelion drop first burn
    # is set to 0
    one_burn_vi = calc_vi(0, max_dv, r0, v0)

    # calculate delta_v from two burns

    # calculate maximum allowed delta_v for first burn - required to meet MIN_R
    max_dv1 = calc_dv(MIN_R, JUPITER_R, v0)
    # array of v1_values (first burn, dropping perihelion)
    v1_values = np.arange(0.0, min(max_dv1, max_dv), step = DV_STEP)
    # array of v2_values (second burn, heliocentric escape)
    v2_values = np.array([max_dv - x for x in list(v1_values)])
    # array holding [v1, v2, v_infinity]
    v_infinities = np.zeros((len(v1_values), 3))
    # print number of delta v combinations to calculate
    print("Number of delta_v combinations: ", len(v_infinities))

    # compute v_infinity for each combination of burns; note that every combination
    # has the same total delta_v
    for dv_i in range(len(v_infinities)):
        # fill in v1 values
        v_infinities[dv_i][0] = v1_values[dv_i]
        # fill in v2_values
        v_infinities[dv_i][1] = v2_values[dv_i]
        # call function to calculate v_infinity
        v_infinities[dv_i][2] = calc_vi(v1_values[dv_i], v2_values[dv_i], r0, v0)

    # call function to plot v_infinity from the two options
    plot_single_dv(v_infinities, one_burn_vi, max_dv)


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

    print("Delta_v calculations complete!")

    # plot plotting function 
    dv_budgets = [10, 20, 40, 80]   # delta_v budgets (km/s) lines to plot
    plot_vi(v_infinities, dv_budgets)   # call function to plot vi combos
    
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


    if (vp + dv2)**2 < 2*M_S*G/rp:
        # heliocentric escape velocity not attained
        v_infinity = -1
    else:
        # attained escape velocity
        v_infinity = ((vp + dv2)**2 - 2*M_S*G/rp)**0.5

    return v_infinity


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

def plot_vi(data, dv_budgets):
    '''plots v_infinity as a function of dv1 and dv2
    inputs: data - data to plot. List of lists with each
                   sublist made of triples (dv1, dv2, v_infinity)
                   Each sublist has the same total delta v
            dv_budgets - list of delta_v budget lines to plot (km/s)'''
    print("\nBeginning to plot...")

    data = data/1000 # convert m/s to km/s

    # array for burn combinations resulting in escape
    dv_1 = []
    dv_2 = []
    v_in = []

    # array for burn combinations that do not escape the sun
    dv_1_trapped = []
    dv_2_trapped = []
    v_in_trapped = []

    for i in range(len(data)):
        # fill in each variable from the data array
        if data[i][2] > 0:
            # fill in array for combos that escape the sun
            dv_1.append(data[i][0])
            dv_2.append(data[i][1])
            v_in.append(data[i][2])
        else:
            # fill in array for combos that do not escape the sun
            dv_1_trapped.append(data[i][0])
            dv_2_trapped.append(data[i][1])
            v_in_trapped.append(data[i][2])

    
    # set up the graph
    plt.xlim(0, max(dv_1))                          # set limit of x axis
    plt.ylim(0, max(dv_2))                          # set limit of y axis
    cm = plt.cm.get_cmap('Blues')                   # color scale for v_infinity
    plt.xlabel("Delta_v first burn (km/s)")         # xlabel
    plt.ylabel("Delta_v second burn(km/s)")         # ylabel
    plt.title("V infinity from burn combos (km/s)") # plot title
    plt.grid(True)                                  # draw gridlines

    # plot the combos that escape with different colors
    sc = plt.scatter(dv_1, dv_2, c=v_in, vmin=0, 
        vmax=(math.ceil(max(v_in)/100)) * 100, cmap=cm)
    # plot the combos that do not escape, all in gray
    plt.scatter(dv_1_trapped, dv_2_trapped, c = "dimgray")
    # plot the color bar
    colorbar = plt.colorbar(sc)
    colorbar.set_label("v_infinity (km/s)")

    # draw lines for each delta_v budget
    for dv_b in dv_budgets:
        # plot a line representing a possible delta-v budget
        plt.plot([0, dv_b], [dv_b, 0])
        # label the line
        plt.text(max(dv_1)/40, dv_b + max(dv_2)/40, 
            "Delta_v = %d km/s" %(dv_b))

    # format plot save name
    currentDT = dt.datetime.now()
    timestamp = currentDT.strftime("%Y-%m-%d %H_%M_%S")

    # go to graph directory and save
    os.chdir(HOME + "/graphs")
    plt.savefig("v_infinity_" + timestamp + "_.png", format="png", dpi = 800)
    os.chdir(HOME)

    plt.close()

    return

def plot_single_dv(v_infinities, one_burn_vi, max_dv):
    '''plots v_infinity for a single constant dv
    inputs: data - array with all v_i data given all dv combinations'''

    # create list of just dv1 (km/s)
    dv_1 = [x[0]/1000 for x in list(v_infinities)]
    # create list of just dv2 (km/s)          
    dv_2 = [x[1]/1000 for x in list(v_infinities)]
    # create list of just v_infinities (km/s)       
    v_in = [max(x[2], 0)/1000 for x in list(v_infinities)]    

    # set up the graph
    plt.xlim(0, max(dv_1))                             # set limit of x axis
    plt.ylim(0, math.ceil(max(max(v_in), one_burn_vi/1000) + 1))            # set limit of y axis            
    plt.xlabel("Delta_v first burn (km/s)")            # x label
    plt.ylabel("v-infinity (km/s)")                    # y label
    plt.title("v-infinity for %d km/s delta-v budget"
     %(max_dv/1000))                                   # plot title
    plt.grid(True)

    print(one_burn_vi)

    # plot the v-infinity combinations
    # plot v_infinity for two burns
    plt.plot(dv_1, v_in, label = "Two burns")                                 
    # plot v_infinity for one burn - if the burn is insufficent for escape
    # plot a zero
    plt.plot([0, max(dv_1)], [max(0, one_burn_vi/1000), max(0, one_burn_vi/1000)], label = "Single burn")  
    # save figure
    plt.legend()

    # go to graph directory and save
    os.chdir(HOME + "/graphs")
    plt.savefig("compare_%d_kms.png" %(max_dv/1000), format="png", dpi = 800)
    os.chdir(HOME)

    plt.close()


    return
