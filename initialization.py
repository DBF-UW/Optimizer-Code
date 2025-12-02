# this will lay out the full initialization of all parameters
import constants
import aero_functions as aero
import numpy as np
import mass_buildup as mass
        

def velocity_parm(self, opti):
      # Velocity parameters
       #  self.V_straight_M2 = opti.variable(init_guess=30, lower_bound=0)
      #  self.V_turn_M2 = opti.variable(init_guess=25, lower_bound=0)
       # self.V_straight_M3_f = opti.variable(init_guess=30, lower_bound=0)
       # self.V_straight_M3_b = opti.variable(init_guess=30, lower_bound=0)
        self.V_turn_M3 = opti.variable(init_guess=25, lower_bound=0)

def mission_parm(self, opti):
        self.restraint_weight = 0

        self.banner_length = opti.variable(init_guess=1, lower_bound=0.0)
        self.banner_width = opti.variable(init_guess=1, lower_bound=0.0)

        self.ducks = opti.variable(init_guess=3, lower_bound=1)
        self.pucks = opti.variable(init_guess=1, lower_bound=1)

def airplane_parm(self, opti):
          # Airplane specific parameters
        
        self.span = opti.variable(init_guess=4, lower_bound=0) #global
        self.chord = opti.variable(init_guess=1, lower_bound=0) #global
        self.n_turn_M2 = opti.variable(init_guess=3, lower_bound=1, upper_bound=constants.n_max)
        self.n_turn_M3 = opti.variable(init_guess=3, lower_bound=1, upper_bound=constants.n_max)

        self.S = self.span * self.chord
        self.AR = self.span**2 / self.S

        self.l_ht = constants.tailArmH
        self.l_vt = constants.tailArmV

        self.S_ht = constants.tail_VH * self.S * self.chord / self.l_ht
        self.S_vt = constants.tail_VV * self.S * self.span  / self.l_vt

        # Simple wetted-area estimate for thin tails
        self.Swet_ht = 2.0 * self.S_ht
        self.Swet_vt = 2.0 * self.S_vt

def CD_planform(self, opti):
         # Lumped parasitic drag increment from tails (added to CD0)

        self.CD0_tail = aero.get_CD0_tail(self.Swet_ht, self.Swet_vt, self.S)

        #induced drag
        self.k = 1 / (np.pi * self.oswaldEff * self.AR) # constants.oswaldEff

        #lift
        # self.CL_straight_M2  = mass.get_weight(self.span, self.chord, self.ducks, self.pucks, 0, 0, self.restraint_weight, self.fuselage_area) / (0.5 * constants.rho * self.S * self.V_straight_M2**2)
      #  self.CL_turn_M2 = self.n_turn_M2 * mass.get_weight(self.span, self.chord, self.ducks, self.pucks, 0, 0, self.restraint_weight, self.fuselage_area) / (0.5 * constants.rho * self.S * self.V_turn_M2**2)

       # self.CL_straight_M3_f = (mass.get_weight(self.span, self.chord, 0, 0, self.banner_length, self.banner_width, 0, self.fuselage_area) + self.extra_weight) / (0.5 * constants.rho * self.S * self.V_straight_M3_f**2)
       # self.CL_straight_M3_b = (mass.get_weight(self.span, self.chord, 0, 0, self.banner_length, self.banner_width, 0, self.fuselage_area) + self.extra_weight) / (0.5 * constants.rho * self.S * self.V_straight_M3_b**2)
        self.CL_turn_M3 = self.n_turn_M3 * (mass.get_weight(self.span, self.chord, 0, 0, self.banner_length, self.banner_width, 0, self.fuselage_area) + self.extra_weight) / (0.5 * constants.rho * self.S * self.V_turn_M3**2)

        # self.wingCD0_M2_s = aero.get_wing_cd0(self.chord, self.V_straight_M2)
        # self.fusCD0_M2_s = aero.getFuselageCD0(self.fuselage_length, self.effective_diameter, self.V_straight_M2, self.fuselage_wetted_area, self.S)
      #  self.wingCD0_M2_t = aero.get_wing_cd0(self.chord, self.V_turn_M2)
       # self.fusCD0_M2_t = aero.getFuselageCD0(self.fuselage_length, self.effective_diameter, self.V_turn_M2, self.fuselage_wetted_area, self.S)
        # self.wingCD0_M3_s_f = aero.get_wing_cd0(self.chord, self.V_straight_M3_f)
        # self.wingCD0_M3_s_b = aero.get_wing_cd0(self.chord, self.V_straight_M3_b)

        self.CD0_tail = aero.get_CD0_tail(self.Swet_ht, self.Swet_vt, self.S)

        # self.CD_straight_M2 = self.skin_friction_drag + self.k * self.CL_straight_M2**2
      #  self.CD_turn_M2 = self.skin_friction_drag + self.k * self.CL_turn_M2 ** 2

       # self.CD_straight_M3_b = self.skin_friction_drag + self.k * self.CL_straight_M3_b**2
       # self.CD_straight_M3_f = self.skin_friction_drag + self.k * self.CL_straight_M3_f**2
        self.CD_turn_M3 = self.skin_friction_drag + self.k * self.CL_turn_M3**2

