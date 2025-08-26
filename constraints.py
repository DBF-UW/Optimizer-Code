"""
Stores general aircraft constraints

Resources
---------
    
"""
import aerosandbox as asb
import aerosandbox.numpy as np

import constants
import unit_conversion

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from optimization import Aircraft

def constraints(opti:asb.Opti, aircraft:"Aircraft") -> None:
    """
    Assigns constraints to optimizer.

    Parameters
    ----------
    opti : asb.Opti
        Aerosandbox optimizer.
    aircraft : Aircraft
        Aircraft object.

    Returns
    -------
    """
    
    # constants - defined in constants.py e.g. MAX_WING_SPAN
    # variables
    banner_length = aircraft.banner_length
    banner_width = aircraft.banner_width
    passengers = aircraft.passengers
    cargo = aircraft.cargo
    airspeed = aircraft.airspeed
    alpha = aircraft.alpha
    span = aircraft.span
    chord = aircraft.chords
    airfoil = aircraft.airfoil
    aero = aircraft.aero

    stall = aircraft.get_stall()
    takeoff = aircraft.get_takeoff()

    lift = aircraft.get_lift()
    drag = aircraft.get_drag(turn=True)

    turn_radius = aircraft.get_min_turning_radius()
    lap_time = aircraft.get_lap_time() # approx

    total_weight = aircraft.get_weight()
    #payload = aircraft.get_weight(payload=True)
    fuselage_weight = aircraft.fuse_w
    wing_weight = total_weight - fuselage_weight

    wing_area = aircraft.wing.area()
    wing_density = aircraft.wing_density

    load_factor = aircraft.get_load_factor()

    # models
    aspect_ratio = aircraft.wing.aspect_ratio()

    # assign constraints as list
    opti.subject_to([
        span <= unit_conversion.feet2meters(constants.MAX_WING_SPAN),
        airspeed > stall,
        banner_length / banner_width <= 5,
        passengers / cargo >= 3,
        turn_radius >= 0, # real turn radius
        lift > total_weight, # level flight limit
        load_factor < constants.LOAD_FACTOR_LIMIT, # structural limit
        drag < constants.DYNAMIC_THRUST(airspeed), # thrust vs drag limit
        takeoff < unit_conversion.feet2meters(constants.AIAA_LENGTH) / 2, # takeoff limit
        stall < 10 # stall speed for low speed flight
    ])
    
    # airfoil optimization constraints
    #this all shouldn't matter
    if airfoil.name == "optimized":
        CL_multipoint_targets = np.array([0.8, 1.0, 1.2, 1.4, 1.5, 1.6])

        aero = airfoil.get_aero_from_neuralfoil(
            alpha=alpha,
            Re=500e3 * (CL_multipoint_targets / 1.25) ** -0.5, # pick multiple different reynolds numbers
            mach=0.03, # select mach number, subsonic is < 1, 0.02 to 0.1 is a good approximation for now
        )

        opti.subject_to([
            aero["analysis_confidence"] > 0.90, # ensure confidants
            #np.diff(alpha) > 0, # not applicable for single alpha value
            #aero["CM"] >= -0.133, # ensure proper moment, commented out becuase this can be accounted for in static stability, we generally ignore this
            airfoil.local_thickness(x_over_c=0.33) >= 0.128, # ensure thickness
            airfoil.local_thickness(x_over_c=0.90) >= 0.014, # ensure thickness
            airfoil.lower_weights[0] < -0.05, # 
            airfoil.upper_weights[0] > 0.05,
            airfoil.local_thickness() > 0, # no negitive thicknesses
        ])

