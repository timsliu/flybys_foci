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

from astro_constants import *     # astronomical constants
from orbit import *               # helper functions for orbital calculations
from spacecraft import *          # spacecraft class
import math                       # math library

def open_flight_profile(f_in_name):
	'''opens a .xlsx file with the initial conditions of a 
	flight profile. Parses file and calls flight_time() to
	calculate the flight time to a given point in space'''

	# TODO

	return


def flight_time(v0, r0, dv, burn_time, burn_steps, parent_m, r_final, name = ""):
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
    outptus: none'''

    # print parameters
    if name != "":
    	print("Mission name: ", name, "\n")

    print("***** Flight parameters *****")
    print("Initial velocity: %.2f km/s" %(v0))
    print("Periapsis:        %.2f AU" %(r0))
    print("Delta-v:          %.2f km/s" %(dv))
    print("Parent mass:      %.0f kg" %(kg))
    print("Flight distance:  %.0f AU\n" %(AU))

    print("***** Approximation parameters ***** ")
    print("Burn time:        %.2f days" %(days))
    print("Burn steps:       %.0f steps\n" %(steps))

    # record start time
    start_time = time.time()

    # create instance of spacecraft
    print("Creating instance of spacecraft class...")
    ship = spacecraft(v0, r0, parent_m)
    print(ship, "\n")

    # call long_burn method and execute approximated continuous burn
    print("Approximating continuous burn...\n")
    ship.long_burn(dv, burn_time, steps)

    # call coast functions to calculate cruise distance to r_f
    print("Approximating coast period...\n")
    ship.coast_distance(coast_steps, r_final)

    # print final results
    print("Flight time: %.2f years", %(ship.get_elapse_t()))
    print("Calculation completed in %.3f seconds" %(time.time()-start_time))

    return

