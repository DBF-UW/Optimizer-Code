#this will be the file for all aero functions for optimization

import numpy as np
import constants
import casadi as ca

INCH_TO_M = 0.0254

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
    return wingWeight/1000 # kg


def banner_weight(length, width):
    density = 0.075 # kg / m^2
    area = length * width
    mass = density * area
    return mass

x = banner_weight(13.43, 2.69) + wing_weight(1.524, 3.549)

print(wing_weight(1.203, 2.012))

def banner_drag(banner_length, banner_width, V):
    Cd_base = 0.1
    effective_area = banner_width * banner_length
    drag = 0.5 * constants.rho * V**2 * effective_area * Cd_base
    return drag

def fus_drag(ducks, pucks, span, chord, V):
    duck_w = 2.15
    duck_l = 2.25
    duck_h = 2.5
    t_skin = 0.0015 # m
    t_core = 0.01 # m
    density_skin = 1600 # kg/m^3
    density_core = 65 # kg/m^3

    V_electric = 15
    V_duck = duck_w * duck_l * duck_h

    puck_d, puck_h = 3, 1
    V_puck = np.pi * (puck_d/2)**2 * puck_h
    V_total_in3 = ducks * V_duck + pucks * V_puck + V_electric

    V_total = 0.0254**3 * V_total_in3  

    W0 = duck_w * 0.0254
    H0 = duck_h * 0.0254
    A0 = W0 * H0
    L0 = V_total / (W0 * H0)
    H0 = H0 * 2
    W0 = W0 * 2
    L0 = V_total / (W0 * H0)
    A0 = W0 * H0
    R_wf = 1.072
    Cf_fus = 0.004
    swet_f = 2 * L0 * W0 + 2 * L0 * H0 + 2 * H0 * W0
    sref = span * chord
    dfeqiv = np.sqrt(4/np.pi * A0)
    Cd = R_wf * Cf_fus * (1 + 60/((L0/dfeqiv)**3) + 0.0025 * L0/dfeqiv) * swet_f/sref
    print("This is CD", Cd)

    sigma_skin = 2 * t_skin * density_skin
    sigma_core = t_core * density_core
    sigma = sigma_skin + sigma_core

    A_surf = 2 * (W0*H0 + W0*L0 + H0*L0)
    mass_fus = A_surf * sigma
    weight_N = mass_fus * constants.g
    Drag_N = Cd * 1.225 * V**2/2 * A_surf


    return {
        Drag_N, weight_N
    }

print(fus_drag(30, 10, 1.524, 0.381, 25))