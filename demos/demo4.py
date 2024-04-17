from ofdm_tof.src.csi_poller import CSIGenerator
from ofdm_tof.src.utils import interpolate_zsc
from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib import animation
import numpy as np
from array import array

cf = 4.25e8
gen = CSIGenerator(external_clock=True, center_freq=cf, conflate=True)

gen.start()

periods = 2
frames = 500
out = np.zeros((frames, periods, 2), dtype=float)
for period in range(periods):
    gen.switch()

    for frame in range(frames):
        out[frame, period, 0] = interpolate_zsc(
            np.angle(gen.get_csi_rx()[1])
        )

    gen.switch()

    for frame in range(frames):
        out[frame, period, 1] = interpolate_zsc(
            np.angle(gen.get_csi_rx()[1])
        )

mpl.style.use("ggplot")
plt.plot(out[:, :, 0])
plt.plot(out[:, :, 1], linestyle="dotted")
plt.gca().set_title("Ping pong demo")
plt.gca().set_xlabel("Frame number")
plt.gca().set_ylabel("Phase")
plt.gca().set_ybound(lower=-np.pi, upper=np.pi)


plt.show()
