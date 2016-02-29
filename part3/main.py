#!/usr/bin/env python2
import RPi.GPIO as GPIO

STATE_OPEN      = 0
STATE_CLOSED    = 1
STATE_INVADED   = 2
STATE_EMERGENCY = 3

if __name__ == '__main__':
    state = STATE_CLOSED

    while True:
        if state == STATE_OPEN:
            pass

        elif state == STATE_CLOSED:
            pass

        elif state == STATE_INVADED:
            pass

        elif state == STATE_EMERGENCY:
            pass
