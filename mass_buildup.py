# full mass buildup functions

import numpy as np
import constants
import casadi as ca

INCH_TO_M = 0.0254

def additional_ap_mass():

    # return kg

    hall_effect_sensor = 0.008
    fuse = 0.052
    on_off_switch = 0.009
    misc_wires = 0.167 * 3

    return hall_effect_sensor + fuse + on_off_switch + misc_wires

def wing_weight(span, chord):
    densityCarbon = 88
    densityNomex = 58
    layersCarbon = 2
    layersNomex = 1
    goopModifier = 1.12
    wingThickness = 0.0254
    internalStructureConstant = 0.042
    grossWingLoad = 28000
    internalStructureWeight = grossWingLoad * internalStructureConstant
    lengthWingwChord = 0.519*wingThickness+1.53
    lengthWing = lengthWingwChord * chord
    wingArea = span*lengthWing
    wingWeight = (densityCarbon*layersCarbon*wingArea+densityNomex*layersNomex*wingArea)+internalStructureWeight
    return wingWeight/1000/2 # kg

def towbar_weight(banner_length):
    return 0.02 * banner_length # this means its 0.0936 kg per meter of banner

def banner_weight(length, width):
    density = 0.1223 # kg / m^2
    area = length * width
    mass = density * area

    front_banner_mount = 0.0138333333333 * length
    aft_banner_mount = 0.0125 * length

    return mass + front_banner_mount + aft_banner_mount

def fuselage_weight(fus_wet_area):

    # this should include the fus skin + internal support structure + tail boom

    return (2 * constants.carbon_fiber_density + constants.nomex_density) * fus_wet_area * constants.fuse_weight_correction_factor

def fus_additional_mass(ducks, pucks): 

    esc_esc_mount = 0.133
    prop_pack = 0.723 # adjust this later possibly if needed
    duck_retention_mass = ducks * 0.11/3
    puck_retention_mass = pucks * 0.047
    avionics_mass = 0.145
    avionics_flight_controller_mass = 0.046
    avionics_mount = 0.030
    landing_gear_plus_mount = 0.320
    rear_gear_plus_mount = 0.050

    return (esc_esc_mount + prop_pack + duck_retention_mass + puck_retention_mass + avionics_mass + avionics_flight_controller_mass + avionics_mount + landing_gear_plus_mount + rear_gear_plus_mount)


def nose_section_mass(): 

    # all units in kg

    propellers_mass = 0.055 * 2 # kg
    spinner_mass = 0.030
    motor_cowling = 0.075
    motor_contra_config = 0.522
    standoffs = 0.043
    wire_plus_connector = 0.015

    return propellers_mass + spinner_mass + motor_cowling + motor_contra_config + standoffs + wire_plus_connector

def empenagge_mass():
    return 0.25 # kg, this should be updated to account for bigger planes

def cargo_mass(ducks, pucks):
    return ducks * 0.0198447 + pucks * 0.198447

def get_weight(span, chord, ducks, pucks, length, width, restraintWeight, fusArea):
    # _, fusweight = aero.fus_drag(ducks, pucks, span, chord, 0)
    return constants.g * constants.stuctures_correction_factor * (wing_weight(span, chord) + banner_weight(length, width) +        # wrote in to show full screen
                                                                  cargo_mass(ducks, pucks) + towbar_weight(length) + fuselage_weight(fusArea) + 
                                                                  nose_section_mass() + empenagge_mass() + additional_ap_mass() + fus_additional_mass(ducks, pucks))