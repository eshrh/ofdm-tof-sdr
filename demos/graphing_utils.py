from ofdm_tof.src.csi_poller import CSIGenerator
from typing import Callable, Optional, Any
import numpy as np
from matplotlib import animation as anim
import matplotlib as mpl
from matplotlib import pyplot as plt

def rolling(data, window):
    return np.mean(data[-window:])

def demo(generator: CSIGenerator,
         init_data: np.ndarray,
         interval: int = 100,
         frames: int = 10000,
         ax_init: Optional[Callable[[mpl.axes.Axes], None]] = None):
    def demo_func(animation_function: Callable[[CSIGenerator,
                                                int,
                                                mpl.axes.Axes,
                                                Any], None]):
        generator.start()
        mpl.style.use("ggplot")
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        def animation_function_wrapper(frame):
            ax.clear()
            animation_function(generator, frame, ax, init_data)
            if ax_init is not None:
                ax_init(ax)

        anim_obj = anim.FuncAnimation(fig, animation_function_wrapper,
                                      interval=interval, frames=frames)
        plt.show()
    return demo_func
