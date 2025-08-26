"""
Main script to optimize aircraft

Resources
---------
"""

import Optimization
import constants
import constraints
import missions
import argparse

import unit_conversion as units

# argparse for more flexible optimizations
parser = argparse.ArgumentParser()
parser.add_argument(
    "-a", "--optimize-airfoil",
    action="store_true",
    help="Flag to perform optimizations on airfoil. Very slow"
)
args = parser.parse_args()


# define functions
constraint_function = constraints.constraints
mission_2 = missions.mission_2
mission_3 = missions.mission_3

# optimize
optimizer = Optimization.Optimizer(
    airfoil= "opti" if args.optimize_airfoil else "e216", 
    fuse_weight=20, 
    wing_density=constants.PINK_FOAM_DENSITY,
)
scores, crafts = optimizer.solve_missions(constraint_function, mission_2, mission_3)

# print score and plot
for mission, score, craft in zip(["MISSION 2", "MISSION 3", "OPTIMIAL"], scores, crafts):
    print(mission)
    print("Score:", score)
    print("CL:", craft.aero["CL"])
    print("CD:", craft.aero["CD"])
    print("Lift:", craft.get_lift(), 'N')
    print("Weight:", craft.get_weight(), 'N  ->  ', units.newtons2lbf(craft.get_weight()), 'lbf')
    print("Drag:", craft.get_drag(turn=True), 'N')
    print("Thrust:", constants.DYNAMIC_THRUST(craft.airspeed), 'N')
    print("Airspeed:", craft.airspeed, "m/s")
    print("Takeoff:", units.meters2feet(craft.get_takeoff()), "ft")
    print("Load Factor:", craft.get_load_factor(), "g's")
    print("Root Chord:", craft.chords[0], 'm')
    print("Tip Chord:", craft.chords[1], 'm')
    print("Span:", craft.span, 'm')
    print("Alpha:", craft.alpha)
    print("Stall:", craft.get_stall(), 'm/s')
    print("Passengers (Rubber Ducks): ", craft.passengers)
    print("Cargo (hockey pucks): ", craft.cargo)
    print("Banner Length: ", craft.banner_length)
    print("Banner Width: ", craft.banner_width)
    craft.plot_vlm()
    craft.wing.draw()