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
# 08/09/19    Tim Liu    wrote test_orbital_height and completed testing
# 08/10/19    Tim Liu    finished writing test functions for orbit.py
# 08/10/19    Tim Liu    wrote function to test coast_distance method - 
#                        method working correctly
# 08/11/19    Tim Liu    wrote and test_long_burn

from astro_constants import *     # astronomical constants
from orbit import *               # helper functions for orbital calculations
from spacecraft import *          # spacecraft class
from flight_time import *         # flight time program
import math                       # math library


# **** TEST ORBIT.PY LIBRARY *** #

def test_orbital_height():
    '''passes arguments to calc_orbital_height - results must
    be manually inspected'''
    # nested list of test cases - each list holds the arguments
    # to pass to calc_orbital_height
    test_cases = [[5000, AU, 30000], [10000, AU, 20000],
                  [-10000, AU, 30000], [20000, AU, 30000]]

    for case in test_cases:
        print("Starting velocity: ", case[2], " m/s")
        print("Starting r0: ", case[1]/AU, " AU")
        print("Delta v: ", case[0], " m/s")
        # pass test cases
        r_op, v_op = calc_orbital_height(case[0], case[1], case[2])
        print("Final rf: ", r_op/AU, " AU")
        print("Final vf: ", v_op, " m/s\n")

    return

def test_calc_dv():
    '''passes arguments to calc_dv - results must
    be manually inspected'''
    # nested list of test cases - each list holds the arguments
    # to pass to calc_orbital_height
    test_cases = [[AU, AU, 20000], [AU, 0.5 * AU, 20000],
                  [AU, 2 * AU, 10000], [AU, 0.8 * AU, 45000]]

    for case in test_cases:
        print("Starting velocity: ", case[2], " m/s")
        print("Starting r0: ", case[1]/AU, " AU")
        print("Final rf: ", case[0]/AU, " AU")
        # pass test cases
        dv = calc_dv(case[0], case[1], case[2])
        print("Delta-v needed: ", dv/1000, " km/s\n")

    return

def test_calc_dv_escape():
    '''passes arguments to calc_dv_escape - results must
    be manually inspected'''
    # nested list of test cases - each list holds the arguments
    # to pass to calc_orbital_height
    test_cases = [[0, 30000, AU], [20000, 30000, AU],
                  [0, 45000, AU]]

    for case in test_cases:
        print("Starting velocity: ", case[1], " m/s")
        print("Starting r0: ", case[2]/AU, " AU")
        print("Final v_inf: ", case[0], " m/s")
        # pass test cases
        dv = calc_dv_escape(case[0], case[1], case[2])
        print("Delta-v needed: ", dv/1000, " km/s\n")

    return

def test_calc_v_1():
    '''passes arguments to calc_v_1 - results must
    be manually inspected'''
    # nested list of test cases - each list holds the arguments
    # to pass to calc_orbital_height
    test_cases = [[AU, AU], [2 * AU, AU], [AU, 0.5 * AU], [AU, 1.5 * AU]]

    for case in test_cases:
        print("Semi-major axis: ", case[0]/AU, " AU")
        print("Orbital height: ", case[1]/AU, " AU")
        # pass test cases
        v = calc_v_1(case[0], case[1])
        print("Current velocity: ", v, " km/s\n")

    return

def test_calc_v_2():
    '''passes arguments to calc_v_2 - results must
    be manually inspected'''
    # nested list of test cases - each list holds the arguments
    # to pass to calc_orbital_height
    test_cases = [[30000, AU, 0.5 * AU], [30000, AU, 2 * AU]]

    for case in test_cases:
        print("Start r0: ", case[1]/AU, " AU")
        print("End rf: ", case[2]/AU, " AU")
        print("Start v0: ", case[0], " m/s")
        # pass test cases
        v = calc_v_2(case[0], case[1], case[2])
        print("Final velocity: ", v, " km/s\n")

    return

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

    # parameters approximately New Horizon's Jupiter to Saturn cruise
    print("Start velocity: ", 23000)
    print("Start r0: ", 5, " AU")
    test_craft = Spacecraft(23000, 5 * AU, M_S)
    test_craft.coast_time(1.25 * SEC_PER_YEAR)

    print("Final r: ", test_craft.get_r(units = "AU"), " AU")
    print("Dis travel: ", test_craft.get_dis_travel(units = "AU"), " AU\n")



