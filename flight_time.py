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
        dv_per_burn = dv/steps
        # calculate coast time between burns
        coast_period = time * SEC_PER_DAY / steps

        # loop steps times
        for step in steps:
        	# perform instantaneous burn
        	self.burn(dv_per_burn)
        	# coast for period of time
        	self.coast_time()

		return

	def burn(self, dv):
		'''execute an instantaneous burn and update orbital
		parameters'''
		self.v += dv
		
		return


	def coast_time(self, coast_period):
		'''coast for a period of time. Computes a linear
		approximation of the velocity and updates dis_travel
		and elapse_t
		inputs: coast_period - desired time to coast for'''

		# compute slope of velocity as function of self.dis_travel

		# solve expression for distance traveled in given time

		# update orbital parameters
        self.v = 
        self.elapse_t += coast_period
        self.dis_travel += 
        self.r = (self.r0**2 + self.dis_travel**2) ** 0.5

		return



	def coast_distance(self, steps, final_d):
		'''coast a step distance and update the time and r
		   inputs - final_d - final distance to coast to (AU)
                    steps - number of steps to take to get
                            to final_d
            outputs: elapse_t - time elapsed to reach final_d (years)'''

        # calculate step size in meters
        step_size = (final_d * AU) - self.dis_travel

        for step in steps:
        	# loop through steps and coast a set distance

        	# starting velocity
        	v_start = self.v
        	# ending velocity
        	v_end = 

        	# trapezoid approximation of time elapsed 
        	t = 0.5 * (1/v_start + 1/v_end) * step_size

        	# update orbital parameters
        	self.v = v_end
        	self.elapse_t += t
        	self.dis_travel += step
        	self.r = (self.r0**2 + self.dis_travel**2) ** 0.5

		return



def calc_flight_time():
    '''calculates the flight time through numerical integration'''

    return

def calc_velocity(v0, r0, rf):
	'''calculates the final velocity vf of a spacecraft by
	conservation of energy
	inputs: v0 - initial velocity
	        r0 - initial distance from parent body
	        rf - final distance from parent body'''
	        
    # calculate C3 - kinetic energy plus potential energy per mass
    C3 = 0.5 * v0 **2 - M_S * G / r0
    # calculate vf - C3 is unchanged
    vf = (2 * (C3 + M_S * G /rf)) ** 0.5
	return