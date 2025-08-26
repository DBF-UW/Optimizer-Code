"""
Manages the optimization process using contraints defined in constraints.py and missions defined in missions.py

Resources
---------
Wing optimization
    https://github.com/peterdsharpe/AeroSandbox/blob/master/tutorial/02%20-%20Design%20Optimization/02%20-%20Wing%20Drag%20Minimization%2C%20with%20practical%20considerations.ipynb
"""
import sys
print("aerosandbox" in sys.modules)


import aerosandbox as asb
import aerosandbox.numpy as np
import neuralfoil as nf

from casadi import casadi
from typing import Callable, Union

import constants
import unit_conversion as units

class Aircraft():
    """
    Aircraft class to manage global aircraft variables and functions.
    
    Attributes
    ----------
    airspeed : casadi.MX
        Velocity (m/s).
    alpha : casadi.MX
        Angle of attack (deg).
    span : casadi.MX
        Wing span (m).
    chords : casadi.MX
        Root and tip chord (m).

    """
    def __init__(self, opti:asb.Opti, airfoil:str='e216', fuse_weight:float=45, wing_density:float=20):
        """
        Aircraft __init__ method.

        Parameters
        ----------
        opti : asb.Opti
            Aerosandbox optimizer.
        airfoil : str
            Airfoil name or file to use
        fuse_weight : float
            Fusalage weight (N).
        wing_density : float
            Wing density (kg/m3).
        """
        # core constants
        self.fuse_w = fuse_weight
        self.wing_density = wing_density

        # core variables (MKS)
        self.airspeed = opti.variable(init_guess=30, lower_bound=0)

        self.alpha = opti.variable(init_guess=0, lower_bound=-10, upper_bound=10)
        self.alpha_max = opti.variable(init_guess=5, lower_bound=5, upper_bound=20)

        self.span = opti.variable(init_guess=1, lower_bound=0)
        self.chords = opti.variable(init_guess=np.ones(2) * 0.1, lower_bound=0)

        #self.payload = opti.variable(init_guess=0, lower_bound=0)

        self.cargo = opti.variable(init_guess=1, lower_bound=1)
        self.passengers = opti.variable(init_guess=3, lower_bound=3)

        self.banner_length = opti.variable(init_guess=10, lower_bound=10)
        self.banner_width = opti.variable(init_guess=2, lower_bound=2)

        # airfoil optimization
        # this optimization was stolen directly from the tutorial...
        # not sure what should go into the optimzation
        self.airfoil = None
        if airfoil == "opti":
            initial_guess = asb.KulfanAirfoil("e216")
            self.airfoil = asb.KulfanAirfoil(
                name="optimized",
                lower_weights=opti.variable(
                    init_guess=initial_guess.lower_weights,
                    lower_bound=-0.5,
                    upper_bound=0.25,
                ),
                upper_weights=opti.variable(
                    init_guess=initial_guess.upper_weights,
                    lower_bound=-0.25,
                    upper_bound=0.5,
                ),
                leading_edge_weight=opti.variable(
                    init_guess=initial_guess.leading_edge_weight,
                    lower_bound=-1,
                    upper_bound=1,
                ),
                TE_thickness=0,
            )
        else:
            self.airfoil = asb.KulfanAirfoil(airfoil)

        # core geometry
        self.wing = asb.Wing(
            symmetric=True,
            xsecs=[
                asb.WingXSec(
                    xyz_le=[
                        -0.25 * self.chords[0],
                        0,
                        0
                    ],
                    chord=self.chords[0],
                    twist=0,
                    airfoil=self.airfoil
                ),
                asb.WingXSec(
                    xyz_le=[
                        -0.25 * self.chords[1],
                        self.span * 0.5,
                        0
                    ],
                    chord=self.chords[1],
                    twist=0,
                    airfoil=self.airfoil
                )
            ]
        )

        self.airplane = asb.Airplane(wings=[self.wing])

        # cruise aerodynamics
        op_point = asb.OperatingPoint(
            velocity=self.airspeed,
            alpha=self.alpha
        )

        self.vlm = asb.VortexLatticeMethod(
            airplane=self.airplane,
            op_point=op_point,
            spanwise_resolution=constants.SPAN_RESOLUTION,
            chordwise_resolution=constants.CHORCH_RESOLUTION,
        )

        self.aero = self.vlm.run()

        # turn aerodynamics
        op_point_turn = asb.OperatingPoint(
            velocity=self.airspeed,
            alpha=self.alpha_max
        )

        self.vlm_turn = asb.VortexLatticeMethod(
            airplane=self.airplane,
            op_point=op_point_turn,
            spanwise_resolution=constants.SPAN_RESOLUTION,
            chordwise_resolution=constants.CHORCH_RESOLUTION,
        )

        self.aero_turn = self.vlm_turn.run()
        

    def get_stall(self) -> Union[float, casadi.MX]:
        """
        Get the aircraft stall speed.

        Returns
        -------
        Union[float, casadi.MX]
            Stall speed (m/s) as a constant float or variable.
        """
        W = self.get_weight()
        rho = units.slugsPerFeetCubed2kgPerMeterCubed(constants.RHO)
        S = self.wing.area()
        CL_max = self.aero_turn['CL']

        return np.sqrt(2 * W / (rho * S * CL_max))

    def get_takeoff(self) -> Union[float, casadi.MX]:
        """
        Get the aircraft takeoff distance.

        Returns
        -------
        Union[float, casadi.MX]
            Takeoff distance (m) as a constant float or variable.
        """
        v = 0.7 * 1.2 * self.get_stall()
        W = self.get_weight()
        rho = units.slugsPerFeetCubed2kgPerMeterCubed(constants.RHO)
        g = constants.GRAVITATIONAL_ACCELERATION
        CL_max = self.aero_turn['CL']
        T = constants.DYNAMIC_THRUST(v)
        D = self.get_drag(v)
        L = self.get_lift(v)
        mu = constants.MU_ROLL

        return 1.44 * W * W / (g * rho * CL_max * (T - (D + mu * (W - L))))
    
    def get_lift(self, v:Union[float, casadi.MX]=None, turn:bool=False) -> Union[float, casadi.MX]:
        """
        Get the aircrafts lift force.

        Parameters
        ----------
        v : Union[float, casadi.MX]
            Velocity as a constant float or variable.
        turn : bool
            Turning lift

        Returns
        -------
        Union[float, casadi.MX]
            Lift force as a constant float or variable.
        """
        if v == None:
            v = self.airspeed

        if turn:
            cl = self.aero_turn['CL']
        else:
            cl = self.aero['CL']
        
        return 0.5 * constants.RHOS * v * v * self.wing.area() * cl

    def get_drag(self, v:Union[float, casadi.MX]=None, turn:bool=False) -> Union[float, casadi.MX]:
        """
        Get the aircrafts drag force.

        Parameters
        ----------
        v : Union[float, casadi.MX]
            Velocity as a constant float or variable.
        turn : bool
            Turning lift

        Returns
        -------
        Union[float, casadi.MX]
            Drag force as a constant float or variable.
        """
        if v == None:
            v = self.airspeed

        if turn:
            cd = self.aero_turn['CD']
        else:
            cd = self.aero['CD']

        A_banner = (self.banner_length ** 2) / 5
        CD_banner = 0.075
        D_banner = 0.5 * constants.RHOS * v * v * A_banner * CD_banner

        return 0.5 * constants.RHOS * v * v * self.wing.area() * cd + D_banner
    
    def get_load_factor(self) -> Union[float, casadi.MX]:
        """
        Get the aircrafts turning load.

        Returns
        -------
        Union[float, casadi.MX]
            Load factor.
        """
        l_max = self.get_lift(turn=True)
        weight = self.get_weight()

        n = l_max / weight # load factor

        return n
    
    def get_min_turning_radius(self) -> Union[float, casadi.MX]:
        """
        Get the aircrafts minimum turning radius.

        Returns
        -------
        Union[float, casadi.MX]
            Minimum turning radius.
        """
        n = self.get_load_factor()

        radius = self.airspeed * self.airspeed / (constants.GRAVITATIONAL_ACCELERATION * np.sqrt(n * n - 1))

        return radius

    def get_lap_distance(self) -> Union[float, casadi.MX]:
        """
        Get the aircraft lap distance for an AIAA lap.

        Returns
        -------
        Union[float, casadi.MX]
            AIAA lap time as a constant float or variable.
        """
        r = self.get_min_turning_radius()
        d = 4 * np.pi * r + (2 * units.feet2meters(constants.AIAA_LENGTH))

        return d  ##### intial approximation

    def get_lap_time(self) -> Union[float, casadi.MX]:
        """
        Get the aircraft lap time for an AIAA lap.

        Returns
        -------
        Union[float, casadi.MX]
            AIAA lap time as a constant float or variable.
        """
        #d = self.get_lap_distance()

        #return d / self.airspeed ##### intial approximation
        n = self.get_load_factor()
        rho = units.slugsPerFeetCubed2kgPerMeterCubed(constants.RHO)
        W = self.get_weight()
        S = self.wing.area()
        CL_max = self.aero_turn['CL']
        r = self.get_min_turning_radius()

        vstar = np.sqrt((2*n*W)/(rho*CL_max*S))

        return ((2 * units.feet2meters(constants.AIAA_LENGTH))/ self.airspeed) + ((4* np.pi * r)/ vstar)

    def get_passengers(self):
        return self.passengers
    
    def get_cargo(self):
        return self.cargo
    
    def get_wingspan(self):
        return self.span
    
    def get_banner_length(self):
        return self.banner_length
    

    def get_weight(self, payload:bool=False) -> Union[float, casadi.MX]:
        """
        Get the aircrafts total weight force.

        Parameters
        ----------
        payload : bool
            Get Payload weight (defualt=False).

        Returns
        -------
        Union[float, casadi.MX]
            Weight force as a constant float or variable.
        """
        # return payload weight
        if payload:
            return self.payload
        
        w = self.fuse_w # fusalage weight
        w += self.wing_density * self.wing.volume() * constants.GRAVITATIONAL_ACCELERATION # wing weight
        w += self.passengers * constants.PASSENGER_WEIGHT + self.passengers * constants.CARGO_WEIGHT

        return w

    def plot(self) -> None:
        """
        Plot geometry
        """
        self.airplane.draw()

    def plot_vlm(self) -> None:
        """
        Plot vortex latice solution
        """
        self.vlm.draw()

    def plot_lap(self) -> None:
        """
        Plot lap shape
        """

