import aerosandbox as asb
import aerosandbox.numpy as np
import constants
import unit_conversion as uc

class Aircraft:

    def __init__(self, opti:asb.Opti, airfoil):

        # Mission Parameters
        self.passengers = opti.variable(init_guess=3)  
        self.cargo = opti.variable(init_guess=1)
        self.banner_length = opti.variable(init_guess = uc.inches2meters(10))

        # Wing Parameters
        self.span = opti.variable(init_guess=1.5)
        self.AR = opti.variable(init_guess=6)
        self.chord = self.span/self.AR
        self.wing_area = self.span * self.chord
        self.airfoil = asb.Airfoil(airfoil)
        self.CL_max = 1.4

        #Fuselage Parameters
        self.fuselage_length = opti.variable(init_guess=1.5)
        self.fuselage_width = opti.variable(init_guess = 0.1)
        self.fuselage_height = opti.variable(init_guess = 0.1)

        self.fuselage_box_length = self.fuselage_length - 2.5 * self.fuselage_width #this creates a shorter usable box area for payload calculations to account for the unusable nose and tail area

        #area constraints
        self.passenger_area = self.passengers*constants.DUCK_LENGTH*constants.DUCK_WIDTH #m^2
        self.battery_area = 0.011 #m^2
        self.total_area = (self.battery_area + self.passenger_area)*1.2

        #length constraints
        passenger_length = self.passenger_area/self.fuselage_width
        battery_length = self.battery_area/self.fuselage_width
        self.total_length = battery_length + passenger_length

        #volume constraints
        passenger_volume = self.passenger_area*constants.DUCK_HEIGHT
        puck_volume = (3.14*(constants.PUCK_DIAMETER/2)**2)*constants.PUCK_THICKNESS/constants.PUCK_PACKING_COEFFICEINT
        self.total_volume = ((puck_volume + passenger_volume)/0.7 + 0.05*0.05*0.15*3.5)/0.8



        self.frontal_area = self.fuselage_height * self.fuselage_width
        self.effective_diameter = np.sqrt(self.frontal_area/3.14)*2
        self.fineness_ratio = self.fuselage_length/self.effective_diameter
       
        self.fuselage_wetted_area = (
                            2*(self.fuselage_height * self.fuselage_width) + #front/back
                            2*(self.fuselage_height * self.fuselage_length) + #sides
                            2*(self.fuselage_width * self.fuselage_length)) #tops

        #Tail Parameters
        elevator_volume_coefficient = 0.4
        rudder_volume_coefficient = 0.04
        self.tail_arm = 0.8 #m

        self.h_stab_area = elevator_volume_coefficient * self.wing_area * self.chord / self.tail_arm
        self.v_stab_area = rudder_volume_coefficient * self.wing_area * self.span / self.tail_arm

        self.fuselageCD0 = self.getFuselageCD0(45, self.wing_area)    
        self.CD_banner = 0.04
        self.CD0_wing = 0.02
        self.CD_tail = 0.02
        

        # AP Parameters
        self.propulsion_energy = opti.variable(init_guess=constants.BATTERY_ENERGY * 3600) #Joules
 
        #Mass Calculations
        self.fuselage_mass = (2 * constants.CARBON_FIBER_DENSITY + constants.NOMEX_DENSITY) * self.fuselage_wetted_area
        self.wing_skin_mass = 2*((2 * constants.CARBON_FIBER_DENSITY + constants.NOMEX_DENSITY)) * self.wing_area
        self.payload_mass = (self.cargo*constants.CARGO_MASS + self.passengers*constants.PASSENGER_MASS) #kg
        self.structure_mass = self.payload_mass*0.1
        self.battery_mass = self.propulsion_energy / constants.BATTERY_SPECIFIC_ENERGY #kg
        self.banner_mass = constants.BANNER_SURFACE_DENSITY * (self.banner_length**2)/5 
        self.motor_mass = 0.450 #kg
        self.wiring_mass = 0.4 #kg
        self.landing_gear_mass = 0.250 #kg
        self.flight_mass = (self.battery_mass + 
                            self.fuselage_mass + 
                            self.wing_skin_mass +
                            self.landing_gear_mass +
                            self.structure_mass + 
                            self.motor_mass + 
                            self.wiring_mass)
        
        self.wetted_area = self.fuselage_wetted_area + self.wing_area*2 + (self.h_stab_area + self.v_stab_area)*2

    def getTotalMass (self, payload:bool, banner:bool):
        if payload:
            return self.flight_mass + self.payload_mass
        if banner:
            return self.flight_mass + self.banner_mass
        else:
            return self.flight_mass

    def getQ (self, speed):
        rho = constants.RHO
        Q = 0.5 * rho * (speed**2)
        return Q
    
    def getReynolds (self, speed, length): 
        return (constants.RHO * speed * length / constants.MEW)
    
    def getCL (self, speed, load_factor, payload:bool, banner:bool):
        total_mass = self.getTotalMass(payload, banner)
        weight = total_mass * constants.GRAVITATIONAL_ACCELERATION
        Q = self.getQ(speed)
        return weight * load_factor / (Q * self.wing_area)
    
    def getFuselageCD0 (self, speed, reference_area): #returns CD relative to given reference area. References https://aerotoolbox.com/drag-polar/, 
        L = self.fuselage_length
        D = self.effective_diameter
        Re = self.getReynolds(speed, L)
        skin_friction = 0.0391 * Re**(-0.157) #Skin friction references https://aerotoolbox.com/skin-friction/, possible issue with opti?
        return skin_friction * (1 + (60/((L/D)**3)) + 0.0025 * (L/D)) * self.fuselage_wetted_area / reference_area

    def getLift (self, speed, load_factor, payload:bool, banner:bool):
         CL = self.getCL(speed, load_factor, payload, banner)
         q = self.getQ(speed)
         return q*CL*self.wing_area
    
    def getDrag (self, speed, load_factor, payload:bool, banner:bool):
        #get basic parameters
        S = self.wing_area
        AR = self.AR  #aspect ratio
        Q = self.getQ(speed) #dynamic pressure 
       
        #Calculate Wing Total Drag Coefficient (Reference area is the wing planform, not wing wetted). Uses lifting line theory
        CL = self.getCL(speed, load_factor, payload, banner)
        e = 0.7 # Oswald efficiency factor
        k = 1 / (np.pi * e * AR) #induced drag term
        CD_Wing = self.CD0_wing + (k * CL**2)

        #Get fuselage drag coefficient (reference area is the wing planform again)
        CD_Fuselage = self.getFuselageCD0(speed, S) 

        #Calculate Drag Forces
        aircraft_drag = Q * (S * (CD_Fuselage + CD_Wing) + (self.CD_tail * (self.h_stab_area + self.v_stab_area)))
        banner_drag = Q * (self.CD_banner * self.banner_length**2)/5 ##investigate reynolds number effects on drag, using skin friction and also consider mast effects (look at naval architecture textbook)
        if banner:
            return aircraft_drag + banner_drag
        else:
            return aircraft_drag  
                        
    
