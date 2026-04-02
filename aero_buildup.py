# building an aerosandbox (aerobuildup) wing solver

import math
import aerosandbox as asb
from aerosandbox.geometry import Airplane, Wing, WingXSec, Airfoil
from aerosandbox.performance import OperatingPoint
from aerosandbox.aerodynamics.aero_3D.aero_buildup import AeroBuildup

from aerosandbox import cas

import aerosandbox as asb
import numpy as np
import matplotlib.pyplot as plt
from aerosandbox.geometry.airfoil import Airfoil

opti = asb.Opti()

# example var

span = 1.524
AR = opti.variable(init_guess=2, lower_bound=4, upper_bound=4)
chord = opti.variable(init_guess=0.381, lower_bound=0.381, upper_bound=0.7)
twist = opti.parameter() # opti.variable(lower_bound=0, upper_bound=5)
airspeed = 20
alpha = 0

opti.set_value(twist, 0)




# theta_Le = np.arctan(0.25*(chord - chord*taper_ratio)/(0.5-taper_location))

banner_length = opti.variable(init_guess=0.1, lower_bound=0)

# constants
span_constraint = 1.524

taper_location = 0.5 * 0.35 # 0.5 * 0.5 # opti.variable(init_guess=0.2, lower_bound=0.15, upper_bound=0.45) # 0.2

taper_ratio = 0.65 # opti.parameter() # opti.variable(init_guess=0.1, lower_bound=-1, upper_bound=1) # opti.variable(init_guess=0, lower_bound=-1, upper_bound=1) # 0.45

frontal_taper = -0.25 # opti.variable(init_guess=-0.1, lower_bound=-0.2, upper_bound=0.2) # -0.25 is straight LE

# opti.set_value(taper_location, 0.5*0.3)

# airfoil = asb.KulfanAirfoil("naca2412")

#coords = np.loadtxt("C:\\Users\\Kesha\\Downloads\\6041.dat", skiprows=1)
#x = coords[:, 0]
#y = coords[:, 1]

# airfoil = asb.KulfanAirfoil.to_kulfan_airfoil(x, y)

#irfoil = asb.KulfanAirfoil("naca2412")
#airfoil = asb.Airfoil("naca2412")

coords = np.loadtxt("C:\\Users\\Kesha\\Downloads\\sg6041-il.txt")
x, y = coords[:, 0], coords[:, 1]
# Normalize coordinates to unit chord (x goes from 0 → 1)
scale = np.max(x)
x = x / scale
y = y / scale
# Create Airfoil object
airfoil = Airfoil(
    name="SG6041",
    x_coordinates=x,
    y_coordinates=y
)

slope = (chord-taper_ratio*chord)/(taper_location-0.5) # slope
intercept = chord - slope * taper_location

MAC_tap = 1/(0.5 - taper_location) * ((slope/2*0.5**2 + intercept*0.5) - (slope/2*taper_location**2 + intercept*taper_location))
opti.subject_to(MAC_tap * (0.5 - taper_location)/0.5 + chord*taper_location/0.5 == 0.381)


# airfoil = Airfoil.from_dat("C:\\Users\\Kesha\\Downloads\\6041_new.dat")
"""
# --- enforce MAC = 0.381 m ---
MAC_target = 0.381

b2 = span / 2.0
y1 = span * taper_location
L = b2 - y1
tr = taper_ratio

A = y1 + (1.0 + tr)/2.0 * L
B = b2 + (tr - 1.0) * L + ((tr - 1.0)**2) * L / 3.0

# if chord is defined as span/AR in your code, constrain that expression:
opti.subject_to( (span / AR) == MAC_target * (A / B) )
"""


wing = asb.Wing(
    symmetric=True,
    xsecs=[
        asb.WingXSec(
            xyz_le=[
                -0.25 * chord,
                0,
                0
            ],
            chord=chord,
            twist=twist,
            airfoil=airfoil
        ),
        asb.WingXSec(
            xyz_le=[
                -0.25 * chord,
                span * taper_location,
                0
            ],
            chord=chord*1, # * 1 will determine taper ratio?
            twist=twist,
            airfoil=airfoil
        ),
        asb.WingXSec(
            xyz_le=[
                frontal_taper * chord,
                span * 0.5,
                0
            ],
            chord=chord*taper_ratio, # * 1 will determine taper ratio?
            twist=0,
            airfoil=airfoil
        )
    ]
)


