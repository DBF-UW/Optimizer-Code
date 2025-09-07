# this will serve as the optimization for the wing

import aerosandbox as asb
import aerosandbox.numpy as np
import constants
import aero_functions as aero
import matplotlib.pyplot as plt

opti = asb.Opti()

# 1.5 * span
# pack as efficiently as possible can only 

# openvsp

# 0.03 * q * length * height

#batteryCapacity = 100
#propulsionEfficiency = 0.75
#EnergyUsable = constants.batteryCapacity * propulsionEfficiency * 3600 # joules
#rho = 1.225
# W = 30 * 9.81 # N
#g = 9.81
#n_max = 8
#CLmax = 1.6
EF = 1

#CD0 = 0.03
#e = 0.9

#straight_dist = 304.8 # m

class Aircraft():

    def __init__(self):
        self.V_straight_M2 = opti.variable(init_guess=30, lower_bound=0)
        self.V_turn_M2 = opti.variable(init_guess=25, lower_bound=0)
        self.V_straight_M3 = opti.variable(init_guess=30, lower_bound=0)
        self.V_turn_M3 = opti.variable(init_guess=25, lower_bound=0)


        self.banner_length = opti.variable(init_guess=1, lower_bound=0.0)
        self.banner_width = opti.variable(init_guess=1, lower_bound=0.0)

        self.span = opti.variable(init_guess=4, lower_bound=0) #global
        self.chord = opti.variable(init_guess=1, lower_bound=0) #global
        self.n_turn_M2 = opti.variable(init_guess=3, lower_bound=1, upper_bound=constants.n_max)
        self.n_turn_M3 = opti.variable(init_guess=3, lower_bound=1, upper_bound=constants.n_max)

        self.ducks = opti.variable(init_guess=3, lower_bound=1)
        self.pucks = opti.variable(init_guess=1, lower_bound=1)


        self.S = self.span * self.chord
        self.AR = self.span**2 / self.S

        # --- Tail sizing from volume coefficients ---
        self.l_ht = constants.tailArmH
        self.l_vt = constants.tailArmV

        # Areas from volume coefficients: VH = (S_H * l_H) / (S * c), VV = (S_V * l_V) / (S * b)
        # => S_H = VH * S * c / l_H ; S_V = VV * S * b / l_V
        self.S_ht = constants.tail_VH * self.S * self.chord / self.l_ht
        self.S_vt = constants.tail_VV * self.S * self.span  / self.l_vt

        # Simple wetted-area estimate for thin tails
        self.Swet_ht = 2.0 * self.S_ht
        self.Swet_vt = 2.0 * self.S_vt

        # Lumped parasitic drag increment from tails (added to CD0)
        self.CD0_tail = constants.Cfe_tail * (self.Swet_ht + self.Swet_vt) / self.S

        #induced drag
        self.k = 1 / (np.pi * constants.oswaldEff * self.AR)



        #lift
        self.CL_straight_M2  = get_weight(self.span, self.chord, self.ducks, self.pucks, 0, 0) / (0.5 * constants.rho * self.S * self.V_straight_M2**2)
        self.CL_turn_M2 = self.n_turn_M2 * get_weight(self.span, self.chord, self.ducks, self.pucks, 0, 0) / (0.5 * constants.rho * self.S * self.V_turn_M2**2)

        self.CL_straight_M3 = get_weight(self.span, self.chord, 0, 0, self.banner_length, self.banner_width) / (0.5 * constants.rho * self.S * self.V_straight_M3**2)
        self.CL_turn_M3 = self.n_turn_M3 * get_weight(self.span, self.chord, 0, 0, self.banner_length, self.banner_width) / (0.5 * constants.rho * self.S * self.V_turn_M3**2)

        self.CD_straight_M2 = constants.CD0 + self.k * self.CL_straight_M2**2
        self.CD_turn_M2 = constants.CD0 + self.k * self.CL_turn_M2 ** 2

        self.CD_straight_M3 = constants.CD0 + self.k * self.CL_straight_M3**2
        self.CD_turn_M3 = constants.CD0 + self.k * self.CL_turn_M3**2

        fusDragM2_s, _ = aero.fus_drag(self.ducks, self.pucks, self.span, self.chord, self.V_straight_M2)
        fusDragM2_t, _ = aero.fus_drag(self.ducks, self.pucks, self.span, self.chord, self.V_turn_M2)
        fusDragM3_s, _ = aero.fus_drag(self.ducks, self.pucks, self.span, self.chord, self.V_straight_M3)
        fusDragM3_t, _ = aero.fus_drag(self.ducks, self.pucks, self.span, self.chord, self.V_turn_M3)
        #drag force
        self.Drag_straight_M2 = 0.5 * constants.rho * self.V_straight_M2**2 * self.S * self.CD_straight_M2 + fusDragM2_s
        self.Drag_turn_M2 = 0.5 * constants.rho * self.V_turn_M2**2 * self.S * self.CD_turn_M2 + fusDragM2_t

        self.Drag_straight_M3 = 0.5 * constants.rho * self.V_straight_M3**2 * self.S * self.CD_straight_M3 + aero.banner_drag(self.banner_length, self.banner_width, self.V_straight_M3) + fusDragM3_s
        self.Drag_turn_M3 = 0.5 * constants.rho * self.V_turn_M3**2 * self.S * self.CD_turn_M3 + aero.banner_drag(self.banner_length, self.banner_width, self.V_turn_M3) + fusDragM3_t

        self.power_straight_M2 = self.Drag_straight_M2 * self.V_straight_M2
        self.power_turn_M2 = self.Drag_turn_M2 * self.V_turn_M2

        self.power_straight_M3 = self.Drag_straight_M3 * self.V_straight_M3
        self.power_turn_M3 = self.Drag_turn_M3 * self.V_turn_M3

        #self.CD_straight_M2 += self.CD0_tail
        self.CD_turn_M2     += self.CD0_tail
        self.CD_straight_M3 += self.CD0_tail
        self.CD_turn_M3     += self.CD0_tail

