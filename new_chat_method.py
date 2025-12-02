import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt

### 1. Define a finite wing
wing = asb.Wing(
    name="Main Wing",
    symmetric=True,
    xsecs=[
        asb.WingXSec(   # Root
            xyz_le=[0, 0, 0],
            chord=1.5,
            twist=0,
            airfoil=asb.Airfoil("naca2412")
        ),
        asb.WingXSec(   # Tip
            xyz_le=[0.5, 5, 0],
            chord=0.5,
            twist=0,
            airfoil=asb.Airfoil("naca2412")
        )
    ]
)

### 2. Define operating conditions
op_point = asb.OperatingPoint(
    velocity=50,     # m/s
    alpha=5,         # degrees
    beta=0,
    p=0, q=0, r=0
)

### 3. Set up the VLM problem
vlm = asb.aerodynamics.aero_3D.VortexLatticeMethod(
    airplane=asb.Airplane(
        wings=[wing]
    ),
    op_point=op_point,
    spanwise_resolution=50,   # More panels = smoother distribution
    chordwise_resolution=8
)

### 4. Run the solver
results = vlm.run()

### 5. Extract spanwise positions & sectional lift coefficients
ys = vlm.y_panels                # Spanwise y-coordinates
cls = vlm.cl_sections             # Sectional lift coefficients

### 6. Plot c_l vs span
plt.figure()
plt.plot(ys, cls)
plt.xlabel("Spanwise Position y [m]")
plt.ylabel("Sectional Lift Coefficient c_l")
plt.title("Spanwise Lift Distribution")
plt.grid(True)
plt.show()
