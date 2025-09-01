#this will be the file for all aero functions for optimization

import numpy as np
import constants

def wing_weight(span, chord):
    densityCarbon = 88
    densityNomex = 58
    layersCarbon = 2
    layersNomex = 1
    goopModifier = 1.12
    span = 1.524
    chord = 0.1
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
    density = 0.15 # kg / m^2
    area = length * width
    mass = density * area
    return mass


def banner_drag(banner_length, banner_width, V):
    Cd_base = 1.2
    effective_area = banner_width * (0.3 * banner_length + banner_width)
    drag = 0.5 * constants.rho * V**2 * effective_area * Cd_base
    return drag



print(np.linspace(3, 200, 198))