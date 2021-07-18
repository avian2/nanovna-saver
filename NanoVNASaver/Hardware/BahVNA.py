# vi:tabstop=4:expandtab:sw=4
import logging

from NanoVNASaver.Hardware.NanoVNA import NanoVNA
from NanoVNASaver.Hardware.Serial import Interface

logger = logging.getLogger(__name__)

class BahVNA(NanoVNA):
    name = "BahVNA"

    def __init__(self, iface: Interface):
        super().__init__(iface)
        self.sweep_max_freq_Hz = 6000e6