def get_weight(span, chord, ducks, pucks, length, width):
    _, fusweight = aero.fus_drag(ducks, pucks, span, chord, 0)
    return constants.g * (aero.wing_weight(span, chord) + aero.banner_weight(length, width) + ducks * 0.0198447 + pucks * 0.198447) + fusweight #20 will be fus weight


#def get_wing_weight(thickness, wing_area, density=1600):
#    volume = thickness * wing_area
#    return volume * density * constants.g



def GM_Score():
    return 1/((3.5 * (plane.ducks)) + 20)

def M_2Score():
    Income = (plane.ducks * (constants.lp1 + (constants.lp2 * laps_flown_M2))) + (plane.pucks * (constants.lc1 + (constants.lc2 * laps_flown_M2)))
    Cost = laps_flown_M2 * (constants.Ce + (plane.ducks * constants.Cp) + (plane.pucks * constants.Cc)) * EF
    Net_Income = Income - Cost
    return Net_Income

def M_3Score():
    RAC = 0.75 + 0.05 * plane.span * 3.28
    M3 = laps_flown_M3 * plane.banner_length / RAC
    return M3

plane = Aircraft()


weight_M2 = get_weight(plane.span, plane.chord, plane.ducks, plane.pucks, 0, 0)
weight_M3 = get_weight(plane.span,  plane.chord, 0, 0, plane.banner_length, plane.banner_width)

lift_M2 = 0.5 * constants.rho * plane.V_straight_M2 ** 2 * plane.S * plane.CL_straight_M2
lift_turn_M2 = 0.5 * constants.rho * plane.V_turn_M2**2 * plane.S * plane.CL_turn_M2

V_stall = ((2 * weight_M2 / constants.g)/(constants.rho * plane.S * constants.CLmax))**0.5


#opti.subject_to(lift >= weight)
#opti.subject_to(lift_turn >= weight)
#opti.subject_to(plane.V >= V_stall)
#opti.subject_to(plane.V_turn >= V_stall)

