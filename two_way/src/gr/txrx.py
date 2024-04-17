#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: TXRX
# GNU Radio version: 3.10.9.2

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from rx_chain import rx_chain  # grc-generated hier_block
from sinksource import sinksource  # grc-generated hier_block


def snipfcn_snippet_0(self):
    gr.logging().set_default_level(gr.log_levels.warn)


def snippets_init_before_blocks(tb):
    snipfcn_snippet_0(tb)


class txrx(gr.top_block):

    def __init__(self, center_freq=2e9, external_clock=0, samp_rate=2e6, sdr_0='serial= 316405A', sdr_1='serial= 316407B', sdr_channel_0=0, sdr_channel_1=0, sync="pc"):
        gr.top_block.__init__(self, "TXRX", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.center_freq = center_freq
        self.external_clock = external_clock
        self.samp_rate = samp_rate
        self.sdr_0 = sdr_0
        self.sdr_1 = sdr_1
        self.sdr_channel_0 = sdr_channel_0
        self.sdr_channel_1 = sdr_channel_1
        self.sync = sync

        ##################################################
        # Blocks
        ##################################################
        snippets_init_before_blocks(self)
        self.zeromq_sub_msg_source_1 = zeromq.sub_msg_source('tcp://127.0.0.1:1235', 100, False)
        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source('tcp://127.0.0.1:1234', 100, False)
        self.sinksource_1 = sinksource(
            center_freq=center_freq,
            channel=sdr_channel_1,
            external_clock=external_clock,
            samp_rate=samp_rate,
            sdr=sdr_1,
            sync=sync,
        )
        self.sinksource_0 = sinksource(
            center_freq=center_freq,
            channel=sdr_channel_0,
            external_clock=external_clock,
            samp_rate=samp_rate,
            sdr=sdr_0,
            sync=sync,
        )
        self.rx_chain_1 = rx_chain(
            fft_len=64,
            port='2000',
            samp_rate=2e6,
        )
        self.rx_chain_0 = rx_chain(
            fft_len=64,
            port='2001',
            samp_rate=samp_rate,
        )
        self.digital_ofdm_tx_0 = digital.ofdm_tx(
            fft_len=64,
            cp_len=16,
            packet_length_tag_key="packet_len",
            occupied_carriers=(list(range(-26, -21)) + list(range(-20, -7)) + list(range(-6, 0)) + list(range(1, 7)) + list(range(8, 21)) + list(range(22, 27)),),
            pilot_carriers=((-21, -7, 7, 21,),),
            pilot_symbols=((1, 1, 1, -1,),),
            sync_word1=[0., 0., 0., 0., 0., 0., 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 0., 0., 0., 0., 0.],
            sync_word2=[0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 0, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
            bps_header=1,
            bps_payload=1,
            rolloff=0,
            debug_log=False,
            scramble_bits=False)
        self.blocks_tag_gate_1 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_1.set_single_key("")
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 64, "packet_len")
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.005)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 1000))), True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.blocks_selector_0, 'oindex'))
        self.msg_connect((self.zeromq_sub_msg_source_1, 'out'), (self.sinksource_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_1, 'out'), (self.sinksource_0, 'msg_in2'))
        self.msg_connect((self.zeromq_sub_msg_source_1, 'out'), (self.sinksource_1, 'msg_in2'))
        self.msg_connect((self.zeromq_sub_msg_source_1, 'out'), (self.sinksource_1, 'msg_in'))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.sinksource_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.sinksource_1, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.rx_chain_1, 0))
        self.connect((self.blocks_tag_gate_1, 0), (self.rx_chain_0, 0))
        self.connect((self.digital_ofdm_tx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.sinksource_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.sinksource_1, 0), (self.blocks_tag_gate_1, 0))


    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.sinksource_0.set_center_freq(self.center_freq)
        self.sinksource_1.set_center_freq(self.center_freq)

    def get_external_clock(self):
        return self.external_clock

    def set_external_clock(self, external_clock):
        self.external_clock = external_clock
        self.sinksource_0.set_external_clock(self.external_clock)
        self.sinksource_1.set_external_clock(self.external_clock)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rx_chain_0.set_samp_rate(self.samp_rate)
        self.sinksource_0.set_samp_rate(self.samp_rate)
        self.sinksource_1.set_samp_rate(self.samp_rate)

    def get_sdr_0(self):
        return self.sdr_0

    def set_sdr_0(self, sdr_0):
        self.sdr_0 = sdr_0
        self.sinksource_0.set_sdr(self.sdr_0)

    def get_sdr_1(self):
        return self.sdr_1

    def set_sdr_1(self, sdr_1):
        self.sdr_1 = sdr_1
        self.sinksource_1.set_sdr(self.sdr_1)

    def get_sdr_channel_0(self):
        return self.sdr_channel_0

    def set_sdr_channel_0(self, sdr_channel_0):
        self.sdr_channel_0 = sdr_channel_0
        self.sinksource_0.set_channel(self.sdr_channel_0)

    def get_sdr_channel_1(self):
        return self.sdr_channel_1

    def set_sdr_channel_1(self, sdr_channel_1):
        self.sdr_channel_1 = sdr_channel_1
        self.sinksource_1.set_channel(self.sdr_channel_1)

    def get_sync(self):
        return self.sync

    def set_sync(self, sync):
        self.sync = sync
        self.sinksource_0.set_sync(self.sync)
        self.sinksource_1.set_sync(self.sync)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--external-clock", dest="external_clock", type=intx, default=0,
        help="Set external clock [default=%(default)r]")
    parser.add_argument(
        "--sdr-0", dest="sdr_0", type=str, default='serial= 316405A',
        help="Set sdr 0 [default=%(default)r]")
    parser.add_argument(
        "--sdr-1", dest="sdr_1", type=str, default='serial= 316407B',
        help="Set sdr 1 [default=%(default)r]")
    parser.add_argument(
        "--sdr-channel-0", dest="sdr_channel_0", type=intx, default=0,
        help="Set sdr channel 0 [default=%(default)r]")
    parser.add_argument(
        "--sdr-channel-1", dest="sdr_channel_1", type=intx, default=0,
        help="Set sdr channel 1 [default=%(default)r]")
    parser.add_argument(
        "--sync", dest="sync", type=str, default="pc",
        help="Set pc [default=%(default)r]")
    return parser


def main(top_block_cls=txrx, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(external_clock=options.external_clock, sdr_0=options.sdr_0, sdr_1=options.sdr_1, sdr_channel_0=options.sdr_channel_0, sdr_channel_1=options.sdr_channel_1, sync=options.sync)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
