# flight_time.py
#
# program for calculating the flight time to the focal point
#
# Table of contents
# open_flight_profile - opens an xlsx spreadsheet with saved
#                       flight parameters then calls flight_time
#
# flight_time - calculates the approximate flight time of a 
#               spacecraft from the periapsis to a given distance
#               in space              
#
# Revision history
# 03/19/19    Tim Liu    created file and wrote calc_exhaust_velocity 
# 03/20/19    Tim Liu    wrote skeleton of spacecraft class
# 03/24/19    Tim Liu    rewrote spacecraft class methods to use
#                        two linear approximations
# 06/26/19    Tim Liu    wrote flight_time function
# 06/26/19    Tim Liu    removed spacecraft class; file now only
#                        contains calculations for flight time
# 08/11/19    Tim Liu    wrote open_flight_profile for reading excel files
#                        with a flight profile

from astro_constants import *     # astronomical constants
from orbit import *               # helper functions for orbital calculations
from spacecraft import *          # spacecraft class
import math                       # math library
import time                       # time library
import pandas as pd               # pandas libray for reading excel
import datetime as dt             # datetime library

def open_flight_profile(f_in_name):
    '''opens a .xlsx file with the conditions describing a 
    flight profile. Parses file and calls flight_time() to
    calculate the flight time to a given point in space. Saves a
    text file as a log of the mission. Records the ship status both
    after the burn and after the cruise phase in the log'''

    # open .xlsx file with flight profile - MUST follow flight_profile_template.xlsx
    f_profile = pd.read_excel(f_in_name, usecols = "B")

    # parse arguments
    v0 = f_profile['Value'][0]
    r0 = f_profile['Value'][1]
    dv = f_profile['Value'][2]
    if f_profile['Value'][3] == "Sun":
        # generalize to other parent bodies
        parent_m = M_S
    else:
        print("Not recognized parent mass!")
    r_final = f_profile['Value'][4]
    burn_time = f_profile['Value'][5]
    burn_steps = f_profile['Value'][6]
    coast_steps = f_profile['Value'][7]

    # call flight_time to run simulation
    post_burn, post_cruise, calc_time = flight_time(v0, r0, dv, burn_time, burn_steps, coast_steps, parent_m, r_final)


    # log string to save flight profile and results in text file
    log_str = ""
    log_str += "***** Flight parameters *****\n"
    log_str += "Initial velocity: %.2f m/s\n" %(v0)
    log_str += "Periapsis:        %.2f AU\n" %(r0)
    log_str += "Delta-v:          %.2f m/s\n" %(dv)
    log_str += "Parent mass:      %.0f kg\n" %(parent_m)
    log_str += "Flight distance:  %.0f AU\n" %(r_final)
    log_str += "***** Approximation parameters ***** \n"
    log_str += "Burn time:        %.2f days\n" %(burn_time)
    log_str += "Burn steps:       %d steps\n" %(burn_steps)
    log_str += "Coast steps:      %d steps\n"   %(coast_steps)
    log_str += "Calculation time: %0.2f seconds\n" %(calc_time)
    
    log_str += "\n*** Post burn craft parameters: ***\n"
    log_str += str(post_burn)
    # call ship repr function
    log_str += "\n*** Final craft parameters: ***\n"
    log_str += str(post_cruise)

    print("Printing flight log...")
    # write information to log
    currentDT = dt.datetime.now()
    f = open("flight_log_%s.txt" %currentDT.strftime("%m-%d_%H-%M"), "w")
    f.write(log_str)
    f.close()
    return


def flight_time(v0, r0, dv, burn_time, burn_steps, coast_steps, parent_m, r_final):
    '''Calculates the time required to fly a given distance from
    the periapsis using numerical approximation. Creates an
    instance of the spacecraft class and calls methods to calculate
    time spent during the burn and during the cruise phase.

    inputs: v0 - starting velocity (km/s)
            r0 - periapsis (AU)
            dv - delta-v of the periapsis burn (km/s)
            time - length of the periapsis burn (days)
            steps - number of discrete burns the periapsis burn is
                    separated into; higher number is more accurate
                    but requires more computation time
            parent_m - mass of the parent body (kg)
            r_final - final distance from the periapsis (AU)
    outptus: ship - Spacecraft object created
             comp_time - seconds needed to finish computation'''


    print("***** Flight parameters *****")
    print("Initial velocity: %.2f m/s" %(v0))
    print("Periapsis:        %.2f AU" %(r0))
    print("Delta-v:          %.2f m/s" %(dv))
    print("Parent mass:      %.0f kg" %(parent_m))
    print("Flight distance:  %.0f AU\n" %(r_final))

    print("***** Approximation parameters ***** ")
    print("Burn time:        %.2f days" %(burn_time))
    print("Burn steps:       %d steps\n" %(burn_steps))
    print("Coast steps:      %d steps\n" %(coast_steps))

    # record start time
    start_time = time.time()

    # create instance of spacecraft
    print("Creating instance of spacecraft class...")
    ship = Spacecraft(v0, r0*AU, parent_m)
    print(ship, "\n")

    # call long_burn method and execute approximated continuous burn
    print("Approximating continuous burn...\n")
    ship.long_burn(dv, burn_time, burn_steps)
    # clone the ship class to save post burn parameters
    post_burn = ship.clone()

    # call coast functions to calculate cruise distance to r_f
    print("Approximating coast period...\n")
    ship.coast_distance(coast_steps, r_final)

    # print final results
    comp_time = time.time()-start_time
    print("Flight time: %.2f years" %(ship.get_elapse_t(units = "years")))
    print("Calculation completed in %.3f seconds" %comp_time)


    return post_burn, ship, comp_time

