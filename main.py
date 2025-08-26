import aerosandbox as asb
import aerosandbox.numpy as np
import constants
import unit_conversion  as uc   
import aircraft
import constraints
import simple_lap_simulator    

opti = asb.Opti()
airfoil_name = "naca2412"  # or any valid airfoil string

mantaRay = aircraft.Aircraft(opti, airfoil_name)
print(mantaRay.span)
constraints.constraints(opti, mantaRay)
lapper = simple_lap_simulator.LapSimulator(opti, mantaRay, payload=True)
solution = opti.solve()
print(solution.value(lapper.lap_time))  # Prints the numeric value of self.mass