class Optimizer():
    """
    Opimizer class to manage multi optimization between missions.


    Attributes
    ----------
    opti : asb:Opti
        Aerosandbox optimizer.
    aircraft : Aircraft
        Aircraft object.
    **kwargs
        Key word arguments to pass to aircraft.
    """
    def __init__(self, **kwargs):
        """
        Optimizer __init__ method.
        """
        self.opti = None
        self.aircraft = None

        self.kwargs = kwargs

    def solve_mission(self, constraint_function:Callable[[asb.Opti, Aircraft], None], mission_function:Callable[[asb.Opti, Aircraft], casadi.MX]) -> tuple[float, Aircraft]:
        """
        Solve for the optimal aircraft of a single given mission.

        Parameters
        ----------
        constraint_function : Callable[[asb.Opti, Aircraft], None]
            Constraint function to assign constraints.
        mission_function : Callable[[asb.Opti, Aircraft], casadi.MX]
            Mission function to assign constraints and calculate score.

        Returns
        -------
        float
            Mission score.
        Aircraft
            Solved aircraft.
        """
        # define problem
        self.opti = asb.Opti()
        self.aircraft = Aircraft(self.opti, **self.kwargs)

        # objective
        score = mission_function(self.opti, self.aircraft)

        # constraints
        constraint_function(self.opti, self.aircraft)

        # solve
        self.opti.maximize(score)

        sol = self.opti.solve(
            max_iter=500,
            behavior_on_failure='return_last'
        )

        # return aircraft
        return sol(score), sol(self.aircraft)
    
    def solve_missions(self, constraint_function:Callable[[asb.Opti, Aircraft], None], *mission_functions:list[Callable[[asb.Opti, Aircraft], casadi.MX]]) -> tuple[list[float], list[Aircraft]]:
        """
        Solve for the optimal aircraft for all missions combined.

        Parameters
        ----------
        constraint_function : Callable[[asb.Opti, Aircraft], None]
            Constraint function to assign constraints.
        *mission_functions : list[Callable[[asb.Opti, Aircraft], casadi.MX]]
            Mission functions to assign constraints and calculate scores.

        Returns
        -------
        list[float]
            Mission scores (last is all missions).
        list[Aircraft]
            Solved aircrafts (last is all missions).
        """
        # create empty list of scores
        scores = []
        crafts = []

        # optimize for each mission
        for m_function in mission_functions:
            # find optimal
            score, craft = self.solve_mission(constraint_function, m_function)

            # store
            scores.append(score)
            crafts.append(craft)

        # create normalized mission function
        def normalized_scoring(opti:asb.Opti, aircraft:Aircraft) -> casadi.MX:
            score = 0

            # get combined score
            for i in range(len(mission_functions)):
                score += mission_functions[i](opti, aircraft, normalizer=scores[i])

            # return combined score
            return score

        # optimize
        score, craft = self.solve_mission(constraint_function, normalized_scoring)

        # store
        scores.append(score)
        crafts.append(craft)

        # output
        return scores, crafts
