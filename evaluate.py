# evaluate.py
#
# call other function and evaluate simple orbital calculations

from astro_constants import *
from orbit import *


def calc1():
    # rp - perihelion distance for jupiter escape burn
    rp = 7.56e7
    return calc_v(CALLISTO_R, rp, M_J)

def calc2():
    return calc_dv_escape(10000, 81100, 7.56e7, M_J)
