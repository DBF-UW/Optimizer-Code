# this will serve as the optimization for the wing

import aerosandbox as asb
import aerosandbox.numpy as np
import constants
import aero_functions as aero
import matplotlib.pyplot as plt
import initialization as in_
import casadi as ca
import mass_buildup as mass
import lap_simulator
import normalDistribution as nd

opti = asb.Opti()

EF = 1

class Aircraft():

    def __init__(self):

        in_.mission_parm(self, opti)
        in_.fuselage_parm(self, opti)
        in_.sweepParm(self, opti)
        in_.velocity_parm(self, opti)
        in_.airplane_parm(self, opti)
        in_.CD_planform(self, opti) 
        lap_simulator.lap_sim(self, opti)

        # self.Drag_turn_M2 = constants.inducedDragFactor * 0.5 * constants.rho * self.V_turn_M2**2 * self.S * self.CD_turn_M2

        self.banner_turn = aero.get_banner_cd(aero.get_Reynolds(self.banner_length, self.V_turn_M3))

        self.Drag_turn_M3 = constants.inducedDragFactor * 0.5 * constants.rho * self.V_turn_M3**2 * self.S * self.CD_turn_M3 + constants.banner_turn_drag_factor * aero.banner_drag(self.banner_length, self.banner_width, self.V_turn_M3, self.banner_turn)

        # self.CD_turn_M2     += self.CD0_tail
        
        self.CD_turn_M3     += self.CD0_tail

        # fuselage optimization

       # self.fusdragM2_s = constants.fuselage_drag_factor * 0.5 * constants.rho * self.V_straight_M2**2 * self.S * aero.getFuselageCD0(self.fuselage_length, self.effective_diameter, self.V_straight_M2, self.fuselage_wetted_area, self.S)
        # self.fusdragM2_t = constants.fuselage_drag_factor * 0.5 * constants.rho * self.V_turn_M2**2 * self.S * aero.getFuselageCD0(self.fuselage_length, self.effective_diameter, self.V_turn_M2, self.fuselage_wetted_area, self.S) # aero.fus_drag(self.fuse_length, self.effective_dia, self.fus_wet_area, self.S, self.V_turn_M2)
        # self.fusdragM3_s_f = constants.fuselage_drag_factor * 0.5 * constants.rho * self.V_straight_M3_f**2 * self.S * aero.getFuselageCD0(self.fuselage_length, self.effective_diameter, self.V_straight_M3_f, self.fuselage_wetted_area, self.S) # aero.fus_drag(self.fuse_length, self.effective_dia, self.fus_wet_area, self.S, self.V_straight_M3_f)
        # self.fusdragM3_s_b = constants.fuselage_drag_factor * 0.5 * constants.rho * self.V_straight_M3_b**2 * self.S * aero.getFuselageCD0(self.fuselage_length, self.effective_diameter, self.V_straight_M3_b, self.fuselage_wetted_area, self.S) # aero.fus_drag(self.fuse_length, self.effective_dia, self.fus_wet_area, self.S, self.V_straight_M3_b)
        self.fusdragM3_t = constants.fuselage_drag_factor * 0.5 * constants.rho * self.V_turn_M3**2 * self.S * aero.getFuselageCD0(self.fuselage_length, self.effective_diameter, self.V_turn_M3, self.fuselage_wetted_area, self.S)
         # aero.fus_drag(self.fuse_length, self.effective_dia, self.fus_wet_area, self.S, self.V_turn_M3)

       #  self.Drag_straight_M2 += self.fusdragM2_s
        # self.Drag_turn_M2 += self.fusdragM2_t
       #  self.Drag_straight_M3_f += self.fusdragM3_s_f
       # self.Drag_straight_M3_b += self.fusdragM3_s_b
        self.Drag_turn_M3 += self.fusdragM3_t
        in_.powerParm(self, opti)

def GM_Score():
    return 1/((3.5 * (plane.ducks + plane.pucks)) + 20 + plane.ground_tax)

def M_2Score():
    Income = (plane.ducks * (constants.lp1 + (constants.lp2 * laps_flown_M2))) + (plane.pucks * (constants.lc1 + (constants.lc2 * laps_flown_M2)))
    Cost = (laps_flown_M2) * (constants.Ce + (plane.ducks * constants.Cp) + (plane.pucks * constants.Cc)) * EF
    Net_Income = Income - Cost
    return Net_Income

