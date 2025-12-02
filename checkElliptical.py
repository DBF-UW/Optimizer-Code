import aerosandbox as asb
import numpy as np
import matplotlib.pyplot as plt
from aerosandbox.geometry.airfoil import Airfoil

chord = 0.381
span = 1.524
twist = 0
airspeed = 20
alpha = np.linspace(-40, 40, 100)

tol = 1e-2

# alpha = 0

SPAN_RESOLUTION = 120
CHORCH_RESOLUTION = 40

# airfoil = asb.KulfanAirfoil("naca2412")

#coords = np.loadtxt("C:\\Users\\Kesha\\Downloads\\6041.dat", skiprows=1)
#x = coords[:, 0]
#y = coords[:, 1]

# airfoil = asb.KulfanAirfoil.to_kulfan_airfoil(x, y)

airfoil = asb.KulfanAirfoil("naca2412")
airfoil = asb.Airfoil("naca2412")

# airfoil = Airfoil.from_dat("C:\\Users\\Kesha\\Downloads\\6041_new.dat")


wing = asb.Wing(
    symmetric=True,
    xsecs=[
        asb.WingXSec(
            xyz_le=[
                -0.25 * chord,
                0,
                0
            ],
            chord=chord,
            twist=twist,
            airfoil=airfoil
        ),
        asb.WingXSec(
            xyz_le=[
                -0.25 * chord,
                span * 0.5,
                0
            ],
            chord=chord,
            twist=0,
            airfoil=airfoil
        )
    ]
)

airplane = asb.Airplane(wings=[wing])

x_values = []
y_values = []
"""
for a in alpha:
    op_point = asb.OperatingPoint(
    velocity=airspeed,
    alpha=a
    )


    vlm = asb.VortexLatticeMethod(
    airplane=airplane,
    op_point=op_point,
    spanwise_resolution=SPAN_RESOLUTION,
    chordwise_resolution=CHORCH_RESOLUTION,
    align_trailing_vortices_with_wind=True
    )

    aero = vlm.run()

    x_values.append(a)
    y_values.append(aero["CD"])


plt.plot(x_values, y_values)
plt.show()
"""
alpha = 0


op_point = asb.OperatingPoint(
    velocity=airspeed,
    alpha=alpha
)

vlm = asb.VortexLatticeMethod(
    airplane=airplane,
    op_point=op_point,
    spanwise_resolution=SPAN_RESOLUTION,
    chordwise_resolution=CHORCH_RESOLUTION,
    align_trailing_vortices_with_wind=True
)

aero = vlm.run()


def plot_vlm():
    vlm.draw(show=True)

# plot_vlm()

# Given
CL = aero["CL"]
CD = aero["CD"]

print("This is aero keys", aero.keys())


print("parasitic CD: ", CD)

AR = 4

e = CL**2 / (np.pi * AR * CD)

print("Total CL:", CL)
print("Total CD:", CD)
print("Estimated Oswald efficiency:", e)

plot_vlm()

AR_vlm = vlm.airplane.b_ref**2 / vlm.airplane.s_ref

print("AR vlm:", AR_vlm)
