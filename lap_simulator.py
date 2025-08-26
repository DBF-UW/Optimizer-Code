import aerosandbox as asb
import aerosandbox.numpy as np
import constants
import unit_conversion as uc

def lap_simulator(opti:asb.Opti, aircraft:"Aircraft") -> None:

    #variables
    full_leg_length = uc.feet2meters(constants.AIAA_LENGTH) #meters
    leg_A_length = opti.variable(init_guess=full_leg_length/2, lower_bound=0.1, upper_bound=full_leg_length) #meters
    leg_B_length = full_leg_length - leg_A_length #meters
    altitudes = opti.variable(init_guess=[20]*11, lower_bound=5, upper_bound = 35) #meters
    speeds = opti.variable(init_guess=[40]*11) #m/s
    turn_radius = opti.variable(init_guess=[0,20,20,0,20,20,20,20,0,20,20], lower_bound=4, upper_bound=100) #unitless
    is_a_turn = [False, True, True, False, True, True, True, True, False, True, True]
    energy_used = [0]*11
    leg_time = [0]*11

    #constraints
    opti.subject_to([
        altitudes >= uc.feet2meters(15), #minimum altitude
        altitudes <= uc.feet2meters(30), #maximum altitude
        
    ])
    #calculate total lap time and energy
    for i in leg_time:

        if i + 1 >= len(leg_time): #prevents index out of bounds
            next = 0
        else:
            next = i + 1

        #find leg length
        if is_a_turn[i]:
            leg_length = 2 * np.pi * turn_radius[i] / 4 #quarter circle
        else:
            if i == 3:
                leg_length = leg_A_length
            elif i == 8:
                leg_length = leg_B_length
            else:
                leg_length = full_leg_length
        
        average_speed = (speeds[i] + speeds[next])/2 #assume linear speed change
        leg_time[i] = leg_length / average_speed

        #find energy used
        if is_a_turn[i]:
            load_factor = np.sqrt(1 + (speeds[i]**2)/(constants.GRAVITATIONAL_ACCELERATION*turn_radius[i]))
        else:
            load_factor = 1
        