def test_coast_distance():
    '''creates an instance of Spacecraft class. Calls coast_distance
    method multiple times and prints starting and end parameters - user
    much manually check values are reasonable'''


    # parameters approximately New Horizon's earth to Jupiter
    test_craft = Spacecraft(44000, AU, M_S)
    test_craft.coast_distance(50, 5)
    print("Start velocity: ", 4400)
    print("Start r0: ", AU/AU, " AU")
    print("Final x: ", 5, " AU")
    print(test_craft.get_elapse_t(units = "years"), " years\n")

    # parameters approximately New Horizon's Jupiter to Pluto cruise
    test_craft = Spacecraft(23000, 5 * AU, M_S)
    test_craft.coast_distance(500, 32.5)
    print("Start velocity: ", 23000)
    print("Start r0: ", AU/AU, " AU")
    print("Final x: ", 1.5, " AU")
    print(test_craft.get_elapse_t(units = "years"), " years\n")

    return

def test_long_burn():
    '''creates instance of Spacecraft class and calls long_burn
    method. Results must be manually inspected.'''

    # test long burn w/ same start parameters but different burn patterns
    print("Test long burn")
    print("Start velocity: ", 150000)
    print("Start r0: ", 0.1, " AU")

    # test 1 - long_burn over 10 days w/ 20 km/s delta-v and 10 steps
    test_craft = Spacecraft(150000, 0.1 * AU, M_S)
    test_craft.long_burn(20, 10, 10)
    # compute time needed to coast to 10 AU
    test_craft.coast_distance(100, 10)
    print("\n10 days 10 steps")
    print("Time to coast to 10 AU: ", test_craft.get_elapse_t(units = "years"), " years")
    print("Final position: ", test_craft.get_dis_travel(units = "AU"), " AU")

    # test 2 - long_burn over 10 days w/ 20 km/s delta-v and 1000 steps
    test_craft = Spacecraft(150000, 0.1 * AU, M_S)
    test_craft.long_burn(20, 10, 1000)
    # compute time needed to coast to 10 AU
    test_craft.coast_distance(100, 10)
    print("\n10 days 1000 steps")
    print("Time to coast to 10 AU: ", test_craft.get_elapse_t(units = "years"), " years")
    print("Final position: ", test_craft.get_dis_travel(units = "AU"), " AU")

     # test 3 - long_burn over 1 day w/ 20 km/s delta-v and 10 steps
    test_craft = Spacecraft(150000, 0.1 * AU, M_S)
    test_craft.long_burn(20, 1, 10)
    # compute time needed to coast to 10 AU
    test_craft.coast_distance(100, 10) 
    print("\n1 days 10 steps")  
    print("Time to coast to 10 AU: ", test_craft.get_elapse_t(units = "years"), " years")
    print("Final position: ", test_craft.get_dis_travel(units = "AU"), " AU")

    # test 4 - long_burn over 0.01 days w/ 20 km/s delta-v and 10 steps
    test_craft = Spacecraft(150000, 0.1 * AU, M_S)
    test_craft.long_burn(20, 0.01, 10)
    # compute time needed to coast to 10 AU
    test_craft.coast_distance(100, 10) 
    print("\n0.01 days 10 steps")
    print("Time to coast to 10 AU: ", test_craft.get_elapse_t(units = "years"), " years")
    print("Final position: ", test_craft.get_dis_travel(units = "AU"), " AU")


    # test 5 - instantaneous 20 km/s delta-v
    test_craft = Spacecraft(170000, 0.1 * AU, M_S)
    # compute time needed to coast to 10 AU
    test_craft.coast_distance(100, 10) 
    print("\nInstantaneous")
    print("Time to coast to 10 AU: ", test_craft.get_elapse_t(units = "years"), " years")
    print("Final position: ", test_craft.get_dis_travel(units = "AU"), " AU")

    return


