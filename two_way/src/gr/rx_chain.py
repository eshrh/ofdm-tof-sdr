# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: OFDM rx (zmq csi)
# GNU Radio version: 3.10.9.2

from gnuradio import blocks
from gnuradio import digital
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from gnuradio import zeromq







class rx_chain(gr.hier_block2):
    def __init__(self, fft_len=64, port='2000', samp_rate=2e6):
        gr.hier_block2.__init__(
            self, "OFDM rx (zmq csi)",
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
                gr.io_signature(0, 0, 0),
        )

        ##################################################
        # Parameters
        ##################################################
        self.fft_len = fft_len
        self.port = port
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.pilot_symbols = pilot_symbols = ((1, 1, 1, -1,),)
        self.pilot_carriers = pilot_carriers = ((-21, -7, 7, 21,),)
        self.payload_mod = payload_mod = digital.constellation_bpsk()
        self.occupied_carriers = occupied_carriers = (list(range(-26, -21)) + list(range(-20, -7)) + list(range(-6, 0)) + list(range(1, 7)) + list(range(8, 21)) + list(range(22, 27)),)
        self.length_tag_key_rx = length_tag_key_rx = "frame_len"
        self.length_tag_key = length_tag_key = "packet_len"
        self.header_mod = header_mod = digital.constellation_bpsk()
        self.sync_word2 = sync_word2 = [0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 0, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 0, 0, 0, 0, 0]
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0., 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 0., 0., 0., 0., 0.]
        self.rolloff = rolloff = 0
        self.payload_equalizer = payload_equalizer = digital.ofdm_equalizer_simpledfe(fft_len, payload_mod.base(), occupied_carriers, pilot_carriers, pilot_symbols, 1)
        self.packet_len = packet_len = 64
        self.header_formatter = header_formatter = digital.packet_header_ofdm(occupied_carriers, n_syms=1, len_tag_key=length_tag_key, frame_len_tag_key=length_tag_key_rx, bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol(), scramble_header=False)
        self.header_equalizer = header_equalizer = digital.ofdm_equalizer_simpledfe(fft_len, header_mod.base(), occupied_carriers, pilot_carriers, pilot_symbols)
        self.center_freq = center_freq = 2e9 - 2*2e7

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 64, "tcp://127.0.0.1:"+str(port), 100, True, (-1), '', True, True)
        self.fft_vxx_0_0 = fft.fft_vcc(fft_len, True, (), True, 1)
        self.digital_packet_headerparser_b_0 = digital.packet_headerparser_b(header_formatter.base())
        self.digital_ofdm_sync_sc_cfb_0 = digital.ofdm_sync_sc_cfb(fft_len, (fft_len//4), False, 0.9)
        self.digital_ofdm_serializer_vcc_header = digital.ofdm_serializer_vcc(fft_len, occupied_carriers, length_tag_key_rx, '', 0, '', True)
        self.digital_ofdm_frame_equalizer_vcvc_0 = digital.ofdm_frame_equalizer_vcvc(header_equalizer.base(), (fft_len//4), length_tag_key_rx, True, 1)
        self.digital_ofdm_chanest_vcvc_0 = digital.ofdm_chanest_vcvc(sync_word1, sync_word2, 1, 0, 3, False)
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
            3,
            fft_len,
            (fft_len//4),
            length_tag_key_rx,
            "",
            True,
            gr.sizeof_gr_complex,
            "rx_time",
            int(samp_rate),
            (),
            0)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(header_mod.base())
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*64)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, (fft_len+fft_len//4))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_packet_headerparser_b_0, 'header_data'), (self.digital_header_payload_demux_0, 'header_data'))
        self.connect((self.blocks_delay_0, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_packet_headerparser_b_0, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.digital_ofdm_chanest_vcvc_0, 0), (self.digital_ofdm_frame_equalizer_vcvc_0, 0))
        self.connect((self.digital_ofdm_chanest_vcvc_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.digital_ofdm_frame_equalizer_vcvc_0, 0), (self.digital_ofdm_serializer_vcc_header, 0))
        self.connect((self.digital_ofdm_serializer_vcc_header, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0, 0), (self.blocks_null_sink_1, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0, 1), (self.digital_header_payload_demux_0, 1))
        self.connect((self.fft_vxx_0_0, 0), (self.digital_ofdm_chanest_vcvc_0, 0))
        self.connect((self, 0), (self.blocks_delay_0, 0))
        self.connect((self, 0), (self.digital_ofdm_sync_sc_cfb_0, 0))


    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_header_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, header_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols))
        self.set_payload_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, payload_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols, 1))
        self.blocks_delay_0.set_dly(int((self.fft_len+self.fft_len//4)))

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols
        self.set_header_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, header_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols))
        self.set_payload_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, payload_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols, 1))

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers
        self.set_header_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, header_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols))
        self.set_payload_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, payload_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols, 1))

    def get_payload_mod(self):
        return self.payload_mod

    def set_payload_mod(self, payload_mod):
        self.payload_mod = payload_mod

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers
        self.set_header_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, header_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols))
        self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, n_syms=1, len_tag_key=self.length_tag_key, frame_len_tag_key=self.length_tag_key_rx, bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol(), scramble_header=False))
        self.set_payload_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, payload_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols, 1))

    def get_length_tag_key_rx(self):
        return self.length_tag_key_rx

    def set_length_tag_key_rx(self, length_tag_key_rx):
        self.length_tag_key_rx = length_tag_key_rx
        self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, n_syms=1, len_tag_key=self.length_tag_key, frame_len_tag_key=self.length_tag_key_rx, bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol(), scramble_header=False))

    def get_length_tag_key(self):
        return self.length_tag_key

    def set_length_tag_key(self, length_tag_key):
        self.length_tag_key = length_tag_key
        self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, n_syms=1, len_tag_key=self.length_tag_key, frame_len_tag_key=self.length_tag_key_rx, bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol(), scramble_header=False))

    def get_header_mod(self):
        return self.header_mod

    def set_header_mod(self, header_mod):
        self.header_mod = header_mod

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_payload_equalizer(self):
        return self.payload_equalizer

    def set_payload_equalizer(self, payload_equalizer):
        self.payload_equalizer = payload_equalizer

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len

    def get_header_formatter(self):
        return self.header_formatter

    def set_header_formatter(self, header_formatter):
        self.header_formatter = header_formatter

    def get_header_equalizer(self):
        return self.header_equalizer

    def set_header_equalizer(self, header_equalizer):
        self.header_equalizer = header_equalizer

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq

