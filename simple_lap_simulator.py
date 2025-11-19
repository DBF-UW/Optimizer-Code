import aerosandbox as asb
import aerosandbox.numpy as np  
import design_constants
import unit_conversion as uc
import aircraft
import constraints

class LapSimulator:
    #optimizer is allowed to decide radius and speed for turns and straights. 
    #This is used to compute lap time and energy consumption, which is fed back to optimizer and constraints for iteration.
    def __init__(self, opti:asb.Opti, aircraft, constants:design_constants.constants_holder, payload:bool, banner:bool):
        self.straight_speed = opti.variable(init_guess=40, lower_bound=0) #m/s
        self.turn_speed = opti.variable(init_guess=40, lower_bound = 0) #m/s
        self.turn_load_factor = opti.variable(init_guess=4, lower_bound=1.5) #g's
        leg_length = uc.feet2meters(constants.AIAA_LENGTH) #meters
        
        #Straights
        self.straight_drag = aircraft.getDrag(constants, self.straight_speed, 1, payload, banner)
        self.straight_CL = aircraft.getCL(constants, self.straight_speed, 1, payload, banner)
        self.straight_L_D = aircraft.getLift(constants, self.straight_speed, 1, payload, banner)/self.straight_drag
        self.straight_power = self.straight_drag*self.straight_speed

        #Turns
        turn_acceleration = np.sqrt(self.turn_load_factor**2 - 1) * constants.GRAVITATIONAL_ACCELERATION
        self.turn_radius = self.turn_speed**2 / turn_acceleration
        turn_drag = aircraft.getDrag(constants, self.turn_speed, self.turn_load_factor, payload, banner)
        self.turn_CL = aircraft.getCL(constants, self.turn_speed, self.turn_load_factor, payload, banner)
        self.turn_power = turn_drag * self.turn_speed

        self.turn_L_D = aircraft.getLift(constants, self.turn_speed, self.turn_load_factor, payload, banner)/turn_drag

        self.lap_energy = (self.straight_drag * (2 * leg_length) + turn_drag * (4 * np.pi * self.turn_radius)) / constants.PROPULSION_EFFICIENCY #Joules
        self.lap_time = (2 * leg_length / self.straight_speed) + (4*np.pi*self.turn_radius/self.turn_speed) #seconds
        self.laps_flown = aircraft.propulsion_energy / self.lap_energy
        self.energy_used = self.lap_energy * self.laps_flown #Joules
        self.total_time = self.laps_flown * self.lap_time #seconds
        


  

        #constraints
        opti.subject_to([
            self.straight_CL <= aircraft.CL_max,
            self.turn_CL <= aircraft.CL_max,
            self.laps_flown >= 3,
            self.turn_speed >= 13,
            self.straight_speed >= 13,
            self.straight_speed <= 22,
            self.turn_radius <= 30,
            self.turn_load_factor < 100,
            self.straight_speed <= self.turn_speed + 8,
            self.lap_energy*self.laps_flown <= aircraft.propulsion_energy, #total energy used must be less than battery energy
            self.lap_time*self.laps_flown <= 300, #5 minute flight time
        ])
    