#opti.subject_to(plane.AR <= 20)

turn_radius_M2 = plane.V_turn_M2 ** 2 / (constants.g * np.sqrt(plane.n_turn_M2**2 - 1))
turn_radius_M3 = plane.V_turn_M3**2 / (constants.g * np.sqrt(plane.n_turn_M3**2 - 1))

circumfrence_M2 = np.pi * 2 * turn_radius_M2
circumfrence_M3 = np.pi * 2 * turn_radius_M3

t_straight_M2 = constants.straightDist / plane.V_straight_M2
t_straight_M3 = constants.straightDist / plane.V_straight_M3

t_turn_M2 = circumfrence_M2 / plane.V_turn_M2
t_turn_M3 = circumfrence_M3 / plane.V_turn_M3

E_lap_M2 = 2 * plane.power_straight_M2 * t_straight_M2 + plane.power_turn_M2 * t_turn_M2 * 2
E_lap_M3 = 2 * plane.power_straight_M3 * t_straight_M3 + plane.power_turn_M3 * t_turn_M3 * 2


t_lap_M2 = 2 * t_straight_M2 + 2 * t_turn_M2
t_lap_M3 = 2 * t_straight_M3 + 2 * t_turn_M3

#laps_flown = constants.energyUsable / E_lap

#laps_flown_M2 = constants.energyUsable / E_lap_M2
#laps_flown_M3 = constants.energyUsable / E_lap_M3

laps_flown_M2 = 300 / t_lap_M2
laps_flown_M3 = 300 / t_lap_M3

plane.V_straight_M2 >= 20,
plane.V_straight_M3 >= 20,
plane.V_turn_M2 >= 20,
plane.V_turn_M3 >= 20
# constraints
constraints = [
    plane.AR >= 3.999,
    plane.AR <= 20,
    plane.ducks <= constants.duck_constraint,
    plane.banner_length == 5 * plane.banner_width,
    plane.CL_straight_M2 <= constants.CLmax,
    plane.CL_turn_M2 <= constants.CLmax,
    plane.CL_straight_M3 <= constants.CLmax,
    plane.CL_turn_M3 <= constants.CLmax,
    plane.ducks >= 3 * plane.pucks,
    E_lap_M2 * laps_flown_M2 <= constants.energyUsable,
    E_lap_M3 * laps_flown_M3 <= constants.energyUsable,
    plane.span >= constants.minSpan,
    plane.span <= constants.maxSpan,
    plane.V_straight_M2 >= 20,
    plane.V_straight_M3 >= 20,
    plane.V_turn_M2 >= 20,
    plane.V_turn_M3 >= 20
]

for c in constraints:
    opti.subject_to(c)


#M2
m2_ma = opti.maximize(M_2Score())

solm2 = opti.solve(verbose=False)

normalizedM2 = solm2(M_2Score())

#GM

gm_ma = opti.maximize(GM_Score())

solgm = opti.solve(verbose=False)

normalizedGM = solgm(GM_Score())

#M3
m3_ma = opti.maximize(M_3Score())

solM3 = opti.solve(verbose=False)

print("Plane span", solM3(plane.span))
print("Plane banner", solM3(plane.banner_length))

normalizedM3 = solM3(M_3Score())

# net
#normalizedGM = 1
#normalizedM2 = 1
#normalizedM3 = 1

netScore = (GM_Score() / normalizedGM) + 1 + (1 + M_2Score() / normalizedM2) + (2 + M_3Score() / normalizedM3)

net_ma = opti.maximize(netScore)
solNet = opti.solve()

ducks_val = float(solNet.value(plane.ducks))
pucks_val = float(solNet.value(plane.pucks))
S_ref_val = float(solNet.value(plane.S))
V_val     = float((solNet.value(plane.V_straight_M3) + solNet.value(plane.V_straight_M2)) / 2)





print("Optimized M2 Ducks: ", solm2(plane.ducks))



print("=== GM Numbers ===")