def M_3Score():
    RAC = 0.75 + 0.05 * plane.span * 3.28
    RAC = 1
    M3 = (laps_flown_M3) * plane.banner_length / RAC
    return M3

plane = Aircraft()


weight_M2 = mass.get_weight(plane.span, plane.chord, plane.ducks, plane.pucks, 0, 0, plane.restraint_weight, plane.fuselage_area)
weight_M3 = mass.get_weight(plane.span,  plane.chord, 0, 0, plane.banner_length, plane.banner_width, 0, plane.fuselage_area) + plane.extra_weight

# lift_M2 = 0.5 * constants.rho * plane.V_straight_M2 ** 2 * plane.S * plane.CL_straight_M2
# lift_turn_M2 = 0.5 * constants.rho * plane.V_turn_M2**2 * plane.S * plane.CL_turn_M2

V_stall = ((2 * weight_M2 / constants.g)/(constants.rho * plane.S * constants.CLmax))**0.5

# turn_radius_M2 = plane.V_turn_M2 ** 2 / (constants.g * np.sqrt(plane.n_turn_M2**2 - 1))
turn_radius_M3 = plane.V_turn_M3**2 / (constants.g * np.sqrt(plane.n_turn_M3**2 - 1))

# circumfrence_M2 = np.pi * 2 * turn_radius_M2
circumfrence_M3 = np.pi * 2 * turn_radius_M3

# t_straight_M2 = constants.straightDist / plane.V_straight_M2
# t_straight_M3_f = constants.straightDist / plane.V_straight_M3_f
# t_straight_M3_b = constants.straightDist / plane.V_ground_M3_b


# t_turn_M2 = circumfrence_M2 / plane.V_turn_M2
t_turn_M3 = circumfrence_M3 / plane.V_turn_M3

E_lap_M2 = plane.e_turn_total_M2 + plane.e_straight_total_M2 # plane.power_turn_M2 * t_turn_M2 * 2 + plane.e_straight_total_M2 # 2 * plane.power_straight_M2 * t_straight_M2 + plane.power_turn_M2 * t_turn_M2 * 2
E_lap_M3 = plane.power_turn_M3 * t_turn_M3 * 2 + plane.e_straight_total_M3 # 1 * plane.power_straight_M3_f * t_straight_M3_f + plane.power_turn_M3 * t_turn_M3 * 2 + 1 * plane.power_straight_M3_b * t_straight_M3_b


t_lap_M2 = plane.t_straight_total_M2 + plane.t_turn_total_M2 # plane.t_straight_total_M2 + 2 * t_turn_M2 # 2 * t_straight_M2 + 2 * t_turn_M2
t_lap_M3 = plane.t_straight_total_M3 + 2 * t_turn_M3 # t_straight_M3_f + t_straight_M3_b + 2 * t_turn_M3

laps_flown_M2 = 300 / t_lap_M2
laps_flown_M3 = 300 / t_lap_M3

opti.set_value(plane.PropEff, 0.7)

M2energyusable = aero.energy_usable(plane.PropEff) # aero.energy_usable(plane.V_straight_M2)
M3energyusable = aero.energy_usable(plane.PropEff) # aero.energy_usable((plane.V_straight_M3_f))


# constraints
constraints = [
    plane.n_turn_M2 <= plane.max_g,
    plane.AR >= 4,
    plane.AR <= 20,
    plane.n_turn_M3 <= plane.max_g,
    plane.ducks <= constants.duck_constraint,
    plane.banner_length == 5 * plane.banner_width,
    # plane.CL_straight_M2 <= plane.CLmax,
   # plane.CL_turn_M2 <= plane.CLmax,
    plane.CL_turn_M3 <= plane.CLmax,
    # plane.CL_straight_M3_b <= plane.CLmax,
    # plane.CL_straight_M3_f <= plane.CLmax,
    plane.ducks >= 3 * plane.pucks,
    # plane.V_straight_M3_f >= plane.min_V3_speed,
    # plane.V_straight_M3_b >= plane.min_V3_speed,
    # E_lap_M2 * laps_flown_M2 <= constants.energyUsable,
    E_lap_M2 * laps_flown_M2 <= M2energyusable,
    # E_lap_M3 * laps_flown_M3 <= constants.energyUsable,
    E_lap_M3 * laps_flown_M3 <= M3energyusable,
    plane.span >= constants.minSpan,
    plane.span <= constants.maxSpan,
    # plane.V_straight_M3_f >= 20, 
    # plane.V_straight_M3_b >= 20,
    # plane.V_turn_M3 >= plane.V_straight_M3_f * 0.9,
    # plane.V_turn_M2 >= plane.V_straight_M2 * 0.9,
    plane.fuselage_box_length < 2,
    plane.fuselage_box_length > 0.07,
    plane.fuselage_width > 0.085,
    plane.fuselage_height > 0.1,
    plane.fuselage_height * plane.fuselage_width > plane.total_volume,  # fus constraints
    plane.fuselage_box_length * plane.fuselage_width > plane.total_area,
]

