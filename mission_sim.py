import aerosandbox as asb
import aerosandbox.numpy as np  
import constants
import unit_conversion as uc    
import aircraft
import constraints
import simple_lap_simulator

max_M2_score = 2200
max_M3_score = 2

def GM (aircraft:"aircraft.Aircraft"):
    return (1.5 * (aircraft.cargo + aircraft.passengers)) + 15

def M1 (aircraft:"aircraft.Aircraft", lapper:"simple_lap_simulator.LapSimulator") -> float:
    return 1

def M2 (aircraft:"aircraft.Aircraft", lapper:"simple_lap_simulator.LapSimulator") -> float:
    passengers = aircraft.passengers
    cargo = aircraft.cargo
    laps = lapper.laps_flown
    #Incomes
    Ip1 = constants.PASSENGER_INCOME_FIXED
    Ip2 = constants.PASSENGER_INCOME_LAP
    Ic1 = constants.CARGO_INCOME_FIXED
    Ic2 = constants.CARGO_INCOME_LAP

    #Costs
    Ce = constants.BASE_OPERATING_COST
    Cp = constants.PER_PASSENGER_COST
    Cc = constants.PER_CARGO_COST
    efficiencyFactor = aircraft.propulsion_energy / (3600*100)

    income = (passengers * (Ip1 + (Ip2 * laps)) + cargo * (Ic1 + (Ic2 * laps)))
    cost = laps * (Ce + (passengers * Cp) + (cargo * Cc)) * efficiencyFactor

    net_income = income - cost
    return net_income

def M3 (aircraft:"aircraft.Aircraft", lapper:"simple_lap_simulator.LapSimulator") -> float:
    RAC = 0.05 * aircraft.span + 0.75
    laps = lapper.laps_flown
    banner_length = aircraft.banner_length
    score = (banner_length * laps) / RAC
    return score