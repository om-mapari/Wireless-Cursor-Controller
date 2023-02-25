# Gesture Encodings
from enum import IntEnum


class Gest(IntEnum):
    # Binary Encoded
    """
    Enum for mapping all hand gesture to binary number.
    """
    # thumb index middle ring pinkie
    FIST = 0  # 00000
    PINKY = 1  # 00001
    RING = 2  # 00010
    MID = 4  # 00100
    LAST3 = 7  # 00111
    INDEX = 8  # 01000
    FIRST2 = 12  # 01100
    LAST4 = 15  # 01111
    THUMB = 16  # 10000
    PALM = 31  # 11111

    # Extra Mappings
    V_GEST = 33
    TWO_FINGER_CLOSED = 34
    PINCH_MAJOR = 35
    PINCH_MINOR = 36