print("\n=== Airplane Numbers ===")
print(f"Span:                {solNet(plane.span):.3f} m")
print(f"Chord:               {solNet(plane.chord):.3f} m")
print(f"Airspeed M2:            {solNet(plane.V_straight_M2):.2f} m/s")
print(f"Airspeed M3:            {solNet(plane.V_straight_M3):.2f} m/s")
print(f"Aspect Ratio (AR):   {solNet(plane.AR):.2f}")
print(f"Weight M2:              {solNet(weight_M2) / constants.g:.2f} kg")
print(f"Weight M3:              {solNet(weight_M3) / constants.g:.2f} kg")
print(f"H-Stab Wing Area:  {solNet(plane.S_ht)}")
print(f"V-Stab Wing Area:  {solNet(plane.S_vt)}")



print("\n=== M2 Parameters ===")
print(f"Ducks:               {solNet(plane.ducks)}")
print(f"Pucks:               {solNet(plane.pucks)}")
print(f"Lap Time M2:            {solNet(t_lap_M2):.2f} s")
print(f"Lap Time M3:            {solNet(t_lap_M3):.2f} s")
print(f"Laps Flown M2:          {solNet(laps_flown_M2)}")
print(f"Laps Flown M3:          {solNet(laps_flown_M3)}")
print(f"Energy Used per lap M2:         {solNet(E_lap_M2):.2f} J")
print(f"Energy Used per lap M3:         {solNet(E_lap_M3):.2f} J")
print(f"Total Energy Used M2:   {(solNet(E_lap_M2) * solNet(laps_flown_M2))/270000*100:.1f} %")
print(f"Total Energy Used M3:   {(solNet(E_lap_M3) * solNet(laps_flown_M3))/270000*100:.1f} %")

print("\n--- Performance ---")
print(f"Turn Load Factor M2:    {solNet(plane.n_turn_M2):.2f}")
print(f"CL (Straight) M2:       {solNet(plane.CL_straight_M2):.3f}")
print(f"CL (Turn) M2:           {solNet(plane.CL_turn_M2):.3f}")
print(f"Turn Radius M2:         {solNet(turn_radius_M2):.2f} m")
print(f"Turn Speed M2:          {solNet(plane.V_turn_M2):.2f} m/s")
print(f"V_stall:             {solNet(V_stall):.2f} m/s")
print(f"Lift (Straight) M2:     {solNet(lift_M2)/constants.g:.2f} kg")
print(f"Lift (Turn) M2:         {solNet(lift_turn_M2)/constants.g:.2f} kg")
print("Load factor: ", solNet(lift_turn_M2) / solNet(weight_M2))


print("\n=== Scoring ===")
print(f"GM Score:          {solNet(GM_Score()):.2f}")
print(f"M2 Score:          {solNet(M_2Score()):.2f}")
print(f"M3 Score:          {solNet(M_3Score() / normalizedM3):.2f}")

print("\n=== Banner ===")
print(f"Banner Length:       {solNet(plane.banner_length):.2f} m")
print(f"Banner Width:        {solNet(plane.banner_width):.2f} m")

print("CD Straight Overall M2 ", (solNet(plane.CD_straight_M2)))

print("Net Score: ", solNet(netScore))
"""
sweep_passengers = np.linspace(3, constants.duck_constraint, constants.duck_constraint - 2)
duck_target = opti.parameter()
opti.maximize(netScore - (plane.ducks - duck_target)**2)
# sweep_passengers = np.linspace(3, 3, 1)
x_vals = []
y_vals = []

for i in sweep_passengers:
    print("Passengers: ", i)

    opti.set_value(duck_target, i)

    try:
        sol = opti.solve(verbose=False)
        y_vals.append(sol.value(netScore))
        x_vals.append(sol.value(plane.ducks))
    except RuntimeError as e:
        print(f"Solver failed for {i} passengers ")

plt.plot(x_vals, y_vals, marker="o", linestyle= 'none')
plt.xlabel("Passengers (ducks)")
plt.ylabel("Score (0-7)")
plt.title("Score vs Passengers")
plt.grid(True)
plt.show()
"""