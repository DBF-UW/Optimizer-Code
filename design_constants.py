"""
Stores all useful constants

Resources
---------
Pink Foam Density
    https://www.homedepot.com/p/Owens-Corning-FOAMULAR-150-2-in-x-4-ft-x-8-ft-R-10-Scored-Squared-Edge-Rigid-Foam-Board-Insulation-Sheathing-45W/100320352
"""
import aerosandbox as asb
import aerosandbox.numpy as np

class constants_holder:
    def __init__(self, opti:asb.Opti):
        # =========== Driving Parameters ===========
        self.PROPULSION_EFFICIENCY_FACTOR = make_param(opti, 1)
        self.STRUCTURES_EXECUTION_FACTOR = make_param(opti, 1)
        self.FUSELAGE_PACKING_FACTOR = make_param(opti, 1)
        self.PARASITIC_DRAG_FACTOR = make_param(opti, 1)
        self.BANNER_CD_FACTOR = make_param(opti, 1)
        self.OSWALD_EFFICIENCY_FACTOR = make_param(opti, 1)
        self.GM_TIME_FACTOR = make_param(opti, 1)
        self.CL_MAX_FACTOR = make_param(opti, 1)
        self.REPORT_SCORE_FACTOR = make_param(opti, 1)

        # =========== PHYSICAL CONSTANTS ===========
        self.GRAVITATIONAL_ACCELERATION = 9.80665  # m/s^2
        self.EARTH_RADIUS = 6371e3  # meters
        self.R = 287.05  # J/(kg*K) gas constant for dry air
        self.PS = 101325  # Pa standard pressure
        self.RHO = 1.225  # kg/m^3 standard density
        self.MEW = 1.802 * 10**-5 #kg/m*s dynamic viscosity
        self.TS = 288.15  # K standard temperature
        self.SPECIFIC_HEAT_AIR_CONSTANT_PRESSURE = 1004  # J/(kg*K)
        self.SPECIFIC_HEAT_AIR_CONSTANT_VOLUME = 717  # J/(kg*K)

        # =========== ENVIROMENTAL CONSTANTS ========

        # =========== MATERIAL CONSTANTS ===========
        self.PINK_FOAM_DENSITY = 23.637083912 # kg/m^3
        self.LOAD_FACTOR_LIMIT = 8 # g's

        # =========== A&P CONSTANTS ============
        self.PROPULSION_EFFICIENCY = 0.7 * self.PROPULSION_EFFICIENCY_FACTOR # unitless
        self.BATTERY_ENERGY = 100  # Wh
        self.MOTOR_MASS = 0.5  # kg
        self.LG_MASS = 0.5  # kg
        self.BATTERY_SPECIFIC_ENERGY = 178000 # Wh/kg

        # =========== Mission Constants ===========
        self.PASSENGER_INCOME_FIXED = 6  # $/passenger
        self.PASSENGER_INCOME_LAP = 2  # $/passenger/lap
        self.CARGO_INCOME_FIXED = 10  # $/cargo
        self.CARGO_INCOME_LAP = 8  # $/cargo/lap
        self.BASE_OPERATING_COST = 10  # $/lap
        self.PER_PASSENGER_COST = 0.5  # $/passenger/lap
        self.PER_CARGO_COST = 2  # $/cargo/lap

        self.DUCK_WIDTH = 0.0584 #meters
        self.DUCK_HEIGHT =  0.0635 #meters
        self.DUCK_LENGTH = 0.0635 #meters

        self.PUCK_THICKNESS = 0.0254 #meters
        self.PUCK_DIAMETER = 0.0762 #meters
        self.PUCK_PACKING_COEFFICEINT = 0.65 #unitless

        self.PASSENGER_MASS = 0.02 + 0.01# KG
        self.CARGO_MASS = 0.170 # KG
        # =========== STRUCTURAL CONSTANTS ========
        self.STRUCTURAL_SAFETY_FACTOR = 1.5  # unitless
        self.WING_SURFACE_DENSITY = 2  # kg/m^2
        

        self.CARBON_FIBER_DENSITY = 0.088 #kg/m^2
        self.NOMEX_DENSITY = 0.058 #kg/m^2
        self.GOOP_MODIFIER = 1.12

        self.BANNER_SURFACE_DENSITY = 0.075 #kg/m^2

        # =========== 2024-2025 DBF REQS ===========
        self.AIAA_LENGTH = 1000 # ft

        self.MAX_WING_SPAN = 5 # ft
        self.MIN_WING_SPAN = 3 # ft

def make_param(opti, startingvalue):
    p = opti.parameter()
    opti.set_value(p, startingvalue)
    return p