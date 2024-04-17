from ofdm_tof.src.csi_poller import CSIGenerator
from ofdm_tof.src.utils import interpolate_zsc
from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib import animation
import numpy as np
from array import array
from demos.graphing_utils import demo, rolling
import pandas as pd

cf = 4.25e8

def axis_init(ax: mpl.axes.Axes):
    ax.set_title(f"Phase demonstration @ {cf}Hz")
    ax.set_ybound(lower=-np.pi, upper=np.pi)
    ax.set_ylabel("Phase")
    ax.set_xlabel("Frame number")


@demo(CSIGenerator(external_clock=True, center_freq=cf, conflate=True),
      (array('f'), array('f')),
      ax_init = axis_init,
      interval=50)
def demo_2(gen, frame, ax, data):
    data_33, data_31 = data
    csi = gen.get_csi_rx()[1]

    data_33.append(np.angle(csi[33]))
    data_31.append(np.angle(csi[31]))

    # rolling_31, rolling_33 = tuple(map(lambda x: rolling(x, 10), [data_31, data_33]))
    # print(rolling_31, rolling_33, rolling_31 - rolling_33)
    ax.plot(pd.Series(data_31[-500:]).rolling(5).mean())
    ax.plot(pd.Series(data_33[-500:]).rolling(5).mean())

if __name__ == "__main__":
    demo_2()
