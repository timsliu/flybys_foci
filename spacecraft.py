# spacecraft.py
#
# class that defines a spacecraft in an approximated hyperbolic
# escape orbit
#
# Table of contents
#
#
# Revision history
# 03/19/19    Tim Liu    created file and wrote calc_exhaust_velocity 
# 03/20/19    Tim Liu    wrote skeleton of spacecraft class
# 03/24/19    Tim Liu    rewrote spacecraft class methods to use
#                        two linear approximations
# 06/26/19    Tim Liu    updated flight_time function
# 06/26/19    Tim Liu    separated spacecraft class into separate
#                        file; removed flight_time
# 06/26/19    Tim Liu    wrote spacecraft.long_burn() method
# 06/26/19    Tim Liu    rewrote spacecraft.coast_distance() method to use
#                        Simpson's rule instead of trapezoid rule
# 07/04/19    Tim Liu    updated default delta in coast_time() to 10 000 km

from astro_constants import *     # astronomical constants
from orbit import *               # helper functions for orbital calculations
import math                       # math library


class Spacecraft():
    '''class for a spacecraft in hyperbolic orbit. Class specifies the spacecraft's
    velocity and position in a hyperbolic orbit approximated as a straight
    line perpendicular to and offset from the mass being orbited. Class
    contains methods for updating the position of the spacecraft
    and calculating the time elapse'''
    def __init__(self, v0, r0, parent_m):
        self.v = v0               # spacecraft velocity (m/s)
        self.r = r0               # spacecraft distance from parent body (m)
        self.r0 = r0              # periapsis (m)
        self.parent_m = parent_m  # mass of parent body (kg)
        self.elapse_t = 0         # time elapsed (seconds)
        self.dis_travel = 0       # distance traveled from periapsis (m)

    # *** accessor functions *** #
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

    # *** main function for executing a long burn *** #
    def long_burn(self, dv, time, steps):
        '''execute a burn that takes a non zero amount of time;
        the burn is spread out into multiple instantaneous burns. Method
        alternates calling burn and coast_time
        inputs: dv - total delta-v (km/s) of the burn
                time - length of time (days) of the burn
                steps - number of discrete burns to break the long
                        burn into
        '''
        
        # calculate dv for each burn in m/s
        dv_per_burn = dv/1000/steps
        # calculate coast time between burns in seconds
        coast_period = time * SEC_PER_DAY / steps

        # loop performing step burns times
        for step in range(steps):
            # perform instantaneous burn
            self.burn(dv_per_burn)
            # coast for period of time
            self.coast_time(coast_period)

        return

    def burn(self, dv):
        '''execute an instantaneous burn. Burn modifies only the
        current velocity'''
        self.v += dv
        
        return

    # *** helper methods for when spacecraft is coasting *** #
    def coast_time(self, coast_period, delta = 1e7):
        '''coast for a period of time. Computes a linear
        approximation of the velocity and updates orbital parameters.

        inputs: coast_period - desired time to coast for (s)
                delta - coast distance used as delta; default to 1000 meters
        updates: self.v
                 self.elapse_t
                 self.dis_travel
                 self.r'''
        # TODO some handling to ensure self.r and r_plus_delta aren't equal
        # compute r after spacecraft coasts for delta
        r_plus_delta = math.sqrt((self.dis_travel + delta) ** 2 + self.r0 ** 2)
        # compute slope of velocity as function of self.dis_travel
        self.get_r()
        print(r_plus_delta)
        print(calc_v_2(self.v, self.r, r_plus_delta))
        print(self.v)
        m = (calc_v_2(self.v, self.r, r_plus_delta) - self.v) / delta
        # check that slope is always negative - TODO check assertion syntax
        assert(m < 0)
        print(m)

        # solve expression for new distance traveled (xf)
        xf = (math.exp(m * coast_period) * (self.v + m * self.dis_travel) - self.v) / m

        # update orbital parameters
        # calculate new distance from parent mass
        new_r = (self.r0**2 + xf**2) ** 0.5 
        # update velocity  
        self.v = calc_v_2(self.v, self.r, new_r)
        # update elapsed time
        self.elapse_t += coast_period
        # update distance traveled 
        self.dis_travel = xf   
        # update distance from parent mass                            
        self.r = new_r

        return

    def coast_distance(self, n, x_final):
        '''calculate the amount of time needed to a coast to a final position
        (self.dis_travel) from the current position. Uses Simpson's rule to
        numerically approximate flight time

        inputs:  n       - number of points to use for Simpson's approximation     
                 x_final - final distance to coast to (max self.dis_travel) (AU)
                 
        updates: self.dis_travel
                 self.r
                 self.v
                 self.elapse_t'''

        # adjust n to be appropriate for Simpson's rule
        if n % 2 != 1:
            # n must be odd for Simpson's rule
            n += 1
        n = max(n, 5) # set minimum value for aproximation

        # calculate step size in meters between points used in approximation
        step_size = (x_final * AU - self.dis_travel)/ (n - 1)
        
        # list of coefficients to multiply f(x_n) by
        coefs = [2 if x%2 == 0 else 4 for x in range(n)]
        coefs[0]  = 1
        coefs[-1] = 1

        # list of x_values (dis_travel) to use - values extend from
        # current self.dis_travel to r_final
        x_values = [self.dis_travel + x * step_size for x in range(n)]
        # TODO - remove assertion
        assert(x_values[-1] == x_final * AU)

        # list of r values (distance from parent mass) to evaluate
        # function being approximated at
        r_values = [math.sqrt(x_values[x] ** 2 + self.r0 ** 2) for x in range(n)]

        # list of evaluated values of the function being approximated (1/v(r))
        f_values = [1/calc_v_2(self.v, self.r, r_values[x]) 
                   for x in range(n)]

        # calculate time to coast to x_final
        coast_time = step_size/3 * \
                     sum([f_values[x] * coefs[x] for x in range(n)])
        
        # update elapsed times
        self.elapse_t += coast_time

        return

    def __repr__(self):
        '''Print basic information about the class when called'''

        # TODO - write repr

        output_string = "This is the spacecraft class. The __repr__\
                         function hasn't been finished."


        return output_string


