# normal distribution calcs

import numpy as np

def sample_wind(num_samples):
    # Example: Rayleigh distribution for speed, uniform for direction
    # Choose scale so mean ~ 10 mph (convert to m/s)
    mean_mph = 12.9 # average wind speed in mph
    mean_ms = mean_mph * 0.44704
    # Rayleigh scale parameter so that E[V] = scale * sqrt(pi/2)
    scale = mean_ms / np.sqrt(np.pi/2)
    speeds = np.random.rayleigh(scale, size=num_samples)
    directions = np.random.uniform(-np.pi, np.pi, size=num_samples)
    return speeds, directions