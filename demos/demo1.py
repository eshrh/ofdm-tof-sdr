from two_way.src.csi_poller import CSIGenerator
from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib import animation
import PyQt5
import numpy as np
from demos.graphing_utils import demo

@demo(CSIGenerator(external_clock=True, center_freq=2e8, conflate=True),
      None,
      ax_init = lambda ax: ax.set_ybound(lower=-np.pi, upper=np.pi))
def demo_1_csi(generator, frame, ax, data):
    csi = generator.get_csi_rx()[1]
    ax.plot(np.angle(csi))

if __name__ == "__main__":
    demo_1_csi()
