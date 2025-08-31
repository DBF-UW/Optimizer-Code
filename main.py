import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import constants
import unit_conversion  as uc   
import aircraft
import constraints
import simple_lap_simulator    
import mission_sim
opti = asb.Opti()
airfoil_name = "naca0012"  # or any valid airfoil string

mantaRay = aircraft.Aircraft(opti, airfoil_name)
M2lapper = simple_lap_simulator.LapSimulator(opti, mantaRay, payload=True, banner=False)
M3lapper = simple_lap_simulator.LapSimulator(opti, mantaRay, payload=False, banner=True)
constraints.constraints(opti, mantaRay)
M2_score = mission_sim.M2(mantaRay, M2lapper) 
M3_score = mission_sim.M3(mantaRay, M3lapper)
GM_score = mission_sim.GM(mantaRay)

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
score = GM_min_score/GM_score + (1+ M2_score/M2_max_score) + (2+M3_score/M3_max_score) + 1

test_vals = np.arange(3, 70)
sols = []

for i in test_vals:
    print("Trying: ", i)
    
    opti.maximize(score - (mantaRay.passengers-i)**2)

    try:
        sol = opti.solve(verbose=False)
    except RuntimeError as e:   # CasADi solver error
        print(f"Solver failed for passengers: {i}")
        score = 0
    
    sols.append(sol)

print(sols[1].value(score))

def makeOptimizerPlot(sols, test_vals, y_variable):
    x_vals = []
    y_vals = []
    for i in np.arange(len(test_vals)):
        x_vals.append(sols[i].value(mantaRay.passengers))
        y_vals.append(sols[i].value(y_variable))
        print(sols[i].value(y_variable))
    plt.plot(x_vals, y_vals, marker="o")
    plt.xlabel("Passengers")
    plt.ylabel(y_variable)
    plt.grid(True)
    plt.show()

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
    print(f"{'Aspect Ratio:':<{label_width}} {solution.value(mantaRay.AR):.2f}")
    print(f"{'Wing Area (m^2):':<{label_width}} {solution.value(mantaRay.wing_area):.2f}")
    print(f"{'Flight Mass (kg):':<{label_width}} {solution.value(mantaRay.flight_mass):.2f}")
    print(f"{'Payload Mass (kg):':<{label_width}} {solution.value(mantaRay.payload_mass):.2f}")
    print(f"{'Battery Energy (Wh):':<{label_width}} {solution.value(mantaRay.propulsion_energy/3600):.2f}")

    print("")
    print("------------------- Mission 2 Parameters -------------------")
    print(f"{'Raw Score:':<{label_width}} {solution.value(M2_score):.2f}")
    print(f"{'Total Mass (kg):':<{label_width}} {solution.value(mantaRay.getTotalMass(payload=True)):.2f}")
    print(f"{'Passengers:':<{label_width}} {solution.value(mantaRay.passengers):.2f}")
    print(f"{'Passenger Area (m^2):':<{label_width}} {solution.value(mantaRay.passenger_area):.2f}")
    print(f"{'Cargo:':<{label_width}} {solution.value(mantaRay.cargo):.2f}")
    print(f"{'Laps Flown:':<{label_width}} {solution.value(M2lapper.laps_flown):.2f}")
    print(f"{'Total Time (s):':<{label_width}} {solution.value(M2lapper.total_time):.2f}")
    print(f"{'Total Energy Used (Wh):':<{label_width}} {solution.value(M2lapper.energy_used/3600):.2f}")
    print(f"{'Lap Time (s):':<{label_width}} {solution.value(M2lapper.lap_time):.2f}")
    print(f"{'Straight Speed (m/s):':<{label_width}} {solution.value(M2lapper.straight_speed):.2f}")
    print(f"{'Turn Speed (m/s):':<{label_width}} {solution.value(M2lapper.turn_speed):.2f}")
    print(f"{'Turn Load Factor (g):':<{label_width}} {solution.value(M2lapper.turn_load_factor):.2f}")
    print(f"{'Turn Radius (m):':<{label_width}} {solution.value(M2lapper.turn_radius):.2f}")
    print(f"{'Turn CL:':<{label_width}} {solution.value(M2lapper.turn_CL):.2f}")
    print(f"{'Turn L/D:':<{label_width}} {solution.value(M2lapper.turn_L_D):.2f}")

    print("")
    print("------------------- Mission 3 Parameters -------------------")
    print(f"{'Raw Score:':<{label_width}} {solution.value(M3_score):.2f}")
    print(f"{'Laps Flown:':<{label_width}} {solution.value(M3lapper.laps_flown):.2f}")
    print(f"{'Total Time (s):':<{label_width}} {solution.value(M3lapper.total_time):.2f}")
    print(f"{'Total Energy Used (Wh):':<{label_width}} {solution.value(M3lapper.energy_used/3600):.2f}")
    print(f"{'Lap Time (s):':<{label_width}} {solution.value(M3lapper.lap_time):.2f}")
    print(f"{'Straight Speed (m/s):':<{label_width}} {solution.value(M3lapper.straight_speed):.2f}")
    print(f"{'Turn Speed (m/s):':<{label_width}} {solution.value(M3lapper.turn_speed):.2f}")
    print(f"{'Turn Load Factor (g):':<{label_width}} {solution.value(M3lapper.turn_load_factor):.2f}")
    print(f"{'Turn Radius (m):':<{label_width}} {solution.value(M3lapper.turn_radius):.2f}")
    print(f"{'Turn CL:':<{label_width}} {solution.value(M3lapper.turn_CL):.2f}")
    print(f"{'Banner Length (m):':<{label_width}} {solution.value(mantaRay.banner_length):.2f}")
    print("")
    print("------------------------------------------------------------")

makeOptimizerPlot(sols, test_vals, score)
#makeOptimizerPlot(sols, test_vals, M2lapper.lap_time)
makeOptimizerPlot(sols, test_vals, M2lapper.straight_speed)
#makeOptimizerPlot(sols, test_vals, mantaRay.fuselage_length)

bestAirplane(opti)

