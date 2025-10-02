import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import design_constants
import unit_conversion  as uc   
import aircraft
import constraints
import simple_lap_simulator    
import mission_sim

#initialize objects
opti = asb.Opti()
constants = design_constants.constants_holder(opti) #this constants thing is an object so that the parameters in it can be manipulated.
mantaRay = aircraft.Aircraft(opti, constants)
M2lapper = simple_lap_simulator.LapSimulator(opti, mantaRay, constants, payload=True, banner=False)
M3lapper = simple_lap_simulator.LapSimulator(opti, mantaRay, constants, payload=False, banner=True)
constraints.constraints(opti, mantaRay, constants)

#calculate mission scores
M2_score = mission_sim.M2(constants, mantaRay, M2lapper) 
M3_score = mission_sim.M3(constants, mantaRay, M3lapper)
GM_score = mission_sim.GM(constants, mantaRay)

MAX_PASSENGERS = 80
opti.subject_to([mantaRay.passengers < MAX_PASSENGERS])
#Sopti.subject_to([mantaRay.passengers > 25])
#find and save score for best GM airplane
opti.minimize(GM_score)  
solution1 = opti.solve(verbose=False)
GM_min_score = solution1.value(GM_score)
print("GM min score is:", GM_min_score)

#find and save score for best M2 airplane
opti.maximize(M2_score) 
solution2 = opti.solve(verbose=False)
M2_max_score = solution2.value(M2_score)
print("M2 max score is:", M2_max_score)

#find and save score for best M3 airplane
opti.maximize(M3_score) 
solution3 = opti.solve(verbose=False)
M3_max_score = solution3.value(M3_score)
print("M3 max score is:", M3_max_score)

#normalized score equation
score = constants.REPORT_SCORE_FACTOR * (GM_min_score/GM_score + (1+ M2_score/M2_max_score) + (2+M3_score/M3_max_score) + 1)

#now that max scores have been made, constrain to our known solution space (3 passengers)
opti.subject_to([mantaRay.passengers < 3])

def sensitivitySweep(sweep_variable, center_value, percent_sweep):
    test_range = np.arange(-percent_sweep, percent_sweep + 1)
    scores = []

    opti.set_value(sweep_variable, center_value)
    opti.maximize(score)
    base_score = opti.solve(verbose = False).value(score)

    for i in test_range:
        modifier = 1 + i/100
        opti.set_value(sweep_variable, center_value * modifier)
        opti.maximize(score)
        print("Trying modifier = ", modifier)
        scores.append(opti.solve(verbose = False).value(score))
    scores = np.array(scores)
    scores = ((scores-base_score)/base_score)*100
    return scores

def bestAirplane(opti):
    
    opti.maximize(score)
    solution = opti.solve(verbose=False)

    label_width = 25  # Adjust as needed

    print("------------------- Scoring Info -------------------")
    print(f"{'Score:':<{label_width}} {solution.value(score):.2f}")
    print(f"{'GM Time (s):':<{label_width}} {solution.value(GM_score):.2f}")
    print(f"{'Min GM Time (s):':<{label_width}} {GM_min_score:.2f}")
    print(f"{'Max M2 Score:':<{label_width}} {M2_max_score:.2f}")
    print(f"{'Max M3 Score:':<{label_width}} {M3_max_score:.2f}")
    print("------------------- AC Parameters -------------------")

    print(f"{'Wing Span (m):':<{label_width}} {solution.value(mantaRay.span):.2f}")
    print(f"{'Wing Chord (m):':<{label_width}} {solution.value(mantaRay.chord):.2f}")
    print(f"{'Fuselage Length (m):':<{label_width}} {solution.value(mantaRay.fuselage_length):.2f}")
    print(f"{'Fuselage Width (m):':<{label_width}} {solution.value(mantaRay.fuselage_width):.2f}")
    print(f"{'Fuselage Height (m):':<{label_width}} {solution.value(mantaRay.fuselage_height):.2f}")
    print(f"{'Fuselage Finess Ratio:':<{label_width}} {solution.value(mantaRay.fineness_ratio):.2f}")
    print(f"{'Fuselage Mass (kg):':<{label_width}} {solution.value(mantaRay.fuselage_mass):.2f}")
    print(f"{'Aspect Ratio:':<{label_width}} {solution.value(mantaRay.AR):.2f}")
    print(f"{'Wing Area (m^2):':<{label_width}} {solution.value(mantaRay.wing_area):.2f}")
    print(f"{'Flight Mass (kg):':<{label_width}} {solution.value(mantaRay.flight_mass):.2f}")
    print(f"{'Payload Mass (kg):':<{label_width}} {solution.value(mantaRay.payload_mass):.2f}")
    print(f"{'Battery Energy (Wh):':<{label_width}} {solution.value(mantaRay.propulsion_energy/3600):.2f}")
    print(f"{'Vertical Stab Area (m^2):':<{label_width}} {solution.value(mantaRay.v_stab_area):.2f}")
    print(f"{'Horizontal Stab Area (m^2):':<{label_width}} {solution.value(mantaRay.h_stab_area):.2f}")
    print(f"{'CD0:':<{label_width}} {solution.value(mantaRay.CD0):.4f}")

    print("")
    print("------------------- Mission 2 Parameters -------------------")
    print(f"{'Raw Score:':<{label_width}} {solution.value(M2_score):.2f}")
    print(f"{'Total Mass (kg):':<{label_width}} {solution.value(mantaRay.getTotalMass(payload=True, banner=False)):.2f}")
    print(f"{'Passengers:':<{label_width}} {solution.value(mantaRay.passengers):.2f}")
    print(f"{'Passenger Area (m^2):':<{label_width}} {solution.value(mantaRay.passenger_area):.2f}")
    print(f"{'Cargo:':<{label_width}} {solution.value(mantaRay.cargo):.2f}")
    print(f"{'Laps Flown:':<{label_width}} {solution.value(M2lapper.laps_flown):.2f}")
    print(f"{'Total Time (s):':<{label_width}} {solution.value(M2lapper.total_time):.2f}")
    print(f"{'Total Energy Used (Wh):':<{label_width}} {solution.value(M2lapper.energy_used/3600):.2f}")
    print(f"{'Turn Power (W):':<{label_width}} {solution.value(M2lapper.turn_power):.2f}")
    print(f"{'Straight Power (W):':<{label_width}} {solution.value(M2lapper.straight_power):.2f}")
    print(f"{'Lap Time (s):':<{label_width}} {solution.value(M2lapper.lap_time):.2f}")
    print(f"{'Straight Speed (m/s):':<{label_width}} {solution.value(M2lapper.straight_speed):.2f}")
    print(f"{'Turn Speed (m/s):':<{label_width}} {solution.value(M2lapper.turn_speed):.2f}")
    print(f"{'Turn Load Factor (g):':<{label_width}} {solution.value(M2lapper.turn_load_factor):.2f}")
    print(f"{'Turn Radius (m):':<{label_width}} {solution.value(M2lapper.turn_radius):.2f}")
    print(f"{'Turn CL:':<{label_width}} {solution.value(M2lapper.turn_CL):.2f}")
    print(f"{'Turn L/D:':<{label_width}} {solution.value(M2lapper.turn_L_D):.2f}")
    print(f"{'Straight CL:':<{label_width}} {solution.value(M2lapper.straight_CL):.2f}")
    print(f"{'Straight L/D:':<{label_width}} {solution.value(M2lapper.straight_L_D):.2f}")

    print("")
    print("------------------- Mission 3 Parameters -------------------")
    print(f"{'Raw Score:':<{label_width}} {solution.value(M3_score):.2f}")
    print(f"{'Laps Flown:':<{label_width}} {solution.value(M3lapper.laps_flown):.2f}")
    print(f"{'Total Time (s):':<{label_width}} {solution.value(M3lapper.total_time):.2f}")
    print(f"{'Total Energy Used (Wh):':<{label_width}} {solution.value(M3lapper.energy_used/3600):.2f}")
    print(f"{'Lap Time (s):':<{label_width}} {solution.value(M3lapper.lap_time):.2f}")
    print(f"{'Straight Speed (m/s):':<{label_width}} {solution.value(M3lapper.straight_speed):.2f}")
    print(f"{'Straight Drag (N):':<{label_width}} {solution.value(M3lapper.straight_drag):.2f}")
    print(f"{'Turn Power (W):':<{label_width}} {solution.value(M3lapper.turn_power):.2f}")
    print(f"{'Straight Power (W):':<{label_width}} {solution.value(M3lapper.straight_power):.2f}")
    print(f"{'Turn Speed (m/s):':<{label_width}} {solution.value(M3lapper.turn_speed):.2f}")
    print(f"{'Turn Load Factor (g):':<{label_width}} {solution.value(M3lapper.turn_load_factor):.2f}")
    print(f"{'Turn Radius (m):':<{label_width}} {solution.value(M3lapper.turn_radius):.2f}")
    print(f"{'Straight CL:':<{label_width}} {solution.value(M3lapper.straight_CL):.2f}")
    print(f"{'Turn CL:':<{label_width}} {solution.value(M3lapper.turn_CL):.2f}")
    print(f"{'Banner Length (m):':<{label_width}} {solution.value(mantaRay.banner_length):.2f}")
    print(f"{'Banner Mass (kg):':<{label_width}} {solution.value(mantaRay.banner_mass):.2f}")
    print("")
    print("------------------------------------------------------------")

driving_parameters = [
    constants.PROPULSION_EFFICIENCY_FACTOR,
    constants.STRUCTURES_EXECUTION_FACTOR,
    constants.FUSELAGE_PACKING_FACTOR,
    constants.PARASITIC_DRAG_FACTOR,
    constants.BANNER_CD_FACTOR,
    constants.OSWALD_EFFICIENCY_FACTOR,
    constants.GM_TIME_FACTOR,
    constants.CL_MAX_FACTOR,
]

labels = [
    "Propulsion Efficiency",
    "Aircraft Weight",
    "Fuselage Size",
    "Parasitic Drag",
    "Banner Drag",
    "Oswald Efficiency",
    "Ground Mission Time",
    "Cl Max",
]

percent_sweep = 25
x_vals = np.arange(-percent_sweep, percent_sweep + 1)

for i in np.arange(0, len(driving_parameters)):
    parameter = driving_parameters[i]
    label = labels[i]
    plt.plot(x_vals, sensitivitySweep(parameter, 1, percent_sweep), label = label)


plt.xlabel("Percent Change In Variable")
plt.ylabel("Percent Change In Score")
plt.grid(True)
plt.legend(loc="upper left", bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.show()
