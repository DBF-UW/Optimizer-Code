"""
Stores current mission functions

Resources
---------
AIAA Previous Rules
    https://www.aiaa.org/dbf/previous-competitions
"""
import aerosandbox as asb
import aerosandbox.numpy as np

from casadi import casadi

import constants

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from optimization import Aircraft

def ground_mission(opti:asb.Opti, aircraft:"Aircraft", normalizer:float=1.0) -> casadi.MX:
    """
    Ground mission score function.

    Parameters
    ----------
    opti : asb.Opti
        Aerosandbox optimizer.
    aircraft : Aircraft
        Aircraft object.
    normalizer : float
        Best score to normalize by.

    Returns
    -------
    casadi.MX
        Score variable.
    """
    #### DUMMY SCORE ####
    x = opti.variable(init_guess=100)
    score = x * x

    opti.subject_to(score < 10)

    # score function
    return score

def mission_1(opti:asb.Opti, aircraft:"Aircraft", normalizer:float=1.0) -> casadi.MX:
    """
    Mission 1 score function.

    Parameters
    ----------
    opti : asb.Opti
        Aerosandbox optimizer.
    aircraft : Aircraft
        Aircraft object.
    normalizer : float
        Best score to normalize by.

    Returns
    -------
    casadi.MX
        Score variable.
    """

    # score function
    return constants.MISSION_1_POINTS

def mission_2(opti:asb.Opti, aircraft:"Aircraft", normalizer:float=1.0) -> casadi.MX:
    """
    Mission 2 score function.

    Parameters
    ----------
    opti : asb.Opti
        Aerosandbox optimizer.
    aircraft : Aircraft
        Aircraft object.
    normalizer : float
        Best score to normalize by.

    Returns
    -------
    casadi.MX
        Score variable.
    """
    lap_time = aircraft.get_lap_time()
    laps = constants.MISSION_2_TIME / lap_time
    passengers = aircraft.get_passengers()
    cargo = aircraft.get_cargo()
    Income = (passengers * (constants.LP1 + (constants.LP2 * laps))) + (cargo * (constants.LC1 + (constants.LC2 * laps)))
    Cost = laps * (constants.CE + (passengers * constants.CP) + (cargo * constants.CC)) * constants.EF
    Net_Income = Income - Cost

    # score function
    return constants.MISSION_2_POINTS + (Net_Income) / normalizer

def mission_3(opti:asb.Opti, aircraft:"Aircraft", normalizer:float=1.0) -> casadi.MX:
    """
    Mission 3 score function.

    Parameters
    ----------
    opti : asb.Opti
        Aerosandbox optimizer.
    aircraft : Aircraft
        Aircraft object.
    normalizer : float
        Best score to normalize by.

    Returns
    -------
    casadi.MX
        Score variable.
    """
    lap_time = aircraft.get_lap_time()
    laps = constants.MISSION_3_TIME / lap_time

    banner_length = aircraft.get_banner_length()

    RAC = 0.75 + 0.15 * aircraft.get_wingspan()
    # score function
    return constants.MISSION_3_POINTS + ((laps * banner_length) / RAC) / normalizer