airplane = Airplane(name="RectPlane", wings=[wing])

# --- Flight condition ---
op = OperatingPoint(velocity=20.0, alpha=0)

op_point = asb.OperatingPoint(
    velocity=airspeed,
    alpha=alpha
)

# --- Analysis ---
#ab = AeroBuildup(airplane=airplane, op_point=op)
#wing_results = ab.wing_aerodynamics(wing)
#e = wing_results.oswalds_efficiency

SPAN_RESOLUTION = 10
CHORCH_RESOLUTION = 5

vlm = asb.VortexLatticeMethod(
    airplane=airplane,
    op_point=op_point,
    spanwise_resolution=SPAN_RESOLUTION,
    chordwise_resolution=CHORCH_RESOLUTION,
    align_trailing_vortices_with_wind=True
)



aero = vlm.run()

score = aero["L"] / aero["D"]



opti.maximize(score)
sweep_core = np.linspace(0, 5, 20)
sweep_location = np.linspace(0.5*0.1, 0.5*0.6, 20)
sweep_ratio = np.linspace(0.01, 1, 20)


x_vals = []
y_vals = [] 

def to_percent_change(val):
    return (val - 1) * 100
"""
for a in sweep_ratio:
    opti.set_value(taper_ratio, a)
    # opti.set_value(twist, a)
    # opti.set_value(taper_location, a)
    sol = opti.solve()
    x_vals.append(sol(taper_ratio))
    #x_vals.append(sol(taper_location * 2))
    z = sol(aero["L"]/aero["D"]) / 94.64 # sol(aero["L"]/aero["D"]) / 9365
    # y_vals.append(z)
    y_vals.append(to_percent_change(z))
    #y_vals.append(to_percent_change(z))
"""

sol = opti.solve()

# print("twist", sol(twist))
"""

plt.title("Lift-to-drag ratio vs. Taper ratio (0.2)")
plt.plot(x_vals, y_vals)
plt.xlabel("Taper Ratio")
plt.ylabel("% Change in Lift-to-drag ratio")
plt.show()

"""


# print("taper loco", sol(taper_location))

# print(f"Aspect Ratio (AR): {span / chord:.3f}")
# print(f"Oswald efficiency e: {float(e):.4f}")



# we'll have the breakout here
# VLM root ...

# VLM tip ...

velocity = airspeed
alpha = alpha


op_point = asb.OperatingPoint(
    velocity=airspeed,
    alpha=alpha
)

SPAN_RESOLUTION = 2
CHORCH_RESOLUTION = 2

wing = asb.Wing(
    symmetric=True,
    xsecs=[
        asb.WingXSec(
            xyz_le=[
                -0.25 * sol(chord),
                0,
                0
            ],
            chord=sol(chord),
            twist=sol(twist),
            airfoil=airfoil
        ),
        asb.WingXSec(
            xyz_le=[
                -0.25 * sol(chord),
                span * sol(taper_location),
                0
            ],
            chord=sol(chord)*1, # * 1 will determine taper ratio?
            twist=sol(twist),
            airfoil=airfoil
        ),
        asb.WingXSec(
            xyz_le=[
                sol(frontal_taper) * sol(chord),
                span * 0.5,
                0
            ],
            chord=sol(chord)*sol(taper_ratio), # * 1 will determine taper ratio?
            twist=0,
            airfoil=airfoil
        )
    ]
)



airplane = Airplane(name="RectPlane", wings=[wing])


vlm = asb.VortexLatticeMethod(
    airplane=airplane,
    op_point=op_point,
    spanwise_resolution=SPAN_RESOLUTION,
    chordwise_resolution=CHORCH_RESOLUTION,
    align_trailing_vortices_with_wind=True
)


aero = vlm.run()

vlm.draw(show=True)

print("_ degrees of twist:", sol(twist))

slope = (chord-taper_ratio*chord)/(taper_location-0.5) # slope
intercept = chord - slope * taper_location

MAC_tap = 1/(0.5 - taper_location) * ((slope/2*0.5**2 + intercept*0.5) - (slope/2*taper_location**2 + intercept*taper_location))
MAC = MAC_tap * (0.5 - taper_location)/0.5 + chord*taper_location/0.5

tip_chord = slope*0.5+intercept

print("MAC check", sol(MAC))

print("Base chord", sol(chord))

print("Taper ratio", sol(taper_ratio))

print("Lift-to-drag ratio", sol(aero["L"]/aero["D"]))

