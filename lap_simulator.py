import math
import mass_buildup as mass
import constants
import aero_functions as aero
import casadi as ca
import numpy as np

def lap_sim(self, opti):

    lap_breakdown = constants.lap_breakdown
    lap_breakdown_turn = constants.lap_breakdown_turn
    distance_breakdown = 2 * constants.straightDist / lap_breakdown

    # --------- Variables ---------
    self.V_straight_M1 = opti.variable(init_guess=[30]*lap_breakdown, lower_bound=1)
    self.V_straight_M2 = opti.variable(init_guess=[30]*lap_breakdown, lower_bound=1)
    self.V_straight_M3 = opti.variable(init_guess=[30]*lap_breakdown, lower_bound=1)
    self.V_turn_M2     = opti.variable(init_guess=[30]*lap_breakdown_turn, lower_bound=1)
    self.wing_direction = opti.parameter() # ca.pi / 220 # ca.pi / 5 # opti.parameter() # -pi to pi
    self.wind_speed = opti.parameter() # m/s

    Vwx = self.wind_speed * ca.cos(self.wing_direction)
    Vwy = self.wind_speed * ca.sin(self.wing_direction)


    # self.V_turn_M3     = opti.variable(init_guess=[30]*lap_breakdown_turn, lower_bound=0)
    self.n_turn_M2     = opti.variable(init_guess=[3]*lap_breakdown_turn, lower_bound=1, upper_bound=constants.n_max)
    # self.h_turn_M2     = opti.variable(init_guess=[1]*lap_breakdown_turn, lower_bound=-15, upper_bound=15)

    # opti.subject_to(self.h_turn_M2[0] == constants.initial_height)

    # --------- Allocate arrays ---------
    self.M1_CL_list_s        = [None] * lap_breakdown
    self.M2_CL_list_s        = [None] * lap_breakdown
    self.M3_CL_list_s        = [None] * lap_breakdown
    self.wingCD0_M1_s        = [None] * lap_breakdown
    self.wingCD0_M2_s        = [None] * lap_breakdown
    self.wingCD0_M3_s        = [None] * lap_breakdown
    self.fusCD0_M1_s         = [None] * lap_breakdown
    self.fusCD0_M2_s         = [None] * lap_breakdown
    self.fusCD0_M3_s         = [None] * lap_breakdown
    self.zero_lift_drag_M1_s = [None] * lap_breakdown
    self.zero_lift_drag_M2_s = [None] * lap_breakdown
    self.zero_lift_drag_M3_s = [None] * lap_breakdown
    self.CD_straight_M1      = [None] * lap_breakdown
    self.CD_straight_M2      = [None] * lap_breakdown
    self.CD_straight_M3      = [None] * lap_breakdown
    self.Drag_straight_M1    = [None] * lap_breakdown
    self.Drag_straight_M2    = [None] * lap_breakdown
    self.Drag_straight_M3    = [None] * lap_breakdown
    self.power_straight_M1   = [None] * lap_breakdown
    self.power_straight_M2   = [None] * lap_breakdown
    self.power_straight_M3   = [None] * lap_breakdown
    self.t_straight_M1       = [None] * lap_breakdown
    self.t_straight_M2       = [None] * lap_breakdown
    self.t_straight_M3       = [None] * lap_breakdown
    self.E_lap_M1_straight   = [None] * lap_breakdown
    self.E_lap_M2_straight   = [None] * lap_breakdown
    self.E_lap_M3_straight   = [None] * lap_breakdown
    self.Banner_CD           = [None] * lap_breakdown
    self.altitude_gain       = [None] * lap_breakdown

    # turn parameters
    self.CD_turn_M2          = [None] * lap_breakdown_turn
    self.CL_turn_M2          = [None] * lap_breakdown_turn
    self.wingCD0_M2_t        = [None] * lap_breakdown_turn
    self.fusCD0_M2_t         = [None] * lap_breakdown_turn
    self.zero_lift_drag_M2_t = [None] * lap_breakdown_turn
    self.Drag_turn_M2        = [None] * lap_breakdown_turn
    self.turn_radius_M2      = [None] * lap_breakdown_turn
    self.power_turn_M2       = [None] * lap_breakdown_turn
    self.t_turn_M2           = [None] * lap_breakdown_turn
    self.e_turn_M2           = [None] * lap_breakdown_turn
    self.delta_PE            = [None] * lap_breakdown_turn

    # Induced drag factor
    self.k = constants.inducedDragFactor / (np.pi * self.oswaldEff * self.AR)


    for i in range(lap_breakdown_turn):

        


        v_t_M2 = self.V_turn_M2[i]
        n_turn_M2 = self.n_turn_M2[i]
        self.turn_radius_M2[i] = v_t_M2 ** 2 / (constants.g * ca.sqrt(n_turn_M2**2 - 1))
        self.CL_turn_M2[i] = n_turn_M2 * mass.get_weight(self.span, self.chord, self.ducks
                                                                 , self.pucks, 0, 0, self.restraint_weight
                                                                 , self.fuselage_area) / (0.5
                                                                                           * constants.rho * self.S * v_t_M2**2)
        self.wingCD0_M2_t[i] = aero.get_wing_cd0(self.chord, v_t_M2)
        self.fusCD0_M2_t[i] = aero.getFuselageCD0(self.fuselage_length, self.effective_diameter, v_t_M2, self.fuselage_wetted_area, self.S)
        self.zero_lift_drag_M2_t[i] = constants.zero_lift_correction_factor * (
            self.wingCD0_M2_t[i] +
            self.fusCD0_M2_t[i] +
            self.CD0_tail
        )

        self.CD_turn_M2[i] = self.zero_lift_drag_M2_t[i] + self.k * self.CL_turn_M2[i] ** 2

        self.Drag_turn_M2[i] = (
            0.5 * constants.rho * v_t_M2**2 * self.S * self.CD_turn_M2[i]
        )

        self.power_turn_M2[i] = self.Drag_turn_M2[i] * v_t_M2
        
        distance = (ca.pi * 4 * self.turn_radius_M2[i]) / lap_breakdown_turn

        # if i > 0:
        #     dh = self.h_turn_M2[i] - self.h_turn_M2[i-1]
        # else:
        #     dh = 0

        mass_total = mass.get_weight(self.span, self.chord, self.ducks
                                                                 , self.pucks, 0, 0, self.restraint_weight
                                                                 , self.fuselage_area)

        # self.delta_PE[i] = mass_total * constants.g * dh


        self.t_turn_M2[i] = (distance) / (v_t_M2)

        self.e_turn_M2[i] = self.power_turn_M2[i] * self.t_turn_M2[i] # + self.delta_PE[i]

    for i in range(1, lap_breakdown_turn):
        # _i     = self.V_turn_M2[i-1]
        # v_next  = self.V_turn_M2[i]
       # drag_i  = self.Drag_turn_M2[i-1]
        # dPE_i   = self.delta_PE[i-1]
        opti.subject_to(self.V_turn_M2[i] >= 0.9 * self.V_turn_M2[i-1])
        opti.subject_to(self.V_turn_M2[i] <= 1.1 * self.V_turn_M2[i-1])
        opti.subject_to(self.CL_turn_M2[i] <= constants.CLmax)

        # opti.subject_to(
        #     0.5 * mass_total * v_next**2
        #    ==
        #     0.5 * mass_total * v_i**2
        #     - dPE_i
        #     - drag_i * distance_breakdown
        # )


        # opti.subject_to(self.turn_radius_M2[i] >= 5)

    left  = 0
    right = lap_breakdown_turn - 1

    while left < right:
        opti.subject_to(self.turn_radius_M2[left] == self.turn_radius_M2[right])
        left  += 1
        right -= 1


    self.t_turn_total_M2 = sum(self.t_turn_M2)
    self.e_turn_total_M2 = sum(self.e_turn_M2)

    # --------- Loop through straight segments ---------
    for i in range(lap_breakdown):

        # Example: self.straight_heading[i] = heading of segment in radians


        if i > 9:
            # write in the wind direction
            heading = -ca.pi

        else:
            heading = 0
            # write in the wind direction opposite

        
        v_s_ground_M1 = self.V_straight_M1[i]
        v_s_ground_M2 = self.V_straight_M2[i]
        v_s_ground_M3 = self.V_straight_M3[i]

        Vg_x_M2 = v_s_ground_M2 * ca.cos(heading)
        Vg_y_M2 = v_s_ground_M2 * ca.sin(heading)

        Va_x_M1 = v_s_ground_M1 * ca.cos(heading) - Vwx
        Va_y_M1 = v_s_ground_M1 * ca.sin(heading) - Vwy

        Va_M1 = ca.sqrt(Va_x_M1**2 + Va_y_M1**2) # replacing all aerodynamics with airspeed

        Va_x_M2 = Vg_x_M2 - Vwx
        Va_y_M2 = Vg_y_M2 - Vwy
        Va_M2 = ca.sqrt(Va_x_M2**2 + Va_y_M2**2) # replacing all aerodynamics with airspeed

        Va_x_M3 = v_s_ground_M3 * ca.cos(heading) - Vwx
        Va_y_M3 = v_s_ground_M3 * ca.sin(heading) - Vwy

        Va_M3 = ca.sqrt(Va_x_M3**2 + Va_y_M3**2) # replacing all aerodynamics with airspeed

        self.M1_CL_list_s[i] = (
            mass.get_weight(self.span, self.chord, 0, 0,
                            0, 0, self.restraint_weight, self.fuselage_area)
            / (0.5 * constants.rho * self.S * Va_M1**2)
        )

        self.M2_CL_list_s[i] = (
            mass.get_weight(self.span, self.chord, self.ducks, self.pucks,
                            0, 0, self.restraint_weight, self.fuselage_area)
            / (0.5 * constants.rho * self.S * Va_M2**2)
        )

        self.M3_CL_list_s[i] = (
            (mass.get_weight(self.span, self.chord, 0, 0,
                              self.banner_length, self.banner_width, 0, self.fuselage_area))
                                / (0.5 * constants.rho * self.S * Va_M3**2)
        )

        self.wingCD0_M1_s[i] = aero.get_wing_cd0(self.chord, Va_M1)
        self.wingCD0_M2_s[i] = aero.get_wing_cd0(self.chord, Va_M2)
        self.wingCD0_M3_s[i] = aero.get_wing_cd0(self.chord, Va_M3)
        
        self.fusCD0_M1_s[i]  = aero.getFuselageCD0(
            self.fuselage_length, self.effective_diameter,  
            Va_M1, self.fuselage_wetted_area, self.S
        )

        self.fusCD0_M2_s[i]  = aero.getFuselageCD0(
            self.fuselage_length, self.effective_diameter,
            Va_M2, self.fuselage_wetted_area, self.S
        )
        self.fusCD0_M3_s[i]  = aero.getFuselageCD0(
            self.fuselage_length, self.effective_diameter,
            Va_M3, self.fuselage_wetted_area, self.S
        )

        self.zero_lift_drag_M1_s[i] = constants.zero_lift_correction_factor * (
            self.wingCD0_M1_s[i] + 
            self.fusCD0_M1_s[i] +
            self.CD0_tail
        )

        self.zero_lift_drag_M2_s[i] = constants.zero_lift_correction_factor * (
            self.wingCD0_M2_s[i] +
            self.fusCD0_M2_s[i] +
            self.CD0_tail
        )

        self.zero_lift_drag_M3_s[i] = constants.zero_lift_correction_factor * (
            self.wingCD0_M3_s[i] +
            self.fusCD0_M3_s[i] +
            self.CD0_tail
        )

        self.CD_straight_M1[i] = (
            self.CD0_factor * self.zero_lift_drag_M1_s[i] + self.k * self.M1_CL_list_s[i]**2
        )

        self.CD_straight_M2[i] = (
            self.CD0_factor * self.zero_lift_drag_M2_s[i] + self.k * self.M2_CL_list_s[i]**2
        )

        self.CD_straight_M3[i] = (
            self.CD0_factor * self.zero_lift_drag_M3_s[i] + self.k * self.M3_CL_list_s[i]**2
        )

        self.Drag_straight_M1[i] = (
            0.5 * constants.rho * Va_M1**2 * self.S * self.CD_straight_M1[i]
        )

        self.Drag_straight_M2[i] = (
            0.5 * constants.rho * Va_M2**2 * self.S * self.CD_straight_M2[i]
        )

        self.Banner_CD[i] = aero.get_banner_cd(aero.get_Reynolds(self.banner_length, Va_M3))

        self.Drag_straight_M3[i] = (
            0.5 * constants.rho * Va_M3**2 * self.S * self.CD_straight_M3[i] + aero.banner_drag(self.banner_length, self.banner_width, Va_M3, self.Banner_CD[i])
        )

        self.power_straight_M1[i] = self.Drag_straight_M1[i] * Va_M1

        self.power_straight_M2[i] = self.Drag_straight_M2[i] * Va_M2

        self.power_straight_M3[i] = self.Drag_straight_M3[i] * Va_M3

        self.t_straight_M1[i] = distance_breakdown / ca.fabs(v_s_ground_M1)

        self.t_straight_M2[i] = distance_breakdown / ca.fabs(v_s_ground_M2)

        self.t_straight_M3[i] = distance_breakdown / ca.fabs(v_s_ground_M3)

        self.E_lap_M1_straight[i] = (
            self.power_straight_M1[i] * self.t_straight_M1[i]
        )

        self.E_lap_M2_straight[i] = (
            self.power_straight_M2[i] * self.t_straight_M2[i]
        )

        self.E_lap_M3_straight[i] = (
            self.power_straight_M3[i] * self.t_straight_M3[i]
        )

    # --------- Velocity adjacency constraints ---------
    #    v[i] must be within 90–110% of v[i-1]
    mid  = lap_breakdown // 2
    last = lap_breakdown - 1
    
    first = 0
    last_turn = lap_breakdown_turn - 1
    

    for i in range(1, lap_breakdown):
        opti.subject_to(self.V_straight_M1[i] >= 0.9 * self.V_straight_M1[i-1])
        opti.subject_to(self.V_straight_M1[i] <= 1.1 * self.V_straight_M1[i-1])
        opti.subject_to(self.V_straight_M2[i] >= 0.9 * self.V_straight_M2[i-1])
        opti.subject_to(self.V_straight_M2[i] <= 1.1 * self.V_straight_M2[i-1])
        opti.subject_to(self.V_straight_M3[i] >= 0.9 * self.V_straight_M3[i-1])
        opti.subject_to(self.V_straight_M3[i] <= 1.1 * self.V_straight_M3[i-1])
        # opti.subject_to(self.V_straight_M3[i] >= 20)  # min speed for M3
        opti.subject_to(self.M1_CL_list_s[i] <= constants.CLmax)
        opti.subject_to(self.M2_CL_list_s[i] <= constants.CLmax)
        opti.subject_to(self.M3_CL_list_s[i] <= constants.CLmax)
        # opti.subject_to(self.V_straight_M3[i] >= 16)
        # opti.subject_to(self.V_straight_M3[i] >= 16)

    # straight ↔ turn velocity consistency
    opti.subject_to(self.V_straight_M1[mid] >= 0.9 * self.V_turn_M1)
    opti.subject_to(self.V_straight_M1[mid] <= 1.1 * self.V_turn_M1)
    opti.subject_to(self.V_straight_M1[last] >= 0.9 * self.V_turn_M1)
    opti.subject_to(self.V_straight_M1[last] <= 1.1 * self.V_turn_M1)
    opti.subject_to(self.V_straight_M2[mid]  >= 0.9 * self.V_turn_M2[first])
    opti.subject_to(self.V_straight_M2[mid]  <= 1.1 * self.V_turn_M2[first])
    opti.subject_to(self.V_straight_M2[last] >= 0.9 * self.V_turn_M2[last_turn])
    opti.subject_to(self.V_straight_M2[last] <= 1.1 * self.V_turn_M2[last_turn])
    opti.subject_to(self.V_straight_M3[mid]  >= 0.9 * self.V_turn_M3)
    opti.subject_to(self.V_straight_M3[mid]  <= 1.1 * self.V_turn_M3)
    opti.subject_to(self.V_straight_M3[last] >= 0.9 * self.V_turn_M3)
    opti.subject_to(self.V_straight_M3[last] <= 1.1 * self.V_turn_M3)

    # ugly subject to

    # opti.subject_to(self.h_turn_M2[0] == self.h_turn_M2[1])
    # opti.subject_to(self.h_turn_M2[6] == self.h_turn_M2[7])
    # opti.subject_to(self.h_turn_M2[2] == self.h_turn_M2[5])
    # opti.subject_to(self.h_turn_M2[1] == self.h_turn_M2[2])
    # opti.subject_to(self.h_turn_M2[5] == self.h_turn_M2[6])



    # --------- Lap time & laps flown ---------

    self.e_straight_total_M1 = sum(self.E_lap_M1_straight)
    self.t_straight_total_M1 = sum(self.t_straight_M1)

    self.t_straight_total_M2 = sum(self.t_straight_M2)
    self.e_straight_total_M2 = sum(self.E_lap_M2_straight)

    self.average_load_M1 = (sum(p**2 for p in self.power_straight_M1) / lap_breakdown)**0.5

    self.average_load_M2 = (sum(p**2 for p in self.power_straight_M2) / lap_breakdown)**0.5

    self.t_straight_total_M3 = sum(self.t_straight_M3)
    self.e_straight_total_M3 = sum(self.E_lap_M3_straight)

    self.average_load_M3 = sum(self.power_straight_M3) / lap_breakdown

    self.average_M2_drag_straight = sum(self.Drag_straight_M2) / lap_breakdown
    self.average_M3_drag_straight = sum(self.Drag_straight_M3) / lap_breakdown

    self.average_velocity_M1 = ca.sum1(self.V_straight_M1) / lap_breakdown
    self.average_velocity_M2 = ca.sum1(self.V_straight_M2) / lap_breakdown
    self.average_velocity_M3 = ca.sum1(self.V_straight_M3) / lap_breakdown