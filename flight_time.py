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
# 03/20/19    Tim Liu    wrote skeleton of spacecraft class
# 03/24/19    Tim Liu    rewrote spacecraft class methods to use
#                        two linear approximations
#

from astro_constants import *

import math


def calc_exhaust_velocity(mass, energy_ev):
    '''calculates the exhaust velocity of a particle
    inputs: mass - mass of the particle
            energy - kinetic energy of the particle in MeV
    outputs: ve - exhaust velocity in meters per second'''

    energy_ev *= EV_PER_MEV                 # convert MeV to EV

    energy_j = energy_ev * J_PER_EV         # convert energy to joules
    velocity = math.sqrt(2 * energy_j/mass) # calculate velocity in m/s
    return velocity


class spacecraft():
	'''class for a spacecraft in hyperbolic orbit. Class specifies the spacecraft's
	velocity and position in a hyperbolic orbit approximated as a straight
	line perpendicular to and offset from the mass being orbited. Class
	contains methods for updating the position of the spacecraft
	and calculating the time elapse'''
	def __init__(self, v0, r0):
		self.v = v0                   # spacecraft velocity
		self.r = r0                   # spacecraft distance from parent body (meters)
		self.r0 = r0                  # periapsis in meters
		self.elapse_t = 0             # time elapsed (seconds)
		self.dis_travel = 0           # distance traveled from periapsis



	def get_v(self):
		'''returns current velocity in km/s'''
		return self.v0/1000

	def get_r(self):
		'''return distance from parent body in AU'''
		return self.r/AU

	def get_r0(self):
		'''returns periapsis r0 in AU'''
		return self.r0/AU

	def get_elapse_t(self):
		'''returns the elapsed time in years'''
		return elapse_t/SEC_PER_YEAR

	def get_dis_travel(self):
		'''returns distance traveled in AU'''
		return self.dis_travel/AU

	def long_burn(self, dv, time, steps):
		'''execute a burn that takes a non zero amount of time;
		the burn is spread out into multiple instantaneous burns. Method
		alternates calling burn and coast_time
		inputs: dv - total delta-v (km/s) of the burn
		        time - length of time (days) of the burn
		        steps - number of discrete burns to break the long
		                burn into'''
        
        # calculate dv for each burn

        # calculate coast time between burns

        # loop steps times

        for step in steps:
        	# instantaneous burn
        	self.burn()
        	# coast for period of time
        	self.coast_time()

		return

	def burn(self, dv):
		'''execute an instantaneous burn and update orbital
		parameters'''

		# update velocity

		return


	def coast_time(self, target_time):
		'''coast for a period of time. Computes a linear
		approximation of the velocity and updates dis_travel
		and elapse_t
		inputs: target_time - desired time to coast for'''

		# compute slope of velocity as function of self.dis_travel

		# solve expression for distance traveled in given time

		# update self.elapsed_t

		# update self.dis_travel

		return



	def coast_distance(self, steps, final_d):
		'''coast a step distance and update the time and r
		   inputs - final_d - final distance to coast to (AU)
                    steps - number of steps to take to get
                            to final_d'''

		return


def calc_flight_time():
    '''calculates the flight time through numerical integration'''

    return
