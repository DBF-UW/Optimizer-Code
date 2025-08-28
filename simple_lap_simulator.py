import aerosandbox as asb
import aerosandbox.numpy as np  
import constants
import unit_conversion as uc
import aircraft
import constraints

class LapSimulator:
    def __init__(self, opti:asb.Opti, aircraft, payload:bool):
        self.speed = opti.variable(init_guess=40, lower_bound=0) #m/s
        self.turn_load_factor = opti.variable(init_guess=4, lower_bound=1.5, upper_bound=8) #g's
        lap_length = uc.feet2meters(constants.AIAA_LENGTH) #meters

        straight_drag = aircraft.getDrag(self.speed, 1, payload)
        self.straight_CL = aircraft.getCL(self.speed, 1, payload)

        #Turns
        turn_acceleration = np.sqrt(self.turn_load_factor**2 - 1) * constants.GRAVITATIONAL_ACCELERATION
        self.turn_radius = self.speed**2 / turn_acceleration
        turn_drag = aircraft.getDrag(self.speed, self.turn_load_factor, payload)
        self.turn_CL = aircraft.getCL(self.speed, self.turn_load_factor, payload)

        self.lap_energy = (straight_drag * (2 * lap_length) + turn_drag * (4 * np.pi * self.turn_radius)) / constants.PROPULSION_EFFICIENCY #Joules
        lap_length = 2 * lap_length + (4*np.pi*self.turn_radius) #meters
        self.lap_time = lap_length / self.speed #seconds
        self.laps_flown = aircraft.propulsion_energy / self.lap_energy
        self.energy_used = self.lap_energy * self.laps_flown #Joules
        self.total_time = self.laps_flown * self.lap_time #seconds

        #constraints
        opti.subject_to([
            self.straight_CL <= aircraft.CL_max,
            self.turn_CL <= aircraft.CL_max,
            self.laps_flown >= 3,
            self.turn_radius <= 15,
            self.lap_energy*self.laps_flown <= aircraft.propulsion_energy, #total energy used must be less than battery energy
            self.lap_time*self.laps_flown <= 300, #5 minute flight time
        ])
    
