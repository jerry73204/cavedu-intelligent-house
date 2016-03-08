#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import logging
import signal
import serial

# flag indicating if any signal is received
SHUTDOWN_FLAG = False

# the delay time (ms) after each loop
LOOP_DELAY = 50

# the path of serial device
SERIAL_DEVICE   = '/dev/ttyAMA0'
SERIAL_BAUDRATE = 115200

# state constants
STATE_OPEN      = 0
STATE_CLOSED    = 1
STATE_INVADED   = 2
STATE_EMERGENCY = 3

def main():
    serial_device = serial.Serial(port=SERIAL_DEVICE,
                                  baudrate=SERIAL_BAUDRATE,
                                  parity=serial.PARITY_NONE,
                                  stopbits=serial.STOPBITS_ONE,
                                  bytesize=serial.EIGHTBITS,
                                  timeout=1)

    prev_door_state = is_door_open()
    state = STATE_OPEN if prev_door_state else STATE_CLOSED

    # utility functions
    def is_door_open():
        # TODO implementation
        return True

    def is_authenticated():
        # TODO implementation
        return True

    def is_signaled_emergency():
        payload = serial_device.read(size=65536)
        return len(payload) > 0

    def open_door():
        # TODO implementation
        pass

    def warn_invaded():
        serial_device.write('I')

    # event handlers
    def on_auth():
        if state == STATE_OPEN:     # ignore this case
            return

        elif state == STATE_CLOSED: # open the door
            open_door()
            state = STATE_OPEN

        elif state in (STATE_INVADED, STATE_EMERGENCY): # reset to closed state
            state = STATE_CLOSED

    def on_housebreaking():
        state = STATE_INVADED
        warn_invaded()

    def on_emergency():
        state = STATE_EMERGENCY

    def on_door_close():
        assert state == STATE_OPEN
        state = STATE_CLOSED

    # monitor the events by polling
    while True:
        if SHUTDOWN_FLAG:
            logging.info('Shutting down...')
            exit()

        elif is_signaled_emergency():
            on_emergency()

        elif is_authenticated():
            on_auth()

        else:
            curr_door_state = is_door_open()

            if curr_door_state != prev_door_state:
                if curr_door_state:
                    on_housebreaking()
                else:
                    on_door_close()

            prev_door_state = curr_door_state

        time.sleep(LOOP_DELAY)

def signal_handler(signum, frame):
    global SHUTDOWN_FLAG
    SHUTDOWN_FLAG = True

if __name__ == '__main__':
    # setup
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    signal.signal(signal.SIGINT, signal_handler)

    # run the main procedure
    logging.info('Access control system started')
    main()
