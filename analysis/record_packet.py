from ofdm_tof.src.csi_poller import CSIGenerator
import numpy as np
import time

def one_way(frames, filename):
    gen = CSIGenerator(conflate = True)
    gen.start()
    gen.switch()
    out = np.zeros((frames, 64), dtype=complex)
    for i in range(frames):
        out[i] = gen.get_csi(gen.current_rx)[1]
    np.save(filename, out)
    gen.stop()

def ofdm_tof_long(frames, periods, filename):
    gen = CSIGenerator(conflate = True)
    gen.start()
    out = np.zeros((periods, frames, 2, 64), dtype=complex)
    for period in range(periods):
        gen.switch()

        for frame in range(frames):
            out[period, frame, 0] = gen.get_csi(gen.current_rx)[1]

        gen.switch()
        # time.sleep(0.05)

        for frame in range(frames):
            out[period, frame, 1] = gen.get_csi(gen.current_rx)[1]
    np.save(filename, out)


# one_way(20000, "/home/esrh/ofdm_tof/data/test.npy")
ofdm_tof_long(10000, 2, "/home/esrh/ofdm_tof/data/ofdm_tof_long.npy")

# gen = CSIGenerator(conflate = False)
# gen.start()
# out = gen.record_and_save()
