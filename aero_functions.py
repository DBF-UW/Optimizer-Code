#this will be the file for all aero functions for optimization, now serving as the drag buildup model

import numpy as np
import constants
import casadi as ca

INCH_TO_M = 0.0254

mu = 1.81e-5 # won't load for some reason
rho = 1.225 

def get_Reynolds(length, velocity):
    
    return rho * velocity * length / mu

# this is Lincolns fuselage drag function below:

def getFuselageCD0 (fuselage_length, effective_diameter, speed, fuselage_wetted_area, reference_area): #returns CD relative to given reference area. References https://aerotoolbox.com/drag-polar/, 
        
        L = fuselage_length
        D = effective_diameter
        Re = get_Reynolds(L, speed)
        skin_friction = 0.0391 * Re**(-0.157) #Skin friction references https://aerotoolbox.com/skin-friction/, possible issue with opti?
        return skin_friction * (1 + (60/((L/D)**3)) + 0.0025 * (L/D)) * fuselage_wetted_area / reference_area * constants.fus_drag_correction_factor

def get_banner_cd(reynolds):

    return 0.02

    return ca.if_else(
    reynolds > 5e5,
    1.552e5 * reynolds**(-0.9942) - 7e-3,
    1.552e5 * (5e5)**(-0.9942) - 7e-3
    )

def get_wing_cd0(chord, velocity):
     reynolds = get_Reynolds(chord, velocity)
     r_wf = 1.072 # wing fus interference factor
     r_LS = 1.065 # lifting surface correction factor: https://aerotoolbox.com/lifting-surface-correction/
     Cf_wing = flat_plate_Cf(reynolds)
     L_star = 1.2
     thickness_chord_rat = 0.1
     wet_to_ref = 1.976 # correction factor based on CFD

     return r_wf * r_LS * Cf_wing * (1 + L_star * thickness_chord_rat + 100 * (thickness_chord_rat)**4) * wet_to_ref

def flat_plate_Cf(reynolds):
     
     # https://aerotoolbox.com/skin-friction/ 

     A = 0.0391
     B = -0.157
     return A * (reynolds)**(B)

def landing_gear_drag(aircraft_weight): 
     return 

def banner_drag(banner_length, banner_width, V, Cd):
    # Cd_base = 0.021 # 0.05
    effective_area = banner_width * banner_length
    drag = 0.5 * rho * V**2 * effective_area * Cd
    return drag

def prop_efficiency(prop):
    return prop # 2*V/35*np.e**((1-V)/35) # randomly chatgpt'd smooth curve for propulsive efficiency

def energy_usable(prop):
    return constants.batteryCapacity * prop * 3600

def aircraft_CD():
     return get_total_CD0() + get_CDI()

def get_CDI(CL, AR):
     return CL**2 / (AR * np.pi * constants.oswaldEff)

def get_CD0_tail(swet_ht, swet_vt, S):
     return constants.Cfe_tail * (swet_ht + swet_vt) / S

def get_total_CD0(wing, fus, tail):
     # gives total CD0 for aircraft
     
     correction_factor = 1.3
     return correction_factor * (wing + fus + tail)

"""
archived fus drag

def fus_drag(length, dfequiv, Swet_f, Sref_w, V):            # this is the function that I wrote
    R_wf = 1.072
    Cf_fus = 0.004
    Cd = R_wf * Cf_fus * (1 + 60/((length/dfequiv)**3) + 0.0025 * length/dfequiv) * Swet_f / Sref_w
    print("This is CD", Cd)

    Drag_N = Cd * 1.225 * V**2/2 * Swet_f

    return Drag_N

"""