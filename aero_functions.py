def equivalentAirspeed2trueAirspeed(eas: float, altitude: float) -> float:
    """Convert equivalent airspeed to true airspeed using altitude in meters."""
    return eas * (1 + altitude * 0.0000068756) ** 2


def trueAirspeed2equivalentAirspeed(tas: float, altitude: float) -> float:
    """Convert true airspeed to equivalent airspeed using altitude in meters."""
    return tas / (1 + altitude * 0.0000068756) ** 2


def equivalentAirspeed2trueAirspeedFromDensity(eas, local_density, standard_density):
    """Convert equivalent airspeed to true airspeed using local and standard density."""
    return eas * (local_density / standard_density) ** 0.5


def trueAirspeed2equivalentAirspeedFromDensity(tas, local_density, standard_density):
    """Convert true airspeed to equivalent airspeed using local and standard density."""
    return tas / (local_density / standard_density) ** 0.5
