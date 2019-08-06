# flight_time test.py
#
# functions for testing the Spacecraft class methods, flight_time.py
# and orbit.py helper functions
#
# Table of contents
#            
#
# Revision history
# 07/02/19    Tim Liu    created file

from astro_constants import *     # astronomical constants
from orbit import *               # helper functions for orbital calculations
from spacecraft import *          # spacecraft class
from flight_time import *         # flight time program
import math                       # math library


# **** TEST ORBIT.PY LIBRARY *** #



# **** TEST SPACECRAFT.PY CLASS *** #

def test_methods():
    '''tests that all methods of Spacecraft class run without error.
    Creates instance of Spacecraft class and calls each method. Does NOT
    check outputs of each method.'''

    # create instance of spacecraft class traveling 30km/s at ~0.6AU
    test_craft = Spacecraft(30000, 1e11, M_S)
    print("\nCalling repr method...")
    print(test_craft)
    
    print("\nCalling burn() method")
    test_craft.burn(10)

    print("\nCalling coast_time() method")
    test_craft.coast_time(1000)

    print("\nCalling long_burn() method")
    test_craft.long_burn(1, 1, 10)

    print("\nCalling coast_distance() method")
    test_craft.coast_distance(5, 1)


def test_coast_time():
    '''creates an instance of Spacecraft. Calls coast time
    multiple times and prints the starting and ending parameters - user
    must manually check values are reasonable'''

    return

def test_coast_distance():
    '''creates an instance of Spacecraft class. Calls coast_distance
    method multiple times and prints starting and end parameters - user
    much manually check values are reasonable'''

    return

def test_coast_distance2():
    '''creates instance of Spacecraft class and calls coast_distance
    method once over a regime where coast time and distance should
    be linear; compares calculated coast distance with linear
    approximation'''


    return

