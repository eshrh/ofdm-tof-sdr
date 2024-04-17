import numpy as np
from scipy import signal

def interpolate_zsc(phi: np.ndarray) -> complex:
    mins, maxs = signal.argrelmin(phi)[0], signal.argrelmax(phi)[0]
    mins = mins[phi[mins] < -2]
    maxs = maxs[phi[maxs] > 2]

    mins = mins[mins > 32]
    maxs = maxs[maxs < 32]
    if len(maxs) == 0 or len(mins) == 0:
        print("error")
        return 0
    x = np.array([maxs[-1], mins[0]])
    y = phi[x]
    slope = (y[-1] - y[0])/(x[-1] - x[0])
    return slope * (32 - x[0]) + y[0]