opti.set_value(plane.CLmax, 1.1)

for c in constraints:
    opti.subject_to(c)

# opti.set_value(plane.banner_CD_e, aero.get_banner_cd(aero.get_Reynolds(plane.banner_length, plane.V_straight_M3_b)))
opti.set_value(plane.ground_tax, 0)
opti.set_value(plane.wind_speed, 1)
opti.set_value(plane.wing_direction, 0)
opti.set_value(plane.max_g, 8)
# opti.set_value(plane.min_V3_speed, 0)
opti.set_value(plane.skin_friction_drag, constants.CD0)
opti.set_value(plane.oswaldEff, 0.7)
# opti.set_value(plane.banner_length, 7)

#M2
m2_ma = opti.maximize(M_2Score())

solm2 = opti.solve(verbose=False)

print("solm2 ducks" + str(solm2(plane.ducks)))
print("laps flown m2 " + str(solm2(laps_flown_M2)))

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

netScore = (GM_Score() / normalizedGM) + 1 + (1 + M_2Score() / normalizedM2) + (2 + M_3Score() / normalizedM3)

N = 20  # number of Monte Carlo draws
wind_speeds, wind_dirs = nd.sample_wind(N)

results = []

for ws, wd in zip(wind_speeds, wind_dirs):
    try:
        
        opti.set_value(plane.wind_speed, ws)
        opti.set_value(plane.wing_direction, wd)
        net_ma = opti.maximize(netScore - (plane.ducks - 3)**2)
        solNet = opti.solve()        # run CasADi solve
        results.append({
            'wind_speed': ws,
            'wind_dir': wd,
            'banner': solNet(plane.banner_length)
        })
    except RuntimeError as e:
        # e.g., optimizer didn't converge
        print("Failed here")

print(results)

# Extract banner lengths for all successful optimizations
banner_lengths = np.array([r['banner'] for r in results])

optimal_weighted_banner = banner_lengths.mean()
banner_std = banner_lengths.std()

print("Optimal weighted banner:", optimal_weighted_banner)
print("Std deviation:", banner_std)

net_ma = opti.maximize(netScore - (plane.ducks - 3)**2)
solNet = opti.solve()

ducks_val = float(solNet.value(plane.ducks))
pucks_val = float(solNet.value(plane.pucks))
S_ref_val = float(solNet.value(plane.S))

fusCD0 = solNet(aero.getFuselageCD0(plane.fuselage_length, plane.effective_diameter, plane.V_straight_M2, plane.fuselage_wetted_area, plane.S))


print("Wing weight ", mass.wing_weight(solNet(plane.span), solNet(plane.chord)))

print("Optimized M2 Ducks: ", solm2(plane.ducks))

lap_breakdown = constants.lap_breakdown
segment_dist = 2 * constants.straightDist / lap_breakdown

# Distance at the *center* of each segment
segment_centers = np.linspace(
    segment_dist/2,
    2 * constants.straightDist - segment_dist/2,
    lap_breakdown
)

V = solNet(plane.V_straight_M2)   # length = lap_breakdown

plt.plot(segment_centers, V, marker='o')  # connected dots
plt.xlabel("Distance along straight (m)")
plt.ylabel("Speed (m/s)")
plt.grid(True)
# plt.show()


