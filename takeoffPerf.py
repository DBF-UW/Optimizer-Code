# takeoff performance

import constants


def energy_takeoff(ground_roll_distance, cruiseAlt, thrust, mass, cruiseVel): 

    # get the total energy needed for climbout and ground roll

    ground_roll_energy = thrust * ground_roll_distance

    potential_energy_increase = constants.g * cruiseAlt * mass

    kinetic_energy_increase = 0.5 * mass * cruiseVel**2 

    return kinetic_energy_increase + potential_energy_increase + ground_roll_energy

def time_takeoff(thrust, mass): 

    A = constants.g * (thrust / (mass * constants.g) - constants.mu_r)
    B = constants.g / 7