"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import time

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, time_per_state=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.port = pmt.intern("port")
        self.message_port_register_out(self.port)
        self.time_per_state = time_per_state
        self.last_switched = time.time()
        self.state = 0
        print("initialized")

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        now = time.time()
        if now - self.last_switched > self.time_per_state:
            self.state = int(not self.state)
            self.message_port_pub(
                self.port,
                pmt.cons(pmt.PMT_NIL, pmt.from_long(self.state))
            )
            self.last_switched = now
        return 0
