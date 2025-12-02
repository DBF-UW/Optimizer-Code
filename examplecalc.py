import math
mu = 1.26686534e8        # km^3/s^2
v_inf = 5.6441           # km/s
phi_deg = 92.02857031278344
phi = math.radians(phi_deg)
b = mu / (v_inf**2 * math.tan(phi/2))
print(b)   # -> ~3838500 (km)
