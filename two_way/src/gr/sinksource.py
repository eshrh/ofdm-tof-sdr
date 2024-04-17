# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: sinksource
# Description: a sink and a source!
# GNU Radio version: 3.10.9.2

from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from gnuradio import uhd
import time


def snipfcn_snippet_0(self):
    if external_clock:
        self.uhd_usrp_sink_node1.set_clock_source("external", 0)
        self.uhd_usrp_source_node1.set_clock_source("external", 0)
    else:
        self.uhd_usrp_sink_node1.set_clock_source("internal", 0)
        self.uhd_usrp_source_node1.set_clock_source("internal", 0)

    if sync == "pc":
        self.uhd_usrp_sink_node1.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.uhd_usrp_source_node1.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
    elif sync == "pps":
        self.uhd_usrp_sink_node1.set_time_unknown_pps(uhd.time_spec(0))
        self.uhd_usrp_source_node1.set_time_unknown_pps(uhd.time_spec(0))


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)





class sinksource(gr.hier_block2):
    def __init__(self, center_freq=2e9, channel=0, external_clock=0, samp_rate=2e6, sdr="", sync=""):
        gr.hier_block2.__init__(
            self, "sinksource",
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )
        self.message_port_register_hier_in("msg_in")
        self.message_port_register_hier_in("msg_in2")

        ##################################################
        # Parameters
        ##################################################
        self.center_freq = center_freq
        self.channel = channel
        self.external_clock = external_clock
        self.samp_rate = samp_rate
        self.sdr = sdr
        self.sync = sync

        ##################################################
        # Blocks
        ##################################################

        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join((sdr, '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_subdev_spec("A:A" if channel==0 else "A:B", 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_source_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_source_0.set_bandwidth(20e6, 0)
        self.uhd_usrp_source_0.set_normalized_gain(1, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join((sdr, '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_clock_source('external', 0)
        self.uhd_usrp_sink_0.set_subdev_spec("A:A" if channel == 0 else "A:B", 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(20e6, 0)
        self.uhd_usrp_sink_0.set_normalized_gain(0.8, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self, 'msg_in'), (self.uhd_usrp_sink_0, 'command'))
        self.msg_connect((self, 'msg_in2'), (self.uhd_usrp_source_0, 'command'))
        self.connect((self, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self, 0))


    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel

    def get_external_clock(self):
        return self.external_clock

    def set_external_clock(self, external_clock):
        self.external_clock = external_clock

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_sdr(self):
        return self.sdr

    def set_sdr(self, sdr):
        self.sdr = sdr

    def get_sync(self):
        return self.sync

    def set_sync(self, sync):
        self.sync = sync

