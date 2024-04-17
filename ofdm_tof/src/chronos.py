from .csi_poller import CSIGenerator
from .utils import interpolate_zsc
import numpy as np
from typing import Union
from scipy import signal

class Chronos():
    def __init__(self,
                 freq_range: tuple[int, int],
                 n_freq: int,
                 n_periods: int,
                 n_frames: int) -> None:
        self.frequencies = np.random.randint(*freq_range, n_freq)
        self.n_periods = n_periods
        self.n_frames = n_frames
        self.generator = CSIGenerator(conflate = True)

    def start(self) -> None:
        self.generator.start()

    def scan_freq_zsc_phase(self, freq) -> np.ndarray:
        self.generator.set_center_freq(freq)
        out = np.zeros((self.n_periods, self.n_frames, 2), dtype=float)
        # TODO: opt by collecting all data and applying angle/interpolate
        for period in range(self.n_periods):
            self.generator.switch()

            for frame in range(self.n_frames):
                # out[period, frame, 0] = np.angle(self.generator.get_csi_rx()[1])[33]
                out[period, frame, 0] = interpolate_zsc(
                    np.angle(self.generator.get_csi_rx()[1])
                )

            self.generator.switch()

            for frame in range(self.n_frames):
                # out[period, frame, 1] = np.angle(self.generator.get_csi_rx()[1])[33]
                out[period, frame, 1] = interpolate_zsc(
                    np.angle(self.generator.get_csi_rx()[1])
                )
        return out

    def compute_tof(self, freq: int) -> float:
        # scan [period, frame, 2] -> zero subcarrier phases
        # TODO: make sure you can square/sqrt the phases rather than complexes.
        scan = self.scan_freq_zsc_phase(freq)
        period_tofs = []
        for period in scan:
            forward = period[:, 0]
            backward = period[:, 1]
            # forward = np.sqrt(np.abs(forward * backward))
            period_tofs.append(np.mean(forward)/(2 * np.pi * freq))
        # return period_tofs
        return np.mean(period_tofs)

    def all_dists(self) -> list[float]:
        return [self.compute_tof(freq) * 300000000  for freq in self.frequencies]
