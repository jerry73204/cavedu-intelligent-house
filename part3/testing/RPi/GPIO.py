# Copyright (C) HENNES CO., LTD. - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written in May 2016 by
# Li-Wei Shih
# Hao-Yun Hsueh
# Feng-Chih Hsu
# Hsiang-Jiu Lin
# Cheng-Chang Liu
# Pei-Hsuan Yan
"""This file is created as a dummy RPi.GPIO package intended for testing purpose"""

import random
import sys

BCM = 0

IN  = 0
OUT = 1

PIN_MAPPINGS = dict()

def setmode(mode):
    pass

def setup(pin, pin_type):
    PIN_MAPPINGS[pin] = pin_type

def input(pin):
    assert PIN_MAPPINGS[pin] == IN
    print 'pin %d input: ' % pin
    sys.stdout.flush()
    value = sys.stdin.readline() != '0\n'
    # value = 1 if random.randint(1, 10) >= 8 else 0
    print('> GPIO pin %d in %d' % (pin, value))
    return value

def output(pin, value):
    assert PIN_MAPPINGS[pin] == OUT
    assert value in (0, 1)
    print '> GPIO pin %d out %d' % (pin, value)
