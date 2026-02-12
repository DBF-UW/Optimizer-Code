import aerosandbox as asb
import aerosandbox.numpy as np  
import design_constants
import unit_conversion as uc
import aircraft
import constraints

class LapSimulator:
    #optimizer is allowed to decide radius and speed for turns and straights. 
    #This is used to compute lap time and energy consumption, which is fed back to optimizer and constraints for iteration.
    def __init__(self, opti:asb.Opti, aircraft, constants:design_constants.constants_holder, payload:bool, banner:bool, cross_wind, head_wind):

        # Lap Profile Parameters
        self.propulsion_energy = opti.variable(init_guess=constants.BATTERY_ENERGY * 3600) #Joules

        self.upwind_groundspeed = opti.variable(init_guess=40, lower_bound=0) #upwind leg ground speed in m/s
        self.downwind_groundspeed = opti.variable(init_guess=40, lower_bound=head_wind) #downwind leg ground speed in m/s, slowest you can go is the headwind speed (0m/s airspeed)

        self.turn_speed = opti.variable(init_guess=40, lower_bound = 0) #m/s
        self.turn_load_factor = opti.variable(init_guess=4, lower_bound=1.5) #g's

        leg_length = uc.feet2meters(constants.AIAA_LENGTH) #meters

        # Calculate airspeeds and leg lengths
        self.upwind_airspeed = np.sqrt((self.upwind_groundspeed + head_wind)**2 + cross_wind**2)
        self.downwind_airspeed = np.sqrt((self.downwind_groundspeed- head_wind)**2 + cross_wind**2)

        self.upwind_length = (leg_length/self.upwind_groundspeed) * (self.upwind_airspeed) #this is the time to complete the leg (which uses ground leg length and groundspeed) multiplied by the airspeed
        self.downwind_length = (leg_length/self.downwind_groundspeed) * (self.downwind_airspeed) #this is the time to complete the leg (which uses ground leg length and groundspeed) multiplied by the airspeed
        
        #Calculate upwind performance
        self.upwind_drag = aircraft.getDrag(constants, self.upwind_airspeed, 1, payload, banner)
        self.upwind_CL = aircraft.getCL(constants, self.upwind_airspeed, 1, payload, banner)
        self.upwind_L_D = aircraft.getLift(constants, self.upwind_airspeed, 1, payload, banner)/self.upwind_drag

        self.upwind_power = self.upwind_drag*self.upwind_airspeed
        self.upwind_energy = self.upwind_drag * self.upwind_length
        self.upwind_time = leg_length/self.upwind_groundspeed

        #Calculate downwind performance
        self.downwind_drag = aircraft.getDrag(constants, self.downwind_airspeed, 1, payload, banner)
        self.downwind_CL = aircraft.getCL(constants, self.downwind_airspeed, 1, payload, banner)
        self.downwind_L_D = aircraft.getLift(constants, self.downwind_airspeed, 1, payload, banner)/self.downwind_drag

        self.downwind_power = self.downwind_drag*self.downwind_airspeed
        self.downwind_energy = self.downwind_drag * self.downwind_length
        self.downwind_time = leg_length/self.downwind_groundspeed

        #Calculate 180 turn performance
        turn_acceleration = np.sqrt(self.turn_load_factor**2 - 1) * constants.GRAVITATIONAL_ACCELERATION
        self.turn_radius = self.turn_speed**2 / turn_acceleration

        self.turn_drag = aircraft.getDrag(constants, self.turn_speed, self.turn_load_factor, payload, banner)
        self.turn_CL = aircraft.getCL(constants, self.turn_speed, self.turn_load_factor, payload, banner)
        self.turn_L_D = aircraft.getLift(constants, self.turn_speed, self.turn_load_factor, payload, banner)/self.turn_drag

        self.turn_power = self.turn_drag * self.turn_speed
        self.turn_energy = self.turn_drag * np.pi * self.turn_radius
        self.turn_time = np.pi * self.turn_radius / self.turn_speed

        #Calculate lap performance

       
        self.lap_energy = self.upwind_energy + self.downwind_energy + 4*self.turn_energy #joules
        self.lap_time = self.upwind_time + self.downwind_time + 4*self.turn_time #seconds
        self.laps_flown = self.propulsion_energy * constants.PROPULSION_EFFICIENCY / self.lap_energy
        self.energy_used = self.lap_energy * self.laps_flown #Joules
        self.total_time = self.laps_flown * self.lap_time #seconds
        
        #constraints
        opti.subject_to([
            #stall protection
            self.upwind_CL <= aircraft.CL_max,
            self.downwind_CL <= aircraft.CL_max,
            self.turn_CL <= aircraft.CL_max,

            #reasonability constraints
            self.laps_flown >= 3,
            self.turn_speed >= 20,
            self.upwind_airspeed >= 20,
            self.downwind_airspeed >= 20,
            self.turn_radius <= 30,
            self.turn_load_factor < 6.5,

            #energy constraints
            self.energy_used <= self.propulsion_energy, #total energy used must be less than battery energy
            self.propulsion_energy <= 3600*100, #max 100wh battery

            #time constraints
            self.lap_time*self.laps_flown <= 300, #5 minute flight time
        ])
    
