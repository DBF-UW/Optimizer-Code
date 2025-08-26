import aerosandbox as asb
import aerosandbox.numpy as np  
import constants
import unit_conversion as uc
import aircraft
import constraints

class LapSimulator:
    def __init__(self, opti:asb.Opti, aircraft, payload:bool):
        self.speed = opti.variable(init_guess=40) #m/s
        self.turn_radius = opti.variable(init_guess=20, lower_bound=4, upper_bound=100) #meters
        lap_length = uc.feet2meters(constants.AIAA_LENGTH) #meters

        if payload:
            aircraft_mass = aircraft.flight_mass + aircraft.payload_mass
        else:
            aircraft_mass = aircraft.flight_mass

        #Straights
        straight_drag = aircraft.getDrag(self.speed, 1, payload)
        self.straight_CL = aircraft.getCL(self.speed, 1, payload)

        #Turns
        self.turn_load_factor = np.sqrt(1 + ((self.speed**2)/(constants.GRAVITATIONAL_ACCELERATION*self.turn_radius))**2)
        turn_drag = aircraft.getDrag(self.speed, self.turn_load_factor, payload)
        self.turn_CL = aircraft.getCL(self.speed, self.turn_load_factor, payload)

        self.lap_energy = (straight_drag * (2 * lap_length) + turn_drag * (4 * np.pi * self.turn_radius)) / constants.PROPULSION_EFFICIENCY #Joules
        lap_length = 2 * lap_length + (4*np.pi*self.turn_radius) #meters
        self.lap_time = lap_length / self.speed #seconds
        self.laps_flown = aircraft.propulsion_energy / self.lap_energy
        self.total_time = self.laps_flown * self.lap_time #seconds

        #constraints
        opti.subject_to([
            self.straight_CL <= aircraft.CL_max,
            self.turn_CL <= aircraft.CL_max,
            self.total_time <= 300 #seconds
        ])
    
