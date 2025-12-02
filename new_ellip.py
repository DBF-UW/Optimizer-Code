chord = 0.381
span = 1.524
 
import aerosandbox as asb
from aerosandbox.aerodynamics.aero_3D.aero_buildup import AeroBuildup

# 1. Build a wing / airplane geometry
wing = asb.Wing(
    name = "simple_wing",
    xs = [0, span/2, span/2, 0],   # simple rectangular planform: leading-edge x positions
    ys = [0, 0, span/2, span/2],   # wing half-span (assuming symmetric about centerline)
    chords = [chord, chord, chord, chord],
    twist = [0, 0, 0, 0],
    airfoil = asb.Airfoil("naca2412")  # example airfoil
)

airplane = asb.Airplane(
    name = "my_plane",
    wings = [wing],
    fuselages = [],  # none for now
)

# 2. Define an operating point
op = asb.OperatingPoint(
    velocity = 30,   # m/s, choose some flight speed
    alpha = 5,       # deg angle of attack
    beta = 0,        # sideslip
    rho = 1.225,     # air density kg/m3 (sea level)
    # you can add more options like gust, etc.
)

# 3. Instantiate AeroBuildup and run
ab = AeroBuildup(
    airplane = airplane,
    op_point = op,
    xyz_ref = [0, 0, 0],  # reference point for moments
    model_size = "small",
    include_wave_drag = False
)

aero = ab.run()

# 4. Extract results
lift = aero.L   # lift in N  (wind-axis)
drag = aero.D   # drag in N
CL = aero.CL()  # coefficient of lift
CD = aero.CD()  # coefficient of drag

print("Lift (N):", lift)
print("Drag (N):", drag)
print("CL, CD:", CL, CD)
