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
# 08/11/19    Tim Liu    wrote repr function
# 08/11/19    Tim Liu    changed long_burn method to take dv in m/s
# 08/11/19    Tim Liu    added clone method

from astro_constants import *     # astronomical constants
from orbit import *               # helper functions for orbital calculations
import math                       # math library


class Spacecraft():
    '''class for a spacecraft in hyperbolic orbit. Class specifies the spacecraft's
    velocity and position in a hyperbolic orbit approximated as a straight
    line perpendicular to and offset from the mass being orbited. Class
    contains methods for updating the position of the spacecraft
    and calculating the time elapsed. Internally all units are handled
    in MKS.'''
    def __init__(self, v0, r0, parent_m):
        self.v = v0               # spacecraft velocity (m/s)
        self.r = r0               # spacecraft distance from parent body (m)
        self.r0 = r0              # periapsis (m)
        self.parent_m = parent_m  # mass of parent body (kg)
        self.elapse_t = 0         # time elapsed (seconds)
        self.dis_travel = 0       # distance traveled from periapsis (m)

    def clone(self):
        '''clone parameters to another Spacecraft class
        outputs: new - new spacecraft class w/ identical attributes'''
        new = Spacecraft(self.get_v(), self.get_r0(), self.parent_m)
        new.r = self.get_r()
        new.elapse_t = self.get_elapse_t()
        new.dis_travel = self.get_dis_travel()

        return new

    # *** accessor functions *** #
    def get_v(self, units = "m/s"):
        '''returns current velocity in m/s unless specified in km/s'''

        if units == "km/s":
            return self.v/1000
        else:
            return self.v

    def get_r(self, units = "m"):
        '''return distance from parent body in m unless specified in AU'''
 
        if units == "AU":
            return self.r/AU
        else:
            return self.r

    def get_r0(self, units = "m"):
        '''returns periapsis r0 in m unless specified in AU'''

        if units == "AU":
            return self.r0/AU
        else:
            return self.r0

    def get_elapse_t(self, units = "sec"):
        '''returns the elapsed time in years'''

        if units == "years":
            return self.elapse_t/SEC_PER_YEAR
        else:
            return self.elapse_t

    def get_dis_travel(self, units = "m"):
        '''returns distance traveled in m unless specified in AU'''

        if units == "AU":
            return self.dis_travel/AU
        else:
            return self.dis_travel

    # *** main function for executing a long burn *** #
    def long_burn(self, dv, time, steps):
        '''execute a burn that takes a non zero amount of time;
        the burn is spread out into multiple instantaneous burns. Method
        alternates calling burn and coast_time
        inputs: dv - total delta-v (m/s) of the burn
                time - length of time (days) of the burn
                steps - number of discrete burns to break the long
                        burn into
        '''
        
        # calculate dv for each burn in m/s
        dv_per_burn = dv / steps
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
    def coast_time(self, coast_period, delta = 1e8):
        '''coast for a period of time. Computes a linear
        approximation of the velocity and updates orbital parameters.

        inputs: coast_period - desired time to coast for (s)
                delta - coast distance used as delta; default to 10 000 kmeters
        updates: self.v
                 self.elapse_t
                 self.dis_travel
                 self.r'''
        # compute r after spacecraft coasts for delta
        r_plus_delta = math.sqrt((self.dis_travel + delta) ** 2 + self.r0 ** 2)
        # compute slope of velocity as function of self.dis_travel
        m = (calc_v_2(self.v, self.r, r_plus_delta) - self.v) / delta
        # check that slope is always negative
        assert(m <= 0)
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

        inputs:  n       - number of segments to use for Simpson's approximation     
                 x_final - final distance to coast to (max self.dis_travel) (AU)
                 
        updates: self.dis_travel
                 self.r
                 self.v
                 self.elapse_t'''

        # adjust n to be appropriate for Simpson's rule
        if n % 2 != 0:
            # n must be even for Simpson's rule
            n += 1
        n = max(n, 6) # set minimum value for aproximation

        # calculate step size in meters between points used in approximation
        step_size = (x_final * AU - self.dis_travel)/n
        
        # list of coefficients to multiply f(x_n) by - last coefficient
        # corresponds to (n) and coefficients are 0 indexed
        coefs = [2 if x%2 == 0 else 4 for x in range(n + 1)]
        coefs[0]  = 1
        coefs[-1] = 1

        # list of x_values (dis_travel) to use - values extend from
        # current self.dis_travel to r_final
        x_values = [self.dis_travel + x * step_size for x in range(n + 1)]

        # list of r values (distance from parent mass) to evaluate
        # function being approximated at
        r_values = [math.sqrt(x_values[x] ** 2 + self.r0 ** 2) for x in range(n + 1)]

        # list of evaluated values of the function being approximated (1/v(r))
        f_values = [1/calc_v_2(self.v, self.r, r_values[x]) 
                   for x in range(n + 1)]

        # calculate time to coast to x_final
        coast_time = step_size/3 * \
                     sum([f_values[x] * coefs[x] for x in range(n+1)])
        
        # update elapsed time
        self.elapse_t += coast_time
        # update position and velocity
        new_r = r_values[-1]
        self.v = calc_v_2(self.v, self.r, new_r)
        self.r = new_r
        self.dis_travel = x_final * AU

        return

    def __str__(self):
        '''Print basic information about the object when called'''

        output_string = ""
        output_string += "Current velocity:     %.2fkm/s\n"  %(self.v/1000)
        output_string += "Periapsis:            %.2fAU\n"    %(self.r0/AU)
        output_string += "Distance from parent: %.2fAU\n"    %(self.get_r(units = "AU"))
        output_string += "Distance travelled:   %.2fAU\n"    %(self.get_dis_travel(units = "AU"))
        output_string += "Elapsed time:         %.2fyears\n" %(self.get_elapse_t(units = "years"))

        return output_string


