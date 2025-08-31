"""
Stores general aircraft constraints

Resources
---------
    
"""
import aerosandbox as asb
import aerosandbox.numpy as np

import constants
import unit_conversion as uc
from aircraft import Aircraft

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
    
    # variables
    banner_length = aircraft.banner_length
    passengers = aircraft.passengers
    cargo = aircraft.cargo
    span = aircraft.span
    propulsion_energy = aircraft.propulsion_energy
    airfoil = aircraft.airfoil
    chord = aircraft.chord
    AR = aircraft.AR
    fuselage_length = aircraft.fuselage_length
    fuselage_width = aircraft.fuselage_width
    fuselage_height = aircraft.fuselage_height

    # assign constraints as list
    opti.subject_to([

        #AC Configuration Constraints
        span <= uc.feet2meters(constants.MAX_WING_SPAN),
        span >= uc.feet2meters(constants.MIN_WING_SPAN),
        AR >= 4, #minimum AR
        AR <= 12, #maximum AR
        propulsion_energy <= constants.BATTERY_ENERGY * 3600, #Battery energy limit
        propulsion_energy >= 0, #Minimum battery energy
        #Mission Constraints
        banner_length > uc.inches2meters(10), # minimum banner length
        banner_length < 20,
        passengers / cargo >= 3, #from AIAA rules
        passengers > 3, #from AIAA rules
        cargo > 1, #from AIAA rules
        fuselage_length > 0.07,
        fuselage_width > 0.07,
        fuselage_height > 0.07,
    ])

