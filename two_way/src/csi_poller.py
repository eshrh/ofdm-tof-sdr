import sys
import time
from subprocess import Popen, run, PIPE, DEVNULL
import zmq
import numpy as np
import pmt
from typing import Optional, Literal
import pickle
from .gr.txrx import txrx

class CSIGenerator:
    '''
    Class to poll and record CSI data
    '''
    def __init__(
            self,
            center_freq: float = 2e8,
            samp_rate: float = 2e6,
            conflate: bool = False,
            sdr_0: tuple[str, Literal[0, 1]] = ("serial= 316405A", 0),
            sdr_1: tuple[str, Literal[0, 1]] = ("serial= 316407B", 0),
            external_clock: bool = True,
            sync: Literal["pc", "pps"] = "pc"
    ) -> None:
        assert center_freq <= 6e9 and center_freq >= 1e7

        self.txrx = txrx(center_freq = center_freq,
                         samp_rate=samp_rate,
                         sdr_0 = sdr_0[0],
                         sdr_1 = sdr_1[0],
                         external_clock = external_clock,
                         sync = sync)

        context = zmq.Context()
        self.recv_sock_1 = context.socket(zmq.SUB)
        self.recv_sock_1.setsockopt_string(zmq.SUBSCRIBE, "")

        self.recv_sock_2 = context.socket(zmq.SUB)
        self.recv_sock_2.setsockopt_string(zmq.SUBSCRIBE, "")

        if conflate:
            self.recv_sock_1.setsockopt(zmq.CONFLATE, 1)
            self.recv_sock_2.setsockopt(zmq.CONFLATE, 1)

        self.recv_sock_2.connect("tcp://127.0.0.1:2001")
        self.recv_sock_1.connect("tcp://127.0.0.1:2000")

        self.sockets = [self.recv_sock_1, self.recv_sock_2]

        self.switch_sock = context.socket(zmq.PUB)
        self.switch_sock.bind("tcp://127.0.0.1:1234")

        self.radio_sock = context.socket(zmq.PUB)
        self.radio_sock.bind("tcp://127.0.0.1:1235")

        self.current_rx = 1  # default tx: radio 0 (405A)

        self.alive = False

    def start(self) -> None:
        '''
        Start the processes for the object, connect socket.
        '''
        self.txrx.start()
        time.sleep(0.5)
        self.alive = True


    def stop(self) -> None:
        '''
        Close everything
        '''
        if not self.alive:
            return
        self.txrx.stop()
        self.txrx.wait()

        self.recv_sock_1.close()
        self.recv_sock_2.close()
        self.switch_sock.close()

        self.alive = False

    def invert(self, socket: int) -> int:
        return (socket + 1) % 2

    def switch(self) -> None:
        if not self.alive:
            return
        # if current rx = 0, set to 1, send output to 0
        self.switch_sock.send(
            pmt.serialize_str(
                pmt.cons(pmt.PMT_NIL, pmt.from_long(self.current_rx))
            )
        )
        self.current_rx = self.invert(self.current_rx)

    def send_message(self, key, val) -> None:
        if not self.alive:
            return
        self.radio_sock.send(
            pmt.serialize_str(
                pmt.to_pmt(
                    {key: val}
                )
            )
        )

    def set_center_freq(self, center_freq: int) -> None:
        self.send_message("freq", int(center_freq))

    def set_gain(self, gain: float) -> None:
        self.send_message("gain", gain)

    def get_csi(self, socket_idx: int) -> tuple[float, np.ndarray]:
        data = self.sockets[socket_idx].recv()
        csi = np.array(pmt.to_python(pmt.deserialize_str(data[87:])))
        time_raw = pmt.to_python(pmt.deserialize_str(data[626:]))
        time = time_raw[0] + time_raw[1]
        return (time, csi)

    def get_csi_rx(self) -> tuple[float, np.ndarray]:
        return self.get_csi(self.current_rx)

    def record_and_save(self,
                        frames: int,
                        filename: Optional[str],
                        delay: float = 0.1) -> None:
        out = np.zeros((frames, 2, 64), dtype=complex)
        times = np.zeros((frames, 2))
        time.sleep(1)
        for i in range(frames):
            self.switch()

            time_1, csi_1 = self.get_csi(self.current_rx)
            out[i][1] = csi_1

            time_0, csi_0 = self.get_csi(self.invert(self.current_rx))
            out[i][0] = csi_0

            times[i][0] = time_0
            times[i][1] = time_1

            time.sleep(delay)
        if filename:
            with open(filename, "wb") as f:
                pickle.dump(out, f)
            with open("times.pkl", "wb") as f:
                pickle.dump(out, f)
        else:
            return out

if __name__=="__main__":
    frames = int(sys.argv[1])
    delay = float(sys.argv[2])
    filename = sys.argv[3]
    gen = CSIGenerator(conflate=True)
    gen.start()
    gen.record_and_save(frames, filename, delay)
