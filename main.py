import aerosandbox as asb
import aerosandbox.numpy as np
import constants
import unit_conversion  as uc   
import aircraft
import constraints
import simple_lap_simulator    

opti = asb.Opti()
airfoil_name = "naca0012"  # or any valid airfoil string

mantaRay = aircraft.Aircraft(opti, airfoil_name)
print(mantaRay.span)
constraints.constraints(opti, mantaRay)
lapper = simple_lap_simulator.LapSimulator(opti, mantaRay, payload=True)
opti.maximize(lapper.laps_flown)
solution = opti.solve()
print(solution.value(lapper.lap_time)) 
print(solution.value(mantaRay.passengers))
print(solution.value(mantaRay.AR))
print(solution.value(lapper.speed))
print(solution.value(lapper.turn_load_factor))
print(solution.value(lapper.lap_energy))