print("\n=== Airplane Numbers ===")
print("Velocity turn M3: ", solNet(plane.V_turn_M3))
print("Turn radius M3 ", solNet(turn_radius_M3))
print(f"Span:                {solNet(plane.span):.3f} m")
print(f"Chord:               {solNet(plane.chord):.3f} m")
print("Velocities M3:  ", solNet(plane.V_straight_M3))
print("Velocities M2: ", solNet(plane.V_straight_M2))
# print(f"Airspeed M2:            {solNet(plane.V_straight_M2):.2f} m/s")
# print(f"Airspeed M3 (f):            {solNet(plane.V_straight_M3_f):.2f} m/s")
# print(f"Airspeed M3 (b):            {solNet(plane.V_straight_M3_b):.2f} m/s")
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
# print(f"Turn Load Factor M2:    {solNet(plane.n_turn_M2):.2f}")
# print(f"CL (Straight) M2:       {solNet(plane.CL_straight_M2):.3f}")
# print(f"CL (Turn) M2:           {solNet(plane.CL_turn_M2):.3f}")
print("Turn Radius M2: " + str(solNet(plane.turn_radius_M2)))
# print(f"Turn Radius M2: "      +  solNet(plane.V_turn_M2))
print(f"V_stall:             {solNet(V_stall):.2f} m/s")
# print(f"Lift (Straight) M2:     {solNet(lift_M2)/constants.g:.2f} kg")
# print(f"Lift (Turn) M2:         {solNet(lift_turn_M2)/constants.g:.2f} kg")
# print("Load factor: ", solNet(lift_turn_M2) / solNet(weight_M2))

print("\n=== Mass Breakdown ===")
print(f"Wing Mass:           {solNet(mass.wing_weight(plane.span, plane.chord)):.2f} kg")
print(f"Fuselage Mass:       {solNet(mass.fuselage_weight(plane.fuselage_area)):.2f} kg")
print(f"Cargo Mass:          {solNet(mass.cargo_mass(plane.ducks, plane.pucks)):.2f} kg")
print(f"Banner Mass:         {solNet(mass.banner_weight(plane.banner_length,    plane.banner_width)):.2f} kg") 
print(f"Towbar Mass:         {solNet(mass.towbar_weight(plane.banner_length)):.2f} kg")
print(f"Empennage Mass:      {solNet(mass.empenagge_mass()):.2f} kg")
print(f"Nose Section Mass:   {solNet(mass.nose_section_mass()):.2f} kg")
print(f"Additional AP Mass:  {solNet(mass.additional_ap_mass()):.2f} kg")
print(f"Fuselage Additional Mass:  {solNet(mass.fus_additional_mass(plane.ducks, plane.pucks)):.2f} kg")


print("\n=== Scoring ===")
print(f"GM Score:          {solNet(GM_Score() / normalizedGM):.2f}")
print(f"M2 Score:          {solNet(M_2Score() / normalizedM2):.2f}")
print(f"M3 Score:          {solNet(M_3Score() / normalizedM3):.2f}")

print(f"GM Raw Score:          {solNet(GM_Score()):.2f}")
print(f"M2 Raw Score:          {solNet(M_2Score()):.2f}")
print(f"M3 Raw Score:          {solNet(M_3Score()):.2f}")
print("Net Score: ", solNet(netScore))

print("\n=== Banner ===")
print(f"Banner Length:       {solNet(plane.banner_length):.2f} m")
print(f"Banner Width:        {solNet(plane.banner_width):.2f} m")

print("\n=== Drag Breakdown ===")

# print("zero lift drag M2 ", solNet(plane.zero_lift_drag))
# wingCD0 = aero.get_wing_cd0(solNet(plane.chord), solNet(plane.V_straight_M3_f))

# print("Total CD0 ", solNet(aero.get_total_CD0(wingCD0,fusCD0,htailCD0, vtailCD0)))

print("CD Straight Overall M2 ", (solNet(plane.CD_straight_M2)))
print("Velocities in M2 ", solNet(plane.V_straight_M2))

# print("Fus Drag M2 straight ", solNet(plane.fusdragM2_s))

print("Total Drag M3 straight ", solNet(plane.Drag_straight_M3_b))

# bannerdrag = solNet(aero.banner_drag(plane.banner_length, plane.banner_width, plane.V_straight_M3_b, plane.banner_cd_b))
# print("Banner drag", bannerdrag)

