# astronomical constants.py
#
# This file contains astronomical constants and is used
# by other files
#
# Revision History
# 03/18/19    Tim Liu    copied constants from oberth


# orbital constants
G = 6.674e-11                         # universal gravity constant in MKS
M_S = 1.99e30                         # mass of the sun in kilograms
M_J = 1.90e27                         # mass of Jupiter in kilograms
M_E = 5.98e24                         # mass of Earth in kilograms
R_S = 6.96e8                          # radius of the sun in meters
C = 299792458                         # speed of light meters per second
AU = 1.496e11                         # astronomical unit in meters
JUPITER_R = 5 * AU                    # approximate Jupiter's distance from sun in meters (5AU)
CALLISTO_R = 1.88e9                   # Callisto semi major axis
JUPITER_V = (G*M_S/JUPITER_R) ** 0.5  # approximate orbital velocity of Jupiter

# particle constants
MASS_HE4 = 6.644e-27                  # mass of He-4 in kg
MASS_HE3 = 5.008e-27                  # mass of He-3 in kg
MASS_D2 =  3.343e-27                  # mass of deuterium in kg
MASS_T3 =  5.008e-27                  # mass of tritium in kg
MASS_P1 =  1.673e-27                  # mass of proton in kg
MASS_N1 =  1.675e-27                  # mass of neutron in kg

EV_PER_MEV = 1e6                      # electron volts per mega electron volt
J_PER_EV = 1.602e-19                  # joules per electron volt

# time constants
SEC_PER_YEAR = 3.154e7                # seconds per year
SEC_PER_DAY = 86400                   # seconds in a day
DAYS_PER_YEAR = 365.25                # days per year
