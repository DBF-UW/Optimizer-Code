import aerosandbox as asb
import aerosandbox.numpy as np
import constants
import unit_conversion as uc

class Aircraft:
    def __init__(self, opti:asb.Opti, airfoil):

        # Mission Parameters
        self.passengers = opti.variable(init_guess=6, lower_bound=3)  
        self.cargo = opti.variable(init_guess=2, lower_bound=1)
        self.banner_length = opti.variable(init_guess = uc.inches2meters(10), lower_bound=0.1)



        # Wing Parameters
        self.span = uc.feet2meters(constants.MAX_WING_SPAN)
        self.chord = opti.variable(init_guess=0.3, lower_bound=0.05)
        self.AR = self.span/self.chord
        self.wing_area = self.span * self.chord
        self.airfoil = asb.Airfoil(airfoil)
        self.CL_max = self.airfoil.CL_max

        #Flight Parameters
        self.max_load_factor = opti.variable(init_guess=4, lower_bound=1)

        # AP Parameters
        self.propulsion_energy = opti.variable(init_guess=100*3600)

        
        #Mass Calculations
        self.empty_mass = 2 #kg
        self.payload_mass = (self.cargo*constants.CARGO_MASS + self.passengers*constants.PASSENGER_MASS) #kg
        self.battery_mass = self.propulsion_energy / constants.BATTERY_SPECIFIC_ENERGY #kg
        self.flight_mass = self.empty_mass + self.battery_mass

    
    def getWingMass(self, max_load_factor, mass):
        wing_area = self.wing_area
        wing_surface_mass = constants.WING_SURFACE_DENSITY * wing_area  # kg/m^2
        structural_safety_factor = constants.STRUCTURAL_SAFETY_FACTOR  # unitless
        wing_structure_mass = (mass * max_load_factor * 0.1) * structural_safety_factor + wing_surface_mass # kg

    def getDrag(self, airspeed, load_factor):
        q = 0.5 * constants.RHO * airspeed**2 # Dynamic pressure
        lift = load_factor * self.mass * constants.GRAVITATIONAL_ACCELERATION
        CL = lift / (q * self.wing_area) 
        CD0 = 0.02  # Parasite drag coefficient, assumed constant
        e = 0.8  # Oswald efficiency factor, assumed constant
        CDi = CL**2 / (np.pi * e * self.AR)  # Induced drag coefficient
        CD = CD0 + CDi
        D = CD * q * self.S
        return D
    
    def getCL(self, airspeed, load_factor):
        q = 0.5 * constants.RHO * airspeed**2 # Dynamic pressure
        lift = load_factor * self.mass * constants.GRAVITATIONAL_ACCELERATION
        CL = lift / (q * self.wing_area) 
        return CL
    
