import aerosandbox as asb
import aerosandbox.numpy as np
import constants
import unit_conversion as uc

class Aircraft:
    def __init__(self, opti:asb.Opti, airfoil):

        # Mission Parameters
        self.passengers = opti.variable(init_guess=6, lower_bound=3, upper_bound=500)  
        self.cargo = opti.variable(init_guess=2, lower_bound=1, upper_bound=500)
        self.banner_length = opti.variable(init_guess = uc.inches2meters(10), lower_bound=0.1)



        # Wing Parameters
        self.span = opti.variable(init_guess=1.5)
        self.chord = opti.variable(init_guess=0.3, lower_bound=0.05)
        self.AR = self.span/self.chord
        self.wing_area = self.span * self.chord
        self.airfoil = asb.Airfoil(airfoil)
        self.CL_max = 1.6

        #Flight Parameters

        # AP Parameters
        self.propulsion_energy = opti.variable(init_guess=constants.BATTERY_ENERGY * 3600) #Joules

        
        #Mass Calculations
        self.empty_mass = 4 #kg
        self.payload_mass = (self.cargo*constants.CARGO_MASS + self.passengers*constants.PASSENGER_MASS) #kg
        self.battery_mass = self.propulsion_energy / constants.BATTERY_SPECIFIC_ENERGY #kg
        self.flight_mass = self.empty_mass + self.battery_mass

    def getTotalMass (self, payload:bool):
        if payload:
            return self.flight_mass + self.payload_mass
        else:
            return self.flight_mass

    def getQ (self, speed):
        rho = constants.RHO
        Q = 0.5 * rho * (speed**2)
        return Q
    
    def getCL (self, speed, load_factor, payload:bool):
        total_mass = self.getTotalMass(payload)
        weight = total_mass * constants.GRAVITATIONAL_ACCELERATION
        self.q = self.getQ(speed)
        self.speed = speed
        return weight * load_factor / (self.q * self.wing_area)
    
    def getDrag (self, speed, load_factor, payload:bool):
        CL = self.getCL(speed, load_factor, payload)
        CD0 = 0.025
        e = 0.8 # Oswald efficiency factor
        AR = self.AR   
        k = 1 / (np.pi * e * AR)
        CD = CD0 + k * CL**2
        q = self.getQ(speed)   
        return CD * q * self.wing_area                                      
    
