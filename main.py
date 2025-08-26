import aerosandbox as asb
import aerosandbox.numpy as np
import constants
import unit_conversion  as uc   
import aircraft
import constraints
import simple_lap_simulator    
import mission_sim
opti = asb.Opti()
airfoil_name = "naca0012"  # or any valid airfoil string

mantaRay = aircraft.Aircraft(opti, airfoil_name)
M2lapper = simple_lap_simulator.LapSimulator(opti, mantaRay, payload=True)
M3lapper = simple_lap_simulator.LapSimulator(opti, mantaRay, payload=False)
constraints.constraints(opti, mantaRay)
score = mission_sim.M2(mantaRay, M2lapper)
opti.maximize(score)
solution = opti.solve()

label_width = 25  # Adjust as needed

print("------------------- AC Parameters -------------------")
print(f"{'Wing Span (m):':<{label_width}} {solution.value(mantaRay.span):.2f}")
print(f"{'Wing Chord (m):':<{label_width}} {solution.value(mantaRay.chord):.2f}")
print(f"{'Aspect Ratio:':<{label_width}} {solution.value(mantaRay.AR):.2f}")
print(f"{'Wing Area (m^2):':<{label_width}} {solution.value(mantaRay.wing_area):.2f}")
print(f"{'Flight Mass (kg):':<{label_width}} {solution.value(mantaRay.flight_mass):.2f}")
print(f"{'Payload Mass (kg):':<{label_width}} {solution.value(mantaRay.payload_mass):.2f}")
print(f"{'Battery Energy (Wh):':<{label_width}} {solution.value(mantaRay.propulsion_energy/3600):.2f}")

print("")
print("------------------- Mission 2 Parameters -------------------")
print(f"{'Score:':<{label_width}} {solution.value(score):.2f}")
print(f"{'Total Mass (kg):':<{label_width}} {solution.value(mantaRay.getTotalMass(payload=True)):.2f}")
print(f"{'Passengers:':<{label_width}} {solution.value(mantaRay.passengers):.2f}")
print(f"{'Cargo:':<{label_width}} {solution.value(mantaRay.cargo):.2f}")
print(f"{'Laps Flown:':<{label_width}} {solution.value(M2lapper.laps_flown):.2f}")
print(f"{'Total Time (s):':<{label_width}} {solution.value(M2lapper.total_time):.2f}")
print(f"{'Total Energy Used (Wh):':<{label_width}} {solution.value(M2lapper.energy_used/3600):.2f}")
print(f"{'Lap Time (s):':<{label_width}} {solution.value(M2lapper.lap_time):.2f}")
print(f"{'Speed (m/s):':<{label_width}} {solution.value(M2lapper.speed):.2f}")
print(f"{'Turn Load Factor (g):':<{label_width}} {solution.value(M2lapper.turn_load_factor):.2f}")
print(f"{'Turn Radius (m):':<{label_width}} {solution.value(M2lapper.turn_radius):.2f}")
print(f"{'Turn CL:':<{label_width}} {solution.value(M2lapper.turn_CL):.2f}")

print("")
print("------------------- Mission 3 Parameters -------------------")
print(f"{'Banner Length (m):':<{label_width}} {solution.value(mantaRay.banner_length):.2f}")

