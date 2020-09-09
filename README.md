# Flybys and Foci
This repository contains libraries for numerically approximating the flight
time of a spacecraft on a hyperbolic escape trajectory. The libraries were
written for the appendix of my short novel Flybys and Foci and are used
to calculate three values:

1. Focal distance of a solar gravitational lens
2. Hyperbolic excess velocity of a spacecraft
3. Flight time to points a specified distance away from the sun

Below is a description of each subdirectory in this repo.

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
2. Hyperbolic excess velocity of a spacecraft
3. Flight time to points a specified distance away from the sun

There are several miscellaneous source files used across multiple calculations.
**orbit.py** is a library for calculating orbital parameters and **astro_constants.py**
has a list of astronomical and physical constants. The **evaluate** file simply
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

The argument passed to plot_foci specifies upper limit for what is plotted. 
The gravitational focal point of light passing between 1 and 5 solar radii from the sun will be plotted. 

### Hyperbolic excess velocity
**oberth.py**

This file calculates the hyperbolic escape velocity of a spacecraft for two
scenarios given a starting heliocentric orbit:

1. A single instantaneous burn
2. Two burns, the first in a retrograde direction bringing the spacecraft
close to the sun followed by a second prograde burn.

The entry point for this calculation is the function **compare**. Import
the **oberth.py** library and call compare:

```
python3
>>> import oberth
>>> oberth.compare(100)
```

which will generate a plot comparing the hyperbolic excess velocity of the
two scenarios given a total delta-v budget of 100km/s. The graphs are saved in
the **graphs** directory.

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
the **config** folder. If the flight profile is named **pluto_flight.xlsx**
invoke the script using the commands:

```
python3
>>> import flight_time
>>> flight_time.open_flight_profile("pluto_flight.xlsx")
```

**flight_time.py** parses the arguments and creates a new **spacecraft** 
object defined in **spacecraft.py**. This class contains methods for 
advancing the spacecraft through space while updating the velocity, position,
time elapsed, and other parameters. For details on how the calculations
are performed, see the inline documentation in **spacecraft.py**.

