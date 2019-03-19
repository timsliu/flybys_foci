# astronomical constants.py
#
# This file contains astronomical constants and is used
# by other files
#
# Revision History
# 03/18/19    Tim Liu    copied constants from oberth


G = 6.674e-11                         # universal gravity constant in MKS
M_S = 1.99e30                         # mass of the sun in kilogram
R_S = 6.96e8                          # radius of the sun in meters
C = 299792458                         # speed of light meters per second
AU = 1.496e11                         # astronomical unit in meters
JUPITER_R = 5 * AU                    # approximate Jupiter's distance from sun in meters (5AU)
JUPITER_V = (G*M_S/JUPITER_R) ** 0.5  # approximate orbital velocity of Jupiter