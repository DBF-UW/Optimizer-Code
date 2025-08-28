import aerosandbox as asb
import aerosandbox.numpy as np
import constants
import unit_conversion as uc



# Example usage:
wing_airfoil = asb.Airfoil("sd7037")
tail_airfoil = asb.Airfoil("naca0010")

fuselage = asb.Fuselage(
    name = "Main Fuselage",
    xsecs=[
        asb.FuselageXSec( #nose
            xyz_c=[0, 0, 0],  # Position of the cross-section (meters)
            radius=0.2,        # Radius of the cross-section (meters)
        ),
        asb.FuselageXSec( #fuselageA
            xyz_c=[1, 0, 0],
            width = 1.2,
            height = 0.6,
        ),
        asb.FuselageXSec( #fuselageB
            xyz_c=[4, 0, 0],
            width = 1.0,
            height = 0.5,
        ),
        asb.FuselageXSec( #tail
            xyz_c=[5, 0, 0],
            radius=0.2
        ),
    ]
)

airplaneAeroModel = asb.Airplane(
    name="Test Airplane",
    fuselages = [fuselage],
    wings = [],
)

airplaneAeroModel.draw()