def powerParm(self, opti):
        # self.power_straight_M2 = self.Drag_straight_M2 * self.V_straight_M2
       # self.power_turn_M2 = self.Drag_turn_M2 * self.V_turn_M2

       # self.power_straight_M3_f = self.Drag_straight_M3_f * self.V_straight_M3_f
       # self.power_straight_M3_b = self.Drag_straight_M3_b * self.V_straight_M3_b
        self.power_turn_M3 = self.Drag_turn_M3 * self.V_turn_M3
        

def sweepParm(self, opti):
        self.extra_Drag_M3_s = opti.variable(init_guess=0, lower_bound=0)
        #self.extra_weight = opti.variable(init_guess=0, lower_bound=-1)
        self.extra_weight = opti.parameter()
        self.banner_CD_e = opti.parameter()
        self.ground_tax = opti.parameter()
        self.wind_speed = opti.parameter()
        self.min_V3_speed = opti.parameter()
        self.max_g = opti.parameter()
        self.skin_friction_drag = opti.parameter()
        self.oswaldEff = opti.parameter()
        self.CLmax = opti.parameter()
        self.PropEff = opti.parameter()

def fuselage_parm(self, opti):
        # fuselage optimization
        self.fuselage_length = opti.variable(init_guess=1.5)
        self.fuselage_width = opti.variable(init_guess = 0.1)
        self.fuselage_height = opti.variable(init_guess = 0.1)

        self.fus_usable_length = self.fuselage_length * 0.9

        self.fuselage_box_length = self.fuselage_length * 0.7

        #area constraints
        self.passenger_area = self.ducks*constants.duck_length*constants.duck_width #m^2
        self.battery_area = 0.011 #m^2
        self.total_area = (self.battery_area + self.passenger_area)*1.2

        #length constraints
        passenger_length = self.passenger_area/self.fuselage_width
        battery_length = self.battery_area/self.fuselage_width
        self.total_length = battery_length + passenger_length

        #volume constraints
        passenger_volume = self.passenger_area*constants.duck_height
        puck_volume = (3.14*(constants.puck_diameter/2)**2)*constants.puck_thickness/constants.PUCK_PACKING_COEFFICEINT
        self.total_volume = constants.FUSELAGE_PACKING_FACTOR*((puck_volume + passenger_volume)/0.7 + 0.05*0.05*0.15*3.5)/0.8

        #fuselage sizing numbers
        self.frontal_area = self.fuselage_height * self.fuselage_width
        self.effective_diameter = np.sqrt(self.frontal_area/3.14)*2
        self.fineness_ratio = self.fuselage_length/self.effective_diameter
       
        self.fuselage_wetted_area = (
                            2*(self.fuselage_height * self.fuselage_width) + #front/back
                            2*(self.fuselage_height * self.fuselage_length) + #sides
                            2*(self.fuselage_width * self.fuselage_length)) #tops
        
        self.fuselage_area = self.fuselage_wetted_area