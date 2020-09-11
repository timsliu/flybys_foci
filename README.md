# Flybys and Foci
This repository contains libraries for numerically approximating the flight
time of a spacecraft on a hyperbolic escape trajectory. The libraries were
written for the appendix of my short novel Flybys and Foci and are used
to calculate three values:

1. Focal distance of a solar gravitational lens
2. Hyperbolic excess velocity of a spacecraft
3. Flight time to points a specified distance away from the sun

Below is a description of each subdirectory in this repo. The full scientific
appendix can be found on my [website] (https://timsliu.org/writing://timsliu.org/writing/)
and the book can be [purchased on Amazon](https://www.amazon.com/Flybys-Foci-Timothy-Liu/dp/1686812647/ref=sxts_sxwds-bia-wc-drs1_0?cv_ct_cx=flybys+and+foci&dchild=1&keywords=flybys+and+foci&pd_rd_i=1686812647&pd_rd_r=165a5c3b-1f94-484f-a4aa-a0d6e574c000&pd_rd_w=btT4J&pd_rd_wg=n0GOG&pf_rd_p=f3f1f1cd-8368-48df-ac69-94019fb84e3f&pf_rd_r=K88PR7YFCQ97A3DJQ9J2&psc=1&qid=1599859131&sr=1-1-f7123c3d-6c2e-4dbe-9d7a-6185fb77bc58).

## Config
The **config** directory stores Excel files for specifying the inputs
used in the flight time calculations. The inputs specify a flight plan and
are parsed by **flight_time.py**. Please see **flight_profile_template.xlsx**
for an example.

## Graphs
The **graphs** directory is where charts from all of the calculations are
saved.

## Output
The results of flight time calculations from **flight_time.py** are stored
in the **output** directory.

## Source
The flybys and foci library calculates three values:

1. Focal distance of a solar gravitational lens (focal.py)
2. Hyperbolic excess velocity of a spacecraft (oberth.py)
3. Flight time to points a specified distance away from the sun (flight_time.py)

There are several additional source files used across multiple calculations.
**orbit.py** is a library for calculating orbital parameters and **astro_constants.py**
has a list of astronomical and physical constants. The **evaluate.py** file simply
calls functions in other files with specified parameters.

### Focal distance
**focal.py**

Plots the focal distance from the sun of a gravitational lens given the closest
approach light makes to the surface of the sun. To run the function, use the commands:

```
python3
>>> import focal
>>> focal.plot_foci(5)
```

The argument passed to plot_foci specifies the upper limit for what is plotted. 
The gravitational focal point of light passing between 1 and 5 solar radii
from the sun will be plotted with the given arguments and saved to the
**graphs** directory. 

### Hyperbolic excess velocity
**oberth.py**

This file calculates the hyperbolic escape velocity of a spacecraft for two
scenarios given a starting heliocentric orbit:

1. A single instantaneous burn
2. Two burns, the first in a retrograde direction bringing the spacecraft
close to the sun followed by a second prograde burn.

There are two separate functions - the **compare** function compares the
hyperbolic escape velocity of the one burn and two burn scenario. Import 
the **oberth.py** library and call compare:

```
python3
>>> import oberth
>>> oberth.compare(20000)
```

which will generate a plot comparing the hyperbolic excess velocity of the
two scenarios given a total delta-v budget of 100km/s. Note that the argument
to compare is the delta-v budget in meters per second. The graphs are saved in
the **graphs** directory. Below is an example of the generated graph.


![Alt text](graphs/compare_20_kms.png?raw=true "20 km/s burn comparison")

The second function is **two_burns** which plots the hyperbolic escape
velocity under the two burn scenario (a retrograde burn to bring the perihelion
near the sun and a second prograde escape burn). The delta-v budget is split
between the two burns, and the final hyperbolic escape velocity for all
combinations is plotted.

```
python3
>>> import oberth
>>> oberth.two_burns(25000)
```

The argument passed is the maximum delta-v of the second burn, again in m/s. 
Below is an example of the generated graph

![Alt text](graphs/v_infinity.png?raw=true "25 km/s burn comparison")


### Flight time
**flight_time.py**
**spacecraft.py**

The third and most complicated calculation is flight time. The library
calculates the flight time to points a specified distance from the sun
assuming a non-instantaneous burn. Inputs to the calculation are specified
in an excel file in the **config** folder, includuing the delta-v budget,
the burn length, starting velocity, and final position. The functions
use a numerical approximation to calculate the time to reach the specified
final position. The results are saved as a text file in the **output**
folder.

To run the calculation, save a new flight profile using the template in
the **config** folder. If the flight profile is named **einstein_550.xlsx**
invoke the script using the commands:

```
python3
>>> import flight_time
>>> flight_time.open_flight_profile("einstein_550.xlsx")
```

**flight_time.py** parses the arguments and creates a new **spacecraft** 
object defined in **spacecraft.py**. This class contains methods for 
advancing the spacecraft through space while updating the velocity, position,
time elapsed, and other parameters. For details on how the calculations
are performed, see the inline documentation in **spacecraft.py**. The 
calculated flight time to reach the specified position is saved in the
**output** folder.

