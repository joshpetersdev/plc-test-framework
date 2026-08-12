from enum import Enum


class PLCVendor(Enum):
    SIEMENS = "siemens"
    ALLEN_BRADLEY = "allen_bradley"
    SCHNEIDER = "schneider"
    SIMULATOR = "simulator"
