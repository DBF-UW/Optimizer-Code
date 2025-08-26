import aerosandbox as asb
import aerosandbox.numpy as np  
import constants
import unit_conversion as uc
import aircraft
import constraints

class LapSimulator:
    def __init__(self, opti:asb.Opti, aircraft, payload:bool):
        speed = opti.variable(init_guess=40) #m/s
        turn_radius = opti.variable(init_guess=20, lower_bound=4, upper_bound=100) #meters
        lap_length = uc.feet2meters(constants.AIAA_LENGTH) #meters

        if payload:
            aircraft_mass = aircraft.flight_mass + aircraft.payload_mass
        else:
            aircraft_mass = aircraft.flight_mass

        #Straights
        straight_drag = aircraft.getDrag(speed, 1)
        self.straight_CL = aircraft.getCL(speed, 1)

        #Turns
        self.turn_load_factor = np.sqrt(1 + ((speed**2)/(constants.GRAVITATIONAL_ACCELERATION*turn_radius))**2)
        turn_drag = aircraft.getDrag(speed, self.turn_load_factor)
        self.turn_CL = aircraft.getCL(speed, self.turn_load_factor)

        self.lap_energy = (straight_drag * (2 * lap_length) + turn_drag * (4 * np.pi * turn_radius)) / constants.PROPULSION_EFFICIENCY #Joules
        lap_length = 2 * lap_length + (4*np.pi*turn_radius) #meters
        self.lap_time = lap_length / speed #seconds
        self.laps_flown = aircraft.propulsion_energy / self.lap_energy
        self.total_time = self.laps_flown * self.lap_time #seconds

        #constraints
        opti.subject_to([
            self.straight_CL <= aircraft.CL_max,
            self.turn_CL <= aircraft.CL_max,
            self.total_time <= 300 #seconds
        ])
    
