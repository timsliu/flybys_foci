#oberth.py




# constants

G =       #universal gravity constant
M_S =     # mass of the sun in kilogram
JUPITER_R = # approximate Jupiter's distance from the sun
JUPITER_V = # approximate orbital velocity of Jupiter
MAX_DV1 = # maximum dv1 to keep Einstein at least x solar radii away from the sun
NUM_DV_COMBO = # number of different DV combinations to calculate for each total dv


def main(total_dv):
	'''main function that calls other functions to calculate and plot the
	hyperbolic escape velocity
	inputs: total_dv - list of total delta-v budget lines to plot. This budget is
	        distributed between the first perihelion reduction burn and the
	        second escape burn'''

    # allocate array for holding v_infinty as a function of dv1 and dv2
    # each sublist has an identical total dv for each element
    # each element of a sublist is a list [dv1, dv2, v_infinity]
    # for each element of a sublist dv1 + dv2 = total_dv[i]
    v_infinities = np.zeroes((len(total_dv), NUM_DV_COMBO, 3))
    # array of possible DV1 values
    v1_values = np.linspace(0.0, MAX_DV1, num = NUM_DV_COMBO)
    # fill in the delta_vs in the v_infinities array
	for dv_i, dv in enumerate(total_dv):
		# for each elemenet of a sublist
		for i in range(NUM_DV_COMBO):




	return

def calc_vi(dv1, dv2, r0 = JUPITER_R, v0 = JUPITER_V):
	'''calculates v_infinity based on the delta v
	of two burns. The starting distance from the sun and
	starting velocity are by default Jupiter's
	inputs: dv1 - change in velocity of retrograde burn
	        dv2 - change in velocity of escape burn
	        r0 - starting distance from sun
	        v0 - starting velocity
	outputs: v_infinity - hyperbolic excess velocity'''


	return v_infinity


def calc_rp(dv1, r0, v0):
	'''helper function for calc_vi. Calculates the perihelion
	and velocity at perihelion
	inputs: dv1 - delta v from first burn
	        r0 - starting distance from the sun
	        v0 - starting velocity'''

def plot_vi(data):
	'''plots v_infinity as a function of dv1 and dv2
	inputs: data - data to plot. List of lists with each
	               sublist made of triples (dv1, dv2, v_infinity)
	               Each sublist has the same total delta v'''

	return
