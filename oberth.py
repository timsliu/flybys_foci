# oberth.py
# program for calculating hyperbolic excess velocity under
# different mission profiles and plotting Einstein's trajectory

# Revision History
# 03/10/19    Tim Liu    started file; wrote main and skeleton functions
# 03/11/19


# Table of Contents
#



# constants

G = 6.674e-11                         # universal gravity constant in MKS
M_S = 1.99e30                         # mass of the sun in kilogram
AU = 1.486e11                         # astronomical unit in meters
JUPITER_R = 5 * AU                    # approximate Jupiter's distance from sun in meters (5AU)
JUPITER_V = (G*M_S/JUPITER_R) ** 0.5  # approximate orbital velocity of Jupiter
MIN_R = 0.1 * AU                      # closest approach to sun allowed
                                      # Parker Solar Probe MIN_R ~0.05 AU
DV_STEP = 50                          # delta_v increment between calculated combinations in m/s


def main_one_burn(max_dv):
	'''calculates the hyperbolic escape velocity of one '''


def main_two_burns(max_dv2, r0 = JUPITER_R, v0 = JUPITER_V):
	'''main function that calls other functions to calculate and plot the
	hyperbolic escape velocity
	inputs: maximum delta_v budget'''

    # TODO
    # calculate maximum delta_v for first burn - required to meet MIN_R
    # r0*(v0-max_dv1) = MIN_R
    max_dv1 = r0*v0

    # array of possible DV1 values
    v1_values = np.arange(0.0, max_dv1, step = DV_STEP)
    # array of possible DV2 values
    v2_values = np.arange(0.0, max_dv2, step = DV_STEP)
    # array of (dv1, dv2, v_infinity)
    v_infinities = np.zeroes((len(v1_values) * len(v2_values)), 3)

    # calculate v_infinity for every combination of dv_1 and dv_2
	for dv_i in range(len(v_infinities)):
		# look up delta_v of first burn
		dv1 = v1_values[int(math.floor(dv_i/len(v2_values)))]
		# look up delta_v of second burn
		dv2 = v2_values[dv_i % len(v2_values)]
		# fill in v1 values
		v_infinities[dv_i][0] = dv1
		# fill in v2_values
		v_infinities[dv_i][1] = dv2
		# call function to calculate v_infinity
		v_infinites[dv_i][2] = calc_vi(dv1, dv2, r0, v0)

	# plot plotting function 
	plot_vi(v_infinities)


	return

def calc_vi(dv1, dv2, r0, v0):
	'''calculates v_infinity based on the delta v
	of two burns. The starting distance from the sun and
	starting velocity are by default Jupiter's
	inputs: dv1 - change in velocity of retrograde burn
	        dv2 - change in velocity of escape burn
	        r0 - starting distance from sun
	        v0 - starting velocity
	outputs: v_infinity - hyperbolic excess velocity'''

    # calculate perihelion and velocity at perihelion
	rp, vp = calc_perhelion(dv1, r0, r0)

	v_infinity = ((vp + dv2)**2 - 2*M_S*G/rp) ** 0.5

	return v_infinity


def calc_perihelion(dv1, r0, v0):
	'''helper function for calc_vi. Calculates the perihelion
	and velocity at perihelion
	inputs: dv1 - delta v from first burn
	        r0 - starting distance from the sun
	        v0 - starting velocity'''
	a = (2/r0 - ((v0-dv1) ** 2)/G/M_S) ** -1  # calculate semi-major axis
	rp = 2*a - r0                           # calculate perihelion distance
	vp = r0*v0/rp                           # calculate velocity at perihelion

	return rp, vp                           # return perihelion and velocity

def calc_dv(rp, r0, v0):
	'''calculate '''

def plot_vi(data):
	'''plots v_infinity as a function of dv1 and dv2
	inputs: data - data to plot. List of lists with each
	               sublist made of triples (dv1, dv2, v_infinity)
	               Each sublist has the same total delta v'''

	return