print("Fuselage wetted area ", solNet(plane.fuselage_wetted_area))
print("Fuselage drag M3 straight ", solNet(plane.fusdragM3_s_b))

# print("Drag Straight M2 ", solNet(plane.Drag_straight_M2))
# print("Fuselage CD0 ", solNet(aero.getFuselageCD0(plane.fuselage_length, plane.effective_diameter, plane.V_straight_M2, plane.fuselage_wetted_area, plane.S)))
# print("Fuselage drag M2 straight", solNet(plane.fusdragM2_s))

print("banner cd e", solNet(plane.banner_cd_b))

print("\n=== Fuselage Parameters")
print("Fuselage Length (m) ", solNet(plane.fuselage_length))
print("Fuselage Width (m) ", solNet(plane.fuselage_width))
print("Fuselage Height (m) ", solNet(plane.fuselage_height))

# print("Everything but banner drag M3 straight ", solNet(plane.Drag_straight_M3_b - bannerdrag))
# print("Fuselage CD0 ", solNet(aero.getFuselageCD0(plane.fuselage_length, plane.effective_diameter, plane.V_straight_M2, plane.fuselage_wetted_area, plane.S)))
def to_percent_change(val):
    return (val - 1) * 100 

"""

sweep_passengers = np.linspace(3, constants.duck_constraint, constants.duck_constraint - 2)
duck_target = opti.parameter()
mass_target = opti.parameter()
opti.maximize(netScore - (plane.ducks - duck_target)**2)
# sweep_passengers = np.linspace(3, 3, 1)
x_vals = []
y_vals = []

for i in sweep_passengers:
    print("Ducks: ", i)

    #opti.set_value(duck_target, i)
    opti.set_value(duck_target, i)

    try:
        sol = opti.solve(verbose=False)
        y_vals.append(sol.value(netScore))
        x_vals.append(sol.value(plane.ducks))
    except RuntimeError as e:
        print(f"Solver failed for {i} passengers ")

plt.plot(x_vals, y_vals, marker="o", linestyle= 'none')
plt.xlabel("Passengers")
plt.ylabel("Score (0-7)")
plt.title("Score vs Passengers")
plt.grid(True)
plt.show()

"""

