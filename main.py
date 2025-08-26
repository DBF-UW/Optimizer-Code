import aerosandbox as asb
import aerosandbox.numpy as np
import constants
import unit_conversion  as uc   
import aircraft
import constraints
import lap_simulator    

opti = asb.Opti()
airfoil_name = "naca2412"  # or any valid airfoil string

mantaRay = aircraft.Aircraft(opti, airfoil_name)
print(mantaRay.span)
constraints.constraints(opti, mantaRay)
solution = opti.solve()
for i in range(opti.x.shape[0]):
    var = opti.x[i]
    print(f"{var.name()}: {solution.value(var)}")