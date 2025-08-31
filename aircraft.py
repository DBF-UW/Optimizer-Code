import aerosandbox as asb
import aerosandbox.numpy as np
import constants
import unit_conversion as uc

class Aircraft:

    def __init__(self, opti:asb.Opti, airfoil):

        # Mission Parameters
        self.passengers = opti.variable(init_guess=3, lower_bound=3, upper_bound=500)  
        self.cargo = opti.variable(init_guess=1, lower_bound=1, upper_bound=500)
        self.banner_length = opti.variable(init_guess = uc.inches2meters(10), lower_bound=0.1)

        # Wing Parameters
        self.span = opti.variable(init_guess=1.5)
        self.chord = opti.variable(init_guess=0.3, lower_bound=0.05)
        self.AR = self.span/self.chord
        self.wing_area = self.span * self.chord
        self.airfoil = asb.Airfoil(airfoil)
        self.CL_max = 1

        #Fuselage Parameters
        self.passenger_area = self.passengers*constants.DUCK_LENGTH*constants.DUCK_WIDTH #m^2
        passenger_volume = self.passenger_area*constants.DUCK_HEIGHT
        puck_volume = (3.14*(constants.PUCK_DIAMETER/2)**2)*constants.PUCK_THICKNESS/constants.PUCK_PACKING_COEFFICEINT
        total_volume = ((puck_volume + passenger_volume)/0.7 + 0.05*0.05*0.15*2)/0.8

        self.fuselage_length = opti.variable(init_guess=1.5)
        self.fuselage_width = self.passenger_area/self.fuselage_length
        self.fuselage_height = total_volume/(self.fuselage_length*self.fuselage_width)

        self.frontal_area = self.fuselage_height * self.fuselage_width
        self.effective_diameter = np.sqrt(self.frontal_area/3.14)*2
        self.fineness_ratio = self.fuselage_length/self.effective_diameter
        
       
        self.fuselage_wetted_area = (
                            2*(self.fuselage_height * self.fuselage_width) + #front/back
                            2*(self.fuselage_height * self.fuselage_length) + #sides
                            2*(self.fuselage_width * self.fuselage_length)) #tops
                            
        self.CD_banner = 0.03
        self.CD0_wing = 0.02
        

        # AP Parameters
        self.propulsion_energy = opti.variable(init_guess=constants.BATTERY_ENERGY * 3600) #Joules
 
        #Mass Calculations
        self.empty_mass = 1.5 #kg
        self.payload_mass = (self.cargo*constants.CARGO_MASS + self.passengers*constants.PASSENGER_MASS) #kg
        self.structure_mass = self.payload_mass*0.3
        self.battery_mass = self.propulsion_energy / constants.BATTERY_SPECIFIC_ENERGY #kg
        self.flight_mass = self.empty_mass + self.battery_mass + self.structure_mass

    def getTotalMass (self, payload:bool):
        if payload:
            return self.flight_mass + self.payload_mass
        else:
            return self.flight_mass

    def getQ (self, speed):
        rho = constants.RHO
        Q = 0.5 * rho * (speed**2)
        return Q
    
    def getReynolds (self, speed, length): 
        return (constants.RHO * speed * length / constants.MEW)
    
    def getCL (self, speed, load_factor, payload:bool):
        total_mass = self.getTotalMass(payload)
        weight = total_mass * constants.GRAVITATIONAL_ACCELERATION
        self.q = self.getQ(speed)
        self.speed = speed
        return weight * load_factor / (self.q * self.wing_area)
    
    def getFuselageCD0 (self, speed, reference_area): #returns CD relative to given reference area. References https://aerotoolbox.com/drag-polar/, 
        L = self.fuselage_length
        D = self.effective_diameter
        Re = self.getReynolds(speed, L)
        skin_friction = 0.0391 * Re**(-0.157) #Skin friction references https://aerotoolbox.com/skin-friction/, possible issue with opti?
        return skin_friction * (1 + (60/((L/D)**3)) + 0.0025 * (L/D)) * self.fuselage_wetted_area / reference_area

    def getLift (self, speed, load_factor, payload:bool, banner:bool):
         CL = self.getCL(speed, load_factor, payload)
         q = self.getQ(speed)
         return q*CL*self.wing_area
    
    def getDrag (self, speed, load_factor, payload:bool, banner:bool):
        #get basic parameters
        S = self.wing_area
        AR = self.AR  #aspect ratio
        Q = self.getQ(speed) #dynamic pressure 
       
        #Calculate Wing Total Drag Coefficient (Reference area is the wing planform, not wing wetted). Uses lifting line theory
        CL = self.getCL(speed, load_factor, payload)
        e = 0.7 # Oswald efficiency factor
        k = 1 / (np.pi * e * AR) #induced drag term
        CD_Wing = self.CD0 + k * CL**2

        #Get fuselage drag coefficient (reference area is the wing planform again)
        CD_Fuselage = self.getFuselageCD0(speed, S) 

        #Calculate Drag Forces
        aircraft_drag = Q * S * (CD_Fuselage + CD_Wing) 
        banner_drag = Q * (self.CDBanner * self.banner_length**2)/5
        if banner:
            return aircraft_drag + banner_drag
        else:
            return aircraft_drag                           
    