# optimal framework
"""
denom = 3.5 * (plane.ducks + plane.pucks) + 20 + plane.ground_tax

x_vals = []
y_vals = []
netScore = (GM_Score() / normalizedGM) + 1 + (1 + M_2Score() / normalizedM2) + (2 + M_3Score() / normalizedM3)

normbanner = solNet(plane.banner_length)
sweep_length = np.linspace(normbanner*0.6, normbanner*1.4, 20)
normskin = solNet(plane.skin_friction_drag)
sweep_skin_friction = np.linspace(normskin*0.6, normskin*1.4, 20)
normspeed = solNet(plane.min_V3_speed)
sweep_speed = np.linspace(normspeed*0.6, normspeed*1.4, 20)
maxg = solNet(plane.max_g)
sweep_g = np.linspace(maxg*0.6, maxg*1.4, 20)
windspeed = solNet(plane.wind_speed)
sweep_wind = np.linspace(windspeed*0.6, windspeed*1.4, 20)
totalweight = solNet(weight_M3) #2.37 * constants.g
bannerCde = solNet(plane.banner_CD_e)
gmtime = solNet(GM_Score())

oswaldDefaultEff = solNet(plane.oswaldEff)
sweep_oswald = np.linspace(oswaldDefaultEff*0.6, oswaldDefaultEff*1.4, 20)

propDefault = solNet(plane.PropEff)
sweep_prop = np.linspace(propDefault*0.6, propDefault*1.4, 20)

defaultClmax = solNet(plane.CLmax)
sweep_Clmax = np.linspace(defaultClmax*0.6, defaultClmax*1.4, 20)

sweep_weight = np.linspace(-totalweight*1.03, totalweight*0.132, 20)
sweep_drag = np.linspace(bannerCde*0.6, bannerCde*1.4, 20)
sweep_gm = np.linspace(-14, 12.7, 20)

totaldrag = 42
sweep_f_drag = np.linspace(-0.8*totaldrag, totaldrag*0.6, 20)

opti.maximize(netScore - (plane.ducks - 3)**2 - (plane.span - 1.524)**2)

def run_sweep(value, sweep, middle_x, middle_y, extra):
    x_vals = []
    y_vals = []

    for w in sweep:
        opti.set_value(value, w)

        try:
            sol = opti.solve(verbose=False)
            x_vals.append(to_percent_change((sol(extra) / middle_x)))
            y_vals.append(to_percent_change((sol(netScore)) / middle_y))
            # y_vals.append(sol(netScore))
        except RuntimeError as e:
            print(f"Error for {w} vals")

    return x_vals, y_vals

x_weight = np.linspace(-40, 40, 20)
m = -1.73 / 40
b = 0
y_weight = m * x_weight + b

x_prop, y_prop = run_sweep(plane.PropEff, sweep_prop, propDefault, 6.0088, plane.PropEff)
x_Cl, y_Cl = run_sweep(plane.CLmax, sweep_Clmax, defaultClmax, 6.1423, plane.CLmax)
x_oswald, y_oswald = run_sweep(plane.oswaldEff, sweep_oswald, oswaldDefaultEff, 6.2116, plane.oswaldEff)
# Run sweeps for each variable you want to plot
x_gm, y_gm = run_sweep(plane.ground_tax, sweep_gm, 33.33, 6.2418, denom)       # Ground maneuver, this ones good
# x_wind, y_wind = run_sweep(plane.wind_speed, sweep_wind, windspeed, 5.70298, plane.wind_speed)  # Wind speed
x_g, y_g = run_sweep(plane.max_g, sweep_g, maxg, 5.651107, plane.max_g)        # Turn performance
# x_speed, y_speed = run_sweep(plane.min_V3_speed, sweep_speed, normspeed, 5.5, plane.min_V3_speed)  # Min speed
x_skin, y_skin = run_sweep(plane.skin_friction_drag, sweep_skin_friction, normskin, 5.9493, plane.skin_friction_drag)  # Skin friction
x_weight, y_weight = run_sweep(plane.extra_weight, sweep_weight, totalweight, 6.034, weight_M3)
x_banner, y_banner = run_sweep(plane.banner_CD_e, sweep_drag, bannerCde, 5.920429, plane.banner_CD_e)
# x_drag, y_drag = run_sweep(plane.extra_Drag_M3_s, sweep_f_drag, totaldrag, 5, plane.Drag_straight_M3_f)
# x_ban, y_ban = run_sweep(plane.banner_length, sweep_length, normbanner, 5, plane.banner_length)

x_weight = np.linspace(-40, 40, 20)
m = -1.73 / 40
b = 0
y_weight = m * x_weight + b

# plt.plot(x_ban, y_ban, label="Banner Length")
# Plot all lines on the same axes
plt.plot(x_gm, y_gm, label="Ground Mission Time")
#plt.plot(x_wind, y_wind, label="Wind Speed") 
# plt.plot(x_g, y_g, label="Turn Performance")
# plt.plot(x_speed, y_speed, label="Min Speed")
plt.plot(x_skin, y_skin, label="Skin Friction Drag")
# mask = (x_weight >= -40) & (x_weight <= 40)
# plt.plot(x_weight[mask], y_weight[mask], label="Weight")
plt.plot(x_weight, y_weight, label="Weight")
plt.plot(x_banner, y_banner, label="Banner CD")
plt.plot(x_oswald, y_oswald, label="Oswald Efficiency")
plt.plot(x_Cl, y_Cl, label="CLmax")
plt.plot(x_prop, y_prop, label="Propulsive Efficiency")

# Add labels, grid, and legend
# plt.xlim(-40, 40)
# Labels with larger font
# Labels with larger font
# Labels with larger font
plt.xlabel("% Change in Variable (+/-)", fontsize=18)
plt.ylabel("% Change in Score (+/-)", fontsize=18)

# Title with larger font
# plt.title("Score Sensitivity to Parameters: M3", fontsize=16)

# Grid
plt.grid(True)
plt.gca().set_box_aspect(1)


# Legend: outside the plot, top right, larger font + box
plt.legend(
    loc='upper right',  # inside top-right corner
    fontsize=13,
    frameon=True
)

plt.tight_layout()  # adjust plot so labels/legend don’t overlap
plt.show()

"""
"""
for w in sweep_gm: # for w in sweep_weight (sweep_drag)
    # opti.set_value(plane.banner_CD_e, w) # opti.set_value(plane.extra_weight, w)
    opti.set_value(plane.ground_tax, w)
    try:
        sol = opti.solve(verbose=False)
        
        # x_vals.append(to_percent_change(sol(plane.banner_CD_e) / bannerCde)) #x_vals.append(to_percent_change((sol(weight_M3) / constants.g) / 2.37))
        x_vals.append(to_percent_change((sol(denom) / 33.33)))
        y_vals.append(to_percent_change((sol(netScore)) / 6.032)) # 6.0078 for weight 6.0832 for banner CD
    except RuntimeError as e:
        print(f"error for {w} drag")
print(x_vals)
"""
#plt.plot(x_vals, y_vals)
#plt.xlabel("% Change in Variable (+/-)")
#plt.ylabel("% Change in Score (+/-)")
#plt.title("Score vs Skin Friction Drag")
#plt.grid(True)
#plt.show()

