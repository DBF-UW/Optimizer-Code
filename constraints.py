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
    airfoil = aircraft.airfoil

    # assign constraints as list
    opti.subject_to([
        span <= uc.feet2meters(constants.MAX_WING_SPAN),
        span >= uc.feet2meters(constants.MIN_WING_SPAN),
        banner_length > uc.inches2meters(10), # minimum banner length
        passengers / cargo >= 3, #from AIAA rules
        passengers > 3, #from AIAA rules
        cargo > 1, #from AIAA rules
    ])

