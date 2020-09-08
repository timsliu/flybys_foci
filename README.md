# Flybys and Foci
This repository contains libraries for numerically approximating the flight
time of a spacecraft on a hyperbolic escape trajectory. The libraries were
written for the appendix of my short novel Flybys and Foci.

## Config
Excel files for configuring a trajectory. These excel files are read by the
script and used as inputs

## Output
Text files with the outputs of calculation.

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
approach light makes to the surface of the sun.

```
python3
import focal
focal.plot_foci(5)
```

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
two scenarios given a total delta-v budget of 100km/s.

## Graphs
The graphs directory is where charts are saved.