"""

totalweight = 2.37

totalDrag = 42 #N
sweep_drag = np.linspace(-totalDrag*0.8, totalDrag*0.6, 20)
sweep_weight = np.linspace(-totalweight*0.2, totalweight*0.2, 20)

weight_tot_targ = opti.parameter()
dragtarg = opti.parameter()
weight_targ = opti.parameter()
ducktarg = opti.parameter()
opti.maximize(netScore - ((plane.ducks - ducktarg)**2 - (weight_M3 - weight_tot_targ)**4))
# sweep_passengers = np.linspace(3, 3, 1)
x_vals = []
y_vals = []

def to_percent_change(val):
    return (val - 1) * 100

for i in sweep_weight:
    print("Drag: ", i)

    

    #opti.set_value(duck_target, i)
    opti.set_value(weight_targ, i)
    opti.set_value(ducktarg, 3)
    opti.set_value(weight_tot_targ, i+totalweight)

    try:
        sol = opti.solve(verbose=False)
        #y_vals.append(to_percent_change(sol.value(netScore)))   # 5.81 for drag
        y_vals.append(to_percent_change(sol.value(netScore)/5.9975))
        x_vals.append(to_percent_change((sol.value(weight_M3)/totalweight)))
        #x_vals.append(sol(plane.extra_weight))
        print("Total weight for M3 ", sol(weight_M3))
    except RuntimeError as e:
        print(f"Solver failed for {i} passengers ")

y_vals = y_vals
x_vals = x_vals

plt.plot(x_vals, y_vals)
plt.xlabel("% Change in Variable (+/-)")
plt.ylabel("% Change in Score (+/-)")
plt.title("Score vs Drag: M3")
plt.grid(True)
plt.show()
"""


"""

totalweight = 21.5

totalDrag = 42 #N
sweep_drag = np.linspace(0, totalDrag*0.6, 20)

dragtarg = opti.parameter()
weight_targ = opti.parameter()
ducktarg = opti.parameter()
opti.maximize(netScore - (plane.Drag_straight_M3_b - dragtarg)**2 - (plane.ducks - ducktarg)**2 - (plane.span - 1.524)**2)
# sweep_passengers = np.linspace(3, 3, 1)
x_vals = []
y_vals = []

def to_percent_change(val):
    return (val - 1) * 100

for i in sweep_drag:
    print("Drag: ", i)

    

    #opti.set_value(duck_target, i)
    opti.set_value(dragtarg, i)
    opti.set_value(ducktarg, 3)

    try:
        sol = opti.solve(verbose=False)
        #y_vals.append(to_percent_change(sol.value(netScore)))   # 5.81 for drag
        y_vals.append(to_percent_change(sol.value(netScore)/5.667))
        # y_vals.append(sol.value(netScore))
        x_vals.append(sol(plane.Drag_straight_M3_f))
        # x_vals.append(sol(plane.Drag_straight_M3_f))
        #x_vals.append(sol(plane.extra_weight))
        print("Total weight for M3 ", sol(plane.Drag_straight_M3_b))
    except RuntimeError as e:
        print(f"Solver failed for {i} passengers ")

y_vals = y_vals
x_vals = x_vals

plt.plot(x_vals, y_vals)
plt.xlabel("% Change in Variable (+/-)")
plt.ylabel("% Change in Score (+/-)")
plt.title("Score vs Drag: M3")
plt.grid(True)
plt.show()







"""


