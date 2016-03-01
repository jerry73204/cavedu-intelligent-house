#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import logging
import signal

# flag indicating if any signal is received
SHUTDOWN_FLAG = False

# state constants
STATE_OPEN      = 0
STATE_CLOSED    = 1
STATE_INVADED   = 2
STATE_EMERGENCY = 3

# utility functions
def is_door_open():
    # TODO implementation
    return True

def is_authenticated():
    # TODO implementation
    return True

def is_signaled_emergency():
    # TODO implementation
    return True

# event handlers
def on_auth():
    # TODO implementation
    pass

def on_housebreaking():
    # TODO implementation
    pass

def on_emergency():
    # TODO implementation
    pass

def on_door_close():
    # TODO implementation
    pass

def main():
    prev_door_state = is_door_open()
    state = STATE_OPEN if prev_door_state else STATE_CLOSED

    # monitor the events by polling
    while True:
        if SHUTDOWN_FLAG:
            logging.info('Shutting down...')
            exit()

        elif is_signaled_emergency():
            on_emergency(state)

        elif is_authenticated():
            on_auth(state)

        else:
            curr_door_state = is_door_open()

            if curr_door_state != prev_door_state:
                if curr_door_state:
                    on_housebreaking(state)
                else:
                    on_door_close(state)

            prev_door_state = curr_door_state

        time.sleep(50)

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
