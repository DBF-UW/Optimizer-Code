from constants import GRAVITATIONAL_ACCELERATION
import aerosandbox.numpy as np


def celsius2fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit"""
    return celsius * 9 / 5 + 32


def fahrenheit2celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5 / 9


def celsius2kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin"""
    return celsius + 273.15


def kelvin2celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius"""
    return kelvin - 273.15


def celsius2rankine(celsius: float) -> float:
    """Convert Celsius to Rankine"""
    return celsius * 9 / 5 + 491.67


def rankine2celsius(rankine: float) -> float:
    """Convert Rankine to Celsius"""
    return (rankine - 491.67) * 5 / 9


def feet2meters(feet: float) -> float:
    """Convert feet to meters"""
    return feet * 0.3048


def meters2feet(meters: float) -> float:
    """Convert meters to feet"""
    return meters / 0.3048


def miles2meters(miles: float) -> float:
    """Convert miles to meters"""
    return miles * 1609.34


def meters2miles(meters: float) -> float:
    """Convert meters to miles"""
    return meters / 1609.34


def feetSquared2metersSquared(feet_squared: float) -> float:
    """Convert square feet to square meters"""
    return feet_squared * 0.092903


def metersSquared2feetSquared(meters_squared: float) -> float:
    """Convert square meters to square feet"""
    return meters_squared / 0.092903


def knots2metersPerSecond(knots: float) -> float:
    """Convert knots to meters per second"""
    return knots * 0.514444


def metersPerSecond2knots(mps: float) -> float:
    """Convert meters per second to knots"""
    return mps / 0.514444


def fpm2mps(fpm: float) -> float:
    """Convert feet per minute to meters per second"""
    return fpm * 0.00508


def mps2fpm(mps: float) -> float:
    """Convert meters per second to feet per minute"""
    return mps / 0.00508


def mph2mps(mph: float) -> float:
    """Convert miles per hour to meters per second"""
    return mph * 0.44704


def mps2mph(mps: float) -> float:
    """Convert meters per second to miles per hour"""
    return mps / 0.44704


def hp2watts(hp: float) -> float:
    """Convert horsepower to watts"""
    return hp * 745.7


def watts2hp(watts: float) -> float:
    """Convert watts to horsepower"""
    return watts / 745.7


def inhg2mbars(inhg: float) -> float:
    """Convert inches of mercury to millibars"""
    return inhg * 33.8639


def mbar2inhg(mbar: float) -> float:
    """Convert millibars to inches of mercury"""
    return mbar / 33.8639


def mbar2pascal(mbar: float) -> float:
    """Convert millibars to pascals"""
    return mbar * 100


def pascal2mbar(pascal: float) -> float:
    """Convert pascals to millibars"""
    return pascal / 100


def kg2lbs(kg: float) -> float:
    """Convert kilograms to pounds"""
    return kg * 2.20462


def lbs2kg(lbs: float) -> float:
    """Convert pounds to kilograms"""
    return lbs / 2.20462


def lbf2newtons(lbf: float) -> float:
    """Convert pounds-force to newtons"""
    return lbf * 4.44822


def newtons2lbf(newtons: float) -> float:
    """Convert newtons to pounds-force"""
    return newtons / 4.44822


def lnfperftSquared2mbars(lnfperft_squared: float) -> float:
    """Convert pounds-force per square foot to millibars"""
    return lnfperft_squared * 47.8803


def mbar2lnfperftSquared(mbar: float) -> float:
    """Convert millibars to pounds-force per square foot"""
    return mbar / 47.8803


def newtons2kg(newtons: float) -> float:
    """Convert newtons to kilograms"""
    return newtons / GRAVITATIONAL_ACCELERATION


def kg2newtons(kg: float) -> float:
    """Convert kilograms to newtons"""
    return kg * GRAVITATIONAL_ACCELERATION


def slugsPerFeetCubed2kgPerMeterCubed(slugs_per_feet_cubed: float) -> float:
    """Convert slugs per cubic foot to kilograms per cubic meter"""
    return slugs_per_feet_cubed * 515.379


def kgPerMeterCubed2slugsPerFeetCubed(kg_per_meter_cubed: float) -> float:
    """Convert kilograms per cubic meter to slugs per cubic foot"""
    return kg_per_meter_cubed / 515.379


def wattsPerNewton2hpPerKilogram(watts_per_newton: float) -> float:
    """Convert power to weight (Watt/N) to hp/kg"""
    return watts_per_newton * 0.00134102

def quadraticFormula(a: float, b: float, c: float) -> list:
    """pass in a,b,c into quadratic formula!!. first value with + second value with -"""
    d = b ** 2 - 4 * a * c
    if d < 0:
        return np.nan, np.nan
    value1 = -1 * b + np.sqrt(d) / (2 * a)
    value2 = -1 * b - np.sqrt(d) / (2 * a)
    return value1, value2